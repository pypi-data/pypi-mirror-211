from rest_framework.views import APIView

from ..services.resource_file_service import ResourceFileService
from ..utils.custom_tool import request_params_wrapper
from ..utils.model_handle import util_response


class UploadFileList(APIView):
    # 文件列表
    @request_params_wrapper
    def get(self, *args, request_params, **kwargs):
        data, err = ResourceFileService.get_list(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
