from Social import apis
from django.conf.urls import url

urlpatterns = [
	url(r'^rcmd_users/', apis.rcmd_users, name="rcmd_users"),
	url(r'^like/', apis.like, name="like"),
	url(r'^superlike/', apis.superlike_someone, name="superlike"),
	url(r'^dislike/', apis.dislike_someone, name="dislike"),
	url(r'^rewind/', apis.rewind, name="rewind"),
	url(r'^whoLikedMe/', apis.who_liked_me, name="whoLikedMe"),
	url(r'^friendList/', apis.friend_list, name="friendList"),
	url(r'^hotRank/', apis.hot_rank, name="hotRanke")
]