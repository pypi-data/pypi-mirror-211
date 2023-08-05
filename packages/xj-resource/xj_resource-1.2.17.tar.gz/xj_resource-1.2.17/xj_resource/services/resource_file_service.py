# coding=utf-8
from django.core.paginator import Paginator, EmptyPage

from ..models import ResourceFile
from ..utils.custom_tool import force_transform_type, format_params_handle, filter_fields_handler


# 用于异常处理
def robust(actual_do):
    def add_robust(*args, **keyargs):
        try:
            return actual_do(*args, **keyargs)
        except Exception as e:
            print(str(e))

    return add_robust


class ResourceFileService:
    file_fields = [i.name for i in ResourceFile._meta.fields]

    def __init__(self):
        pass

    @staticmethod
    def get(file_id):
        image_set = ResourceFile.objects.filter(id=file_id).values(
            "id",
            "group_id",
            "user_id",
            "title",
            "filename",
            "url",
            "format",
            "size",
            "thumb",
            "md5",
            "snapshot",
            "counter",
        ).first()
        if not image_set:
            return None, '数据库找不到图片'
        return image_set, None

    @staticmethod
    def add(params):
        new_params = {
            'group_id': params.get('group_id', None),
            'user_id': params.get('user_id', None),
            'title': params.get('title', None),
            'url': params.get('url', None),
            'filename': params.get('filename', None),
            'format': params.get('format', None),
            'size': params.get('size', None),
            'thumb': params.get('thumb', None),
            'md5': params.get('md5', None),
            'snapshot': params.get('snapshot', None),
            'counter': params.get('counter', 1),
        }
        image_set = ResourceFile(**new_params)
        image_set.save()
        return image_set, None

    @staticmethod
    def get_list(params):
        """文件分类查询"""
        params, is_pass = force_transform_type(variable=params, var_type="dict", default={})
        limit, is_pass = force_transform_type(variable=params.pop('limit', params.pop('size', 10)), var_type="int", default=10)
        page, is_pass = force_transform_type(variable=params.pop('page', 1), var_type="int", default=1)
        print("limit", limit, "page:", page)
        filter_fields = filter_fields_handler(
            input_field_expression=params.get("filter_fields"),
            default_field_list=[
                "group_id", "user_id", "title", "url", "filename", "format", "size", "thumb", "md5", "created_at", "updated_at"
            ],
            all_field_list=ResourceFileService.file_fields
        )

        # 参数过滤
        search_params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "group_id|int", "user_id|int", "title", "url", "filename", "format", "size", "md5",
                "created_start|date", "updated_start|date", "created_end|date", "updated_end|date",
                "counter",
            ],
            alias_dict={
                "title": "title__contains",
                "created_start": "created_at__gte",
                "updated_start": "updated_at__gte",
                "created_end": "created_at__lte",
                "updated_end": "updated_at__lte"
            }
        )

        # 构建ORM
        list_obj = ResourceFile.objects.extra(select={
            'created_at': 'DATE_FORMAT(created_at, "%%Y-%%m-%%d %%H:%%i:%%s")',
            'updated_at': 'DATE_FORMAT(updated_at, "%%Y-%%m-%%d %%H:%%i:%%s")'
        }).filter(**search_params).order_by("-id")
        count = list_obj.count()
        list_obj = list_obj.values(*filter_fields)
        paginator = Paginator(list_obj, limit)
        try:
            res_set = paginator.page(page)
        except EmptyPage:
            return {'count': count, 'page': page, 'limit': limit, "list": []}, None

        page_list = list(res_set.object_list)
        return {'count': count, 'page': page, 'limit': limit, "list": page_list}, None
