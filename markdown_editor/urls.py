from markdown_editor.views import upload_image

from django.conf.urls import url

app_name = 'markdown_editor'
urlpatterns = [
    url(r'^uploadimage/$', upload_image, name='upload_image'),
]