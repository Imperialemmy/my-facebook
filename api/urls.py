from django.urls import include, path
from rest_framework import routers
from .views import UsersViewSet, WorkViewSet, EducationViewSet, FriendRequestViewSet, PostViewset, StoriesViewSet, \
    CommentsViewSet, LikeViewSet, FriendListView, ConversationView, MessageHistory, MediaUploadView, \
    WatchSectionVideoUploadView, \
    ListingImageViewSet, ListingViewSet, CategoryViewSet, OfferViewSet, SavedListingViewSet, RefundRequestViewSet, \
    ReviewViewSet
from rest_framework_nested import routers
router = routers.DefaultRouter()
router.register(r"users", UsersViewSet)
router.register("work", WorkViewSet)
router.register("education", EducationViewSet)
router.register("friendrequests", FriendRequestViewSet)
router.register(r"posts", PostViewset)
router.register(r'stories',StoriesViewSet)
router.register(r'conversations',ConversationView,basename='conversations')
router.register(r'watch',WatchSectionVideoUploadView,basename='watch')
router.register(r'product-images', ListingImageViewSet, basename='product-images')
router.register(r'products', ListingViewSet, basename='products')
router.register(r'product-categories', CategoryViewSet, basename='categories')
router.register(r'my-product-offers', OfferViewSet, basename='offers')
router.register(r'saved-products', SavedListingViewSet, basename='saved-listings')
router.register(r'refund-request', RefundRequestViewSet, basename='refunds')

# router.register(r'friendslist',FriendListViewSet, basename='friends-list')



#Nested routers
#Posts section nested routers
comments_router = routers.NestedSimpleRouter(router, r"posts", lookup="post")
comments_router.register(r"comments", CommentsViewSet, basename="post-comments")
likes_router = routers.NestedSimpleRouter(router, r"posts", lookup="post")
likes_router.register(r"likes", LikeViewSet, basename="post-likes")


#Marketplace nested routers
reviews_router = routers.NestedSimpleRouter(router, r'products', lookup='product')  # Use a distinct lookup name
reviews_router.register(r'reviews', ReviewViewSet, basename='product_reviews')


urlpatterns = [
    path(r'', include(comments_router.urls)),
    path(r'', include(likes_router.urls)),
    path(r'', include(router.urls)),
    path('friends/', FriendListView.as_view(), name='friends'),
    # path('conversations/', ConversationListView.as_view(), name='conversation-list'),
    path('conversations/<int:conversation_id>/messages/', MessageHistory.as_view(), name='message-list'),
    path('media-upload/', MediaUploadView.as_view(), name='media-upload')
]


