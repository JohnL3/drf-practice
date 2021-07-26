from rest_framework import serializers
from .models import Profile
# from posts.models import Post
from followers.models import Follower
# pylint: disable=no-member


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    # posts = serializers.SerializerMethodField()
    # followers = serializers.SerializerMethodField()
    # following = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    # def get_posts(self, obj):
    #     return Post.objects.filter(owner=obj.owner).count()

    # def get_followers(self, obj):
    #     return Follower.objects.filter(followed=obj.owner).count()

    # def get_following(self, obj):
    #     return Follower.objects.filter(owner=obj.owner).count()

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user,
                followed=obj.owner
            ).first()
            print(following)
            print()
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        # fields = [
        #     'id', 'owner', 'is_owner', 'created_at', 'updated_at',
        #     'name', 'content', 'image', 'posts', 'followers', 'following',
        #     'following_id', 'posts_count', 'followers_count',
        #      'following_count'
        # ]
        fields = [
            'id', 'owner', 'is_owner', 'created_at', 'updated_at',
            'name', 'content', 'image',
            'following_id', 'posts_count', 'followers_count', 'following_count'
        ]
