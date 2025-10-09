from rest_framework import viewsets, permissions, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer


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
        comment = serializer.save(author=self.request.user)
        # Create notification for post author
        from notifications.models import Notification

        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb="commented on your post",
                target=comment.post,
            )


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


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    """Like a post"""
    post = get_object_or_404(Post, pk=pk)

    # Check if user already liked the post
    if Like.objects.filter(user=request.user, post=post).exists():
        return Response(
            {"error": "You have already liked this post"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Create the like
    like = Like.objects.create(user=request.user, post=post)

    # Create notification for post author
    from notifications.models import Notification

    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post,
        )

    return Response(
        {"message": "Post liked successfully"}, status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    """Unlike a post"""
    post = get_object_or_404(Post, pk=pk)

    # Check if like exists
    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        return Response(
            {"message": "Post unliked successfully"}, status=status.HTTP_200_OK
        )
    except Like.DoesNotExist:
        return Response(
            {"error": "You have not liked this post"},
            status=status.HTTP_400_BAD_REQUEST,
        )
