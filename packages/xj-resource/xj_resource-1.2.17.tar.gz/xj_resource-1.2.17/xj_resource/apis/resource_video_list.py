from rest_framework.views import APIView

from ..services.resource_video_service import ResourceVideoService
from ..utils.custom_tool import request_params_wrapper
from ..utils.model_handle import util_response


class UploadVideoList(APIView):
    # 文件列表
    @request_params_wrapper
    def get(self, *args, request_params, **kwargs):
        data, err = ResourceVideoService.get_list(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
