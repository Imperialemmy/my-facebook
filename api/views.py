from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from marketplace.models import ListingImage, Listing, Category, Offer, SavedListing, Refund, Review
from users.models import CustomUser, Work, Education, FriendRequest
from messaging.models import MessageMedia
from posts.models import Post, PostImage, PostVideo, Stories, Comments, Like
from messaging.models import Conversation, Message
from watch.models import Video
from .serializers import CustomUserSerializer, WorkSerializer, EducationSerializer, FriendRequestSerializer, PostSerializer, StoriesSerializer, \
    CommentsSerializer, LikeSerializer,FriendListSerializer, MessageSerializer, ConversationSerializer, MessageMediaUploadSerializer,\
    WatchSectionVideoUploadSerializer, ListingImageSerializer, ListingSerializer, CategorySerializer, OfferSerializer, SavedListingSerializer,\
    RefundSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView
from .pagination import CustomPaginationForPosts,ChatPagination






class UsersViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]



class WorkViewSet(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticated]



class EducationViewSet(ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]




class FriendRequestViewSet(ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        receiver_id = self.request.data.get("receiver")
        receiver = get_object_or_404(CustomUser, id=receiver_id)

        if FriendRequest.objects.filter(sender=self.request.user, receiver=receiver).exists():
            return Response({"detail": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(sender=self.request.user, receiver=receiver)

    @action(detail=True, methods=["POST", "GET"])
    def accept(self, request, pk=None):
        """Accept a friend request"""
        friend_request = self.get_object()
        if friend_request.receiver != request.user:
            return Response({"detail": "You can't accept this request."}, status=status.HTTP_403_FORBIDDEN)

        friend_request.accept()
        return Response({"detail": "Friend request accepted!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST", "GET"])
    def decline(self, request, pk=None):
        """Decline a friend request"""
        friend_request = self.get_object()
        if friend_request.receiver != request.user:
            return Response({"detail": "You can't decline this request."}, status=status.HTTP_403_FORBIDDEN)

        friend_request.decline()
        return Response({"detail": "Friend request declined."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST", "GET"])
    def cancel(self, request, pk=None):
        """Cancel a friend request"""
        friend_request = self.get_object()
        if friend_request.sender != request.user:
            return Response({"detail": "You can't cancel this request."}, status=status.HTTP_403_FORBIDDEN)

        friend_request.cancel()
        return Response({"detail": "Friend request canceled."}, status=status.HTTP_200_OK)




class PostViewset(ModelViewSet):
    queryset = Post.objects.order_by('?')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPaginationForPosts
    filterset_fields = {
        'privacy': ['exact'],
    }
    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response({"error": "You can only delete your own posts."}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def my_posts(self,request):
        posts=Post.objects.filter(user=request.user)
        serializer=self.get_serializer(posts,many=True)
        return Response(serializer.data)




class StoriesViewSet(ModelViewSet):
    queryset = Stories.objects.all().order_by('-created_at')
    serializer_class = StoriesSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        story = self.get_object()
        if story.user != request.user:
            return Response({"error": "You can only delete your own stories."}, status=status.HTTP_403_FORBIDDEN)

        story.delete()
        return Response({"message": "Story deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET", "POST"], permission_classes=[IsAuthenticated])
    def my_stories(self, request):
        if request.method == "GET":
            stories = Stories.objects.filter(user=request.user)
            serializer = self.get_serializer(stories, many=True)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



class CommentsViewSet(ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return Comments.objects.filter(post=self.kwargs['post_pk'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post_pk = self.kwargs['post_pk']

        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer.save(post=post, user=request.user)
        # serializer.save(recipe=recipe)#Without user auth
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return Response({"error": "You can only delete your own comments."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def my_comments(self, request):
        comments = Comments.objects.filter(user=request.user)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)



class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        like = self.get_object()
        if like.user != request.user:
            return Response({"error": "You can only delete your own likes."}, status=status.HTTP_403_FORBIDDEN)

        like.delete()
        return Response({"message": "Like deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def my_likes(self, request, *args, **kwargs):
        likes = Like.objects.filter(user=request.user)
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data)


class FriendListView(ListAPIView):
    """List of all the logged-in user's friends"""
    serializer_class = FriendListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return friend requests received by the logged-in user."""
        return CustomUser.objects.filter(friends=self.request.user)



# Chat view for websockets /////////////////////////////////////////////////////////////////////////////////////////////
class MediaUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Allows file uploads

    def post(self, request, *args, **kwargs):
        serializer = MessageMediaUploadSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()  # Saves files and returns their URLs
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConversationView(ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Fetch all conversations where the logged-in user is a participant"""
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """Ensure two users are added when creating a conversation"""
        user1 = self.request.user
        user2_id = self.request.data.get("user2")

        if not user2_id:
            return Response({"error": "user2 is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user2 = CustomUser.objects.get(id=user2_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if conversation already exists
        conversation = Conversation.objects.filter(participants=user1).filter(participants=user2).first()

        if not conversation:
            conversation = serializer.save()
            conversation.participants.add(user1, user2)

        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        conversation = self.get_object()
        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant in this conversation"}, status=status.HTTP_403_FORBIDDEN)

        conversation.delete()
        return Response({"message": "Conversation deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



class MessageHistory(ListAPIView):
    serializer_class = MessageSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    pagination_class = ChatPagination

    def get_queryset(self):
        try:
            conversation_id = self.kwargs['conversation_id']
            return Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
        except Message.DoesNotExist:
            return Response({"error": "Message not found"}, status=404)



class WatchSectionVideoUploadView(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = WatchSectionVideoUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


    def destroy(self, request, *args, **kwargs):
        video = self.get_object()
        if video.user != request.user:
            return Response({"error": "You can only delete your own videos."}, status=status.HTTP_403_FORBIDDEN)

        video.delete()
        return Response({"message": "Video deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def my_videos(self, request):
        videos = PostVideo.objects.filter(user=request.user)
        serializer = self.get_serializer(videos, many=True)
        return Response(serializer.data)



class ListingImageViewSet(ModelViewSet):
    queryset = ListingImage.objects.all()
    serializer_class = ListingImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def destroy(self, request, *args, **kwargs):
        image = self.get_object()
        if image.user != request.user:
            return Response({"error": "You can only delete your own images."}, status=status.HTTP_403_FORBIDDEN)

        image.delete()
        return Response({"message": "Image deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def my_images(self, request):
        images = PostImage.objects.filter(user=request.user)
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)


class ListingViewSet(ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]

class SavedListingViewSet(ModelViewSet):
    queryset = SavedListing.objects.all()
    serializer_class = SavedListingSerializer
    permission_classes = [IsAuthenticated]

class RefundRequestViewSet(ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Automatically set the user when creating a refund request """
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        """ Approve a refund request """
        refund = self.get_object()
        refund.approve()
        return Response({"message": "Refund request approved."})

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        """ Reject a refund request """
        refund = self.get_object()
        refund.reject()
        return Response({"message": "Refund request rejected."})


class ReviewViewSet(ModelViewSet): #api/products/product_pk/reviews
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Review.objects.filter(recipe=self.kwargs['product_pk'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_pk = self.kwargs['product_pk']

        try:
            product = Listing.objects.get(pk=product_pk)
        except Listing.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer.save(product=product, user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)