from rest_framework import permissions, generics, filters
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import IsOwnerOrReadOnly
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
# pylint: disable=no-member


class PostList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # queryset = Post.objects.all()
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('created_at')
    serializer_class = PostSerializer
    filter_backends = [
                filters.SearchFilter,
                filters.OrderingFilter,
                DjangoFilterBackend
            ]
    filterset_fields = [
        'owner__profile',
        'owner__followed__owner__profile',
        'likes__owner__profile'
    ]
    search_fields = ['owner__username', 'title']
    ordering_fields = ['likes_count', 'comments_count', 'likes__created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('created_at')
