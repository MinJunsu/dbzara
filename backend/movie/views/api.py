from datetime import date

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from accounts.models import Profile
from movie.models import Movie, Review, MovieInfo
from movie.serializers import (
    MovieListSerializer, MovieDetailSerializer, MovieStaffSerializer, MovieImageSerializer,
    MovieVideoSerializer, MovieReviewSerializer, ReviewSerializer, MovieInfoSerializer
)


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 12
    max_page_size = 10


class MovieListAPIView(ListModelMixin, GenericAPIView):
    queryset = Movie.objects.all()
    permission_classes = [AllowAny]
    pagination_class = BasicPagination
    serializer_class = MovieListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        option = self.request.query_params.get('option', 'box-office')
        today = date(2021, 11, 10)
        query_set = super().get_queryset()

        if option == 'box-office':
            return sorted(query_set.filter(
                closing_date__gte=today
            ), key=lambda movie: movie.reservation_rate, reverse=True)

        elif option == 'not-open':
            return sorted(query_set.filter(
                opening_date__gte=today
            ), key=lambda movie: movie.reservation_rate, reverse=True)


class MovieBaseAPIView (RetrieveModelMixin, GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Movie.objects.all()

    @swagger_auto_schema(responses={
        200: 'Return Object',
        404: 'Object Does not exist'
    })
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class MovieAPIDetailView(MovieBaseAPIView):
    serializer_class = MovieDetailSerializer


class MovieInfoAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = MovieInfo.objects.all()
    serializer_class = MovieInfoSerializer


class MovieStaffAPIView(MovieBaseAPIView):
    serializer_class = MovieStaffSerializer


class MovieImageAPIView(MovieBaseAPIView):
    """
    Movie Image View
    ___
    영화와 관련된 이미지 반환
    """
    serializer_class = MovieImageSerializer


class MovieVideoAPIView(MovieBaseAPIView):
    serializer_class = MovieVideoSerializer


class MovieReviewAPIView(ListModelMixin, MovieBaseAPIView):
    serializer_class = MovieReviewSerializer
    pagination_class = BasicPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ReviewBaseAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer = ReviewSerializer
    model = Review


class ReviewAPIView(ReviewBaseAPIView):
    movie_field = openapi.Schema(
        'movie',
        description='movie number.',
        type=openapi.TYPE_INTEGER
    )
    comment_field = openapi.Schema(
        'comment',
        description='comment.',
        type=openapi.TYPE_STRING
    )
    score_field = openapi.Schema(
        'score',
        description='score.',
        type=openapi.TYPE_INTEGER
    )
    response = openapi.Schema(
        'response',
        type=openapi.TYPE_OBJECT,
        properties={
            'movie': movie_field,
            'comment': comment_field,
            'score': score_field}
    )

    @swagger_auto_schema(responses={
        200: response,
        400: 'Not Authentication'
    })
    def post(self, request):
        serializer = self.serializer(data=request.data)
        profile = Profile.objects.get(user=request.user)
        if serializer.is_valid():
            serializer.save(profile=profile)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ReviewDetailAPIView(ReviewBaseAPIView):
    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def is_author(self, request, pk):
        if request.user == self.get_object(pk).profile.user:
            return True
        return False

    def put(self, request, pk):
        if self.is_author(request, pk):
            review = self.get_object(pk)
            serializer = self.serializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        if self.is_author(request, pk):
            review = self.get_object(pk)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
