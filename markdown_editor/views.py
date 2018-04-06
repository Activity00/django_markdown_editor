import os
import time
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from markdown_editor import settings as markdown_settings


@csrf_exempt
def upload_image(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        _file = request.FILES.get("editormd-image-file", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not _file:
            return HttpResponse(json.dumps({'success': 0, 'message': 'upload image failed'}, ensure_ascii=False),
                                content_type="application/json")

        media_root = markdown_settings.MEDIA_ROOT
        strs = _file.name.split('.')
        suffix = strs[-1]
        file_name = strs[0]
        if not suffix or suffix not in markdown_settings.MARKDOWN_IMAGE_FORMATS:
            return HttpResponse(json.dumps({'success': 0, 'message': 'upload image failed'}, ensure_ascii=False),
                                content_type="application/json")
        now_time = str(int(time.time()*1000))
        file_name = file_name.replace('(', '[').replace(')', ']')
        image_floder = os.path.join(media_root, markdown_settings.MARKDOWN_IMAGE_FLODER)
        if not os.path.exists(image_floder):
            os.makedirs(image_floder)

        image_name = file_name+ "_" + now_time + "." + suffix
        count = 1
        while os.path.exists(os.path.join(image_floder, image_name)):
            image_name = file_name + "_" + now_time + "["+str(count)+"]." + suffix
            count += 1

        destination = open(os.path.join(image_floder, image_name), 'wb+')
        for chunk in _file.chunks():
            destination.write(chunk)
        destination.close()
        return HttpResponse(json.dumps({'success': 1, 'message': 'upload image successed',
                                        'url': markdown_settings.MEDIA_URL+markdown_settings.MARKDOWN_IMAGE_FLODER+"/"+ image_name},
                                       ensure_ascii=False), content_type="application/json")
