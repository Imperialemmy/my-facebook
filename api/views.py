from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser, Work, Education, FriendRequest
from posts.models import Post, PostImage, PostVideo, Stories, Comments, Like
from messaging.models import Conversation, Message
from .serializers import CustomUserSerializer, WorkSerializer, EducationSerializer, FriendRequestSerializer, PostSerializer, StoriesSerializer, CommentsSerializer, LikeSerializer,FriendListSerializer, MessageSerializer, ConversationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination



class CustomPaginationForPosts(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



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



# Chat view
class ConversationListView(ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)  # Add user to conversation
        return Response(serializer.data)


class MessageListView(ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')

    def perform_create(self, serializer):
        conversation = get_object_or_404(Conversation, id=self.kwargs['conversation_id'])
        serializer.save(sender=self.request.user, conversation=conversation)