from rest_framework import generics, filters
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
# pylint: disable=no-member


class ProfileList(generics.ListAPIView):
    # queryset = Profile.objects.all()
    '''
    owner refers to the field, post refers to the model
    fot the next two owner refers to the field, and as the model is Follower
    we cant use it twice so insetead we refer to the realated_name of the fields
    in the Follower model
    '''
    # q = Profile.objects.annotate(posts_count=Count('owner__post', distinct=True))
    # print(q.query)
    # q = Profile.objects.filter(owner_id=5)
    # print(q.query)
    # print(q)
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count(
            'owner__following', distinct=True
            )
        ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
            'posts_count',
            'followers_count',
            'following_count',
            'owner__following__created_at',
            'owner__followed__created_at'
        ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    # queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count(
            'owner__following', distinct=True
            )
        ).order_by('-created_at')
