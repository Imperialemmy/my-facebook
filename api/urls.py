from django.urls import include, path
from rest_framework import routers
from .views import UsersViewSet, WorkViewSet, EducationViewSet, FriendRequestViewSet, PostViewset, StoriesViewSet, \
    CommentsViewSet, LikeViewSet, FriendListView
from rest_framework_nested import routers
router = routers.DefaultRouter()
router.register(r"users", UsersViewSet)
router.register("work", WorkViewSet)
router.register("education", EducationViewSet)
router.register("friendrequests", FriendRequestViewSet)
router.register(r"posts", PostViewset)
router.register(r'stories',StoriesViewSet)
# router.register(r'friendslist',FriendListViewSet, basename='friends-list')



#Nested routers
comments_router = routers.NestedSimpleRouter(router, r"posts", lookup="post")
comments_router.register(r"comments", CommentsViewSet, basename="post-comments")
likes_router = routers.NestedSimpleRouter(router, r"posts", lookup="post")
likes_router.register(r"likes", LikeViewSet, basename="post-likes")


urlpatterns = [
    path(r'', include(comments_router.urls)),
    path(r'', include(likes_router.urls)),
    path(r'', include(router.urls)),
    path('friends/', FriendListView.as_view(), name='friends'),
]


