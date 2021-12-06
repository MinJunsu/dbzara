from movie.serializers.base import *


class MovieListSerializer(MovieSerializer):
    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ['reservation_rate']


class ReservationBaseMovieSerializer(MovieSerializer):
    class Meta(MovieSerializer.Meta):
        fields = ['id', 'name', 'grade']


class ReservationChoiceMovieSerializer(ReservationBaseMovieSerializer):
    class Meta(ReservationBaseMovieSerializer.Meta):
        pass


class MovieRankSerializer(MovieSerializer):
    # TODO: 예약 인원을 파악할 수 있는 모델 제작 이후 rank 추가
    class Meta:
        model = Movie
        fields = ['id', 'name', 'images']


class MovieDetailSerializer(MovieSerializer):
    genres = GenreSerializer(many=True)
    distributors = DistributorSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'name', 'poster', 'backdrop', 'grade', 'running_time', 'summary', 'opening_date', 'genres', 'distributors']


class MovieReservationSerializer(MovieSerializer):

    class Meta(MovieSerializer.Meta):
        fields = []


class MovieStaffSerializer(MovieSerializer):
    actors = CharacterSerializer(source='short_actors', many=True)
    directors = DirectorSerializer(source='short_directors', many=True)

    class Meta(MovieSerializer.Meta):
        fields = ['actors', 'directors']


class MovieImageSerializer(MovieSerializer):
    images = ImageSerializer(many=True)

    class Meta(MovieSerializer.Meta):
        fields = ['images']


class MovieVideoSerializer(MovieSerializer):
    videos = VideoSerializer(many=True)

    class Meta(MovieSerializer.Meta):
        fields = ['videos']


class MovieReviewSerializer(MovieSerializer):
    reviews = ReviewSerializer(source='review_set', many=True)

    class Meta(MovieSerializer.Meta):
        fields = ['reviews']
