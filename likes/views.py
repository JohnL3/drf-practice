from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from likes.models import Like
from likes.serializers import LikeSerializer
# pylint: disable=no-member


class LikeList(generics.ListCreateAPIView):
    """
    List all likes. Create a like if authenticated.
    The perform_create method associates the like with the logged in user.
    """

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a like. No Update view, as users can only like or unlike a post.
    Destroy a like, i.e. unlike a post if owner of that like
    """

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsOwnerOrReadOnly]
