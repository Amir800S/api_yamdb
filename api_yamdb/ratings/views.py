from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from ratings.models import Comment, Review
from ratings.serializers import CommentSerializer, ReviewSerializer
from ratings.permissions import IsAuthorOrReadOnly
from reviews.models import Title

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=int(self.kwargs.get('title_id')))
        print(title)
        queryset = Review.objects.filter(title_id=title.id)
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=int(self.kwargs.get('title_id')))
        serializer.save(author=self.request.user, title_id=title.id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=int(self.kwargs.get('review_id')))
        queryset = Comment.objects.filter(review_id=review.id)
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=int(self.kwargs.get('review_id')))
        serializer.save(author=self.request.user, review_id=review.id)
