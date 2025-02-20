from users.models import CustomUser, Work, Education, FriendRequest
from posts.models import Post, PostImage, PostVideo, Stories, Comments, Like
from rest_framework import serializers

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['post_picture', 'image']

class PostVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVideo
        fields = ['post_video', 'video']


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer):
    work_experiences = WorkSerializer(many=True, read_only=True)
    education_history = EducationSerializer(many=True, read_only=True)
    friends_count = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'bio', 'about_me', 'profile_picture', 'cover_photo', 'date_of_birth', 'gender', 'location', 'website', 'relationship_status', 'friends', 'friends_count', 'is_private', 'allow_messages', 'work_experiences', 'education_history', 'email', 'password', 'username']
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def get_friends_count(self, obj):
        return obj.friends_count()


    def create(self, validated_data):
        work_data = validated_data.pop("work_experiences")
        education_data = validated_data.pop("education_history")
        user = CustomUser.objects.create(**validated_data)
        work_data.tags.set(work_data)
        education_data.ingredients_used.set(education_data)

        for work in work_data:
            Work.objects.create(user=user, **work)

        for education in education_data:
            Education.objects.create(user=user, **education)

        return user

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"
        read_only_fields = ["sender", "status"]


class PostSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    post_images = PostImageSerializer(many=True, read_only=True)  # Nested serializer for existing images
    post_videos = PostVideoSerializer(many=True, read_only=True)  # Nested serializer for existing videos
    uploaded_images = serializers.ListField(child=serializers.ImageField(max_length=100, allow_empty_file=False, use_url=False), write_only=True, required=False)
    uploaded_videos = serializers.ListField(child=serializers.ImageField(max_length=100, allow_empty_file=False, use_url=False), write_only=True,required=False)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'username', 'content', 'privacy', 'shared_from', 'tagged_users', 'created_at', 'updated_at', 'post_images', 'post_videos', 'uploaded_images', 'uploaded_videos', 'likes']
        read_only_fields = ["user", "created_at", "updated_at", "likes"]

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        uploaded_videos = validated_data.pop('uploaded_videos', [])
        tagged_users = validated_data.pop('tagged_users', [])
        post = Post.objects.create(user=self.context['request'].user,   **validated_data)
        post.tagged_users.set(tagged_users)

        for image in uploaded_images:
            PostImage.objects.create(post_picture=post, image=image)

        for video in uploaded_videos:
            PostVideo.objects.create(post_video=post, video=video)

        return post

    def update(self, instance, validated_data):
        # Ensure only content and privacy can be updated
        instance.content = validated_data.get('content', instance.content)
        instance.privacy = validated_data.get('privacy', instance.privacy)
        tagged_users = validated_data.get('tagged_users', None)
        if tagged_users is not None:
            instance.tagged_users.set(tagged_users)
        instance.save()
        return instance


class StoriesSerializer(serializers.ModelSerializer):
    post_images = PostImageSerializer(many=True, read_only=True)  # Nested serializer for existing images
    post_videos = PostVideoSerializer(many=True, read_only=True)  # Nested serializer for existing videos
    uploaded_images = serializers.ListField(child=serializers.ImageField(max_length=100, allow_empty_file=False, use_url=False), write_only=True, required=False)
    uploaded_videos = serializers.ListField(child=serializers.ImageField(max_length=100, allow_empty_file=False, use_url=False), write_only=True, required=False)
    likes = LikeSerializer(many=True, read_only=True)
    class Meta:
        model = Stories
        fields = ['id', 'user', 'created_at', 'post_images', 'post_videos', 'uploaded_images', 'uploaded_videos', 'likes']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        uploaded_videos = validated_data.pop('uploaded_videos', [])
        story = Stories.objects.create(user=self.context['request'].user,   **validated_data)
        for image in uploaded_images:
            PostImage.objects.create(story=story, image=image)

        for video in uploaded_videos:
            PostVideo.objects.create(story=story, video=video)

        return story


class CommentsSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    class Meta:
        model = Comments
        fields = ['id', 'user', 'post', 'content', 'image', 'video', 'created_at', 'updated_at', 'likes']
        read_only_fields = ["user", "post", "created_at", "updated_at"]


class FriendListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id' ,'friends']