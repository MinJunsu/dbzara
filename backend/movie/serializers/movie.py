from movie.serializers.base import *


class ReservationBaseMovieSerializer(MovieSerializer):
    class Meta(MovieSerializer.Meta):
        fields = ['id', 'name', 'grade']


class ReservationChoiceMovieSerializer(ReservationBaseMovieSerializer):
    class Meta(ReservationBaseMovieSerializer.Meta):
        pass


class MovieDetailSerializer(MovieSerializer):
    genres = GenreSerializer(many=True)
    distributors = DistributorSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'name', 'poster', 'backdrop', 'watch_grade', 'running_time',
                  'summary', 'opening_date', 'genres', 'distributors', 'reservation', 'review']


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
