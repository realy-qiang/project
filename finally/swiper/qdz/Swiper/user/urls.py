from django.conf.urls import url

from user import apis

urlpatterns = [
    url(r'^get_code/', apis.get_code, name='get_code'),
    url(r'^submit_code/', apis.submit_code, name='submit_code'),
    url(r'^get_profile/', apis.get_profile, name='profile'),
    url(r'^set_profile/', apis.set_profile, name='set_profile'),
    url(r'^upload_avatar/', apis.upload_avatar, name='upload_avatar')
]
