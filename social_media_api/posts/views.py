from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author
        return obj.author == request.user


class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def feed_view(request):
    """
    Get posts from users that the current user follows
    """
    # Get users that the current user is following
    following_users = request.user.following.all()

    # Get posts from those users, ordered by most recent first
    feed_posts = Post.objects.filter(author__in=following_users).order_by("-created_at")

    # Paginate the results
    paginator = StandardResultsPagination()
    paginated_posts = paginator.paginate_queryset(feed_posts, request)

    # Serialize the data
    serializer = PostSerializer(paginated_posts, many=True)

    return paginator.get_paginated_response(serializer.data)
