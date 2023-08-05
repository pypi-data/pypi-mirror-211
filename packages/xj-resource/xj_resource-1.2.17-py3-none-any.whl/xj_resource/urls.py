# _*_coding:utf-8_*_
from django.conf.urls import url

from .apis.resource_file_list import UploadFileList
from .apis.resource_image_list import UploadImageList
from .apis.resource_upload_file import UploadFile
from .apis.resource_upload_image import UploadImage
from .apis.resource_upload_video import UploadVideo
from .apis.resource_video_list import UploadVideoList

# 应用名称
app_name = 'resource'

urlpatterns = [
    # 上传接口
    url(r'upload_file/?$', UploadFile.as_view(), name='st_upload_file'),  # 文件上传
    url(r'upload_image/?$', UploadImage.as_view(), name='st_upload_image'),  # 图片上传
    url(r'upload_video/?$', UploadVideo.as_view(), name='st_upload_image'),  # 图片上传
    # 列表接口
    url(r'image_list/?$', UploadImageList.as_view(), name='st_image_list'),  # 图片列表
    url(r'file_list/?$', UploadFileList.as_view(), name='st_file_list'),  # 文件列表
    url(r'video_list/?$', UploadVideoList.as_view(), name='st_video_list'),  # 文件列表
    # re_path(r'^_upload_image/?$', UploadImage.as_view(), ),

]
