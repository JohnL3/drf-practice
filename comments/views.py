from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentDetailSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
# pylint: disable=no-member


class CommentList(generics.ListCreateAPIView):
    """
    List all comments
    Create a new comment if authenticated
    Associate the current logged in user with the comment
    """

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['post']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # def get_serializer_context(self):
    #     context = super(CommentList, self).get_serializer_context()
    #     context.update({'request': self.request})
    #     return context


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a comment
    update or delete a comment if owner
    """

    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.all()

    # def get_serializer_context(self):
    #     context = super(CommentDetail, self).get_serializer_context()
    #     context.update({'request': self.request})
    #     return context
