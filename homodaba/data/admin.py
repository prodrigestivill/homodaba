from django.contrib import admin
from django.db.models import Q

from .models import Movie, Person, MovieStorageType, MoviePerson, Tag, GenreTag, TitleAka, ContentRatingTag
from .search import populate_search_filter

# from easy_select2 import select2_modelform
# MovieForm = select2_modelform(Movie, attrs={'width': '250px'})

class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)

class GenreTagAdmin(admin.ModelAdmin):
    pass
admin.site.register(GenreTag, GenreTagAdmin)

class TitleAkaAdmin(admin.ModelAdmin):
    pass
admin.site.register(TitleAka, TitleAkaAdmin)

class CustomAbstractTagListFilter(admin.SimpleListFilter):
    """
    Filtro personalizado para AbstractTag
    """
    title = 'Filtro de tags personalizado'
    parameter_name = 'tag'
    tag_model = None
    tag_filter = 'tags__id'

    def lookups(self, request, model_admin):
        filters = tuple()
        for gt in self.tag_model.objects.order_by('name').all():
            filters = filters + ((gt.id, gt.name),)

        return filters
 
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{self.tag_filter: self.value()})
        
        return queryset
    
    class Meta:
        abstract = True

class TagListFilter(CustomAbstractTagListFilter):
    title = 'Etiquetas'
    parameter_name = 'tag'
    tag_model = Tag
    tag_filter = 'tags__id'


class GenreListFilter(CustomAbstractTagListFilter):
    title = 'Géneros'
    parameter_name = 'genre'
    tag_model = GenreTag
    tag_filter = 'genres__id'

class ContentRatingListFilter(CustomAbstractTagListFilter):
    title = 'Clasificaciones de edad'
    parameter_name = 'crs'
    tag_model = ContentRatingTag
    tag_filter = 'content_rating_systems__id'


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'get_poster_thumbnail_img', 'get_directed_by', 'get_other_titles', 'get_storage_types_html', 'rating',)
    
    # TODO: Pensar que hacemos con title_akas
    exclude = ('title_akas',)
    list_filter = (TagListFilter, GenreListFilter, ContentRatingListFilter,)

    # Lo ponemos para que saque la caja de texto pero la busqueda
    # la hacemos manualmente en get_search_results
    search_fields = ('title',)

    def get_search_results(self, request, queryset, search_term):
        # Si No hay terminos de busqueda devolvemos el queryset tal como esta
        if not search_term:
            return queryset, False

        # OJO: Esto es solo para DSL VVVVV
        genre_filter = None
        if 'genre' in request.GET.keys():
            if request.GET['genre']:
                genre_filter = int(request.GET['genre'])
        
        crs_filter = None
        if 'crs' in request.GET.keys():
            if request.GET['crs']:
                crs_filter = int(request.GET['crs'])

        tag_filter = None
        if 'tag' in request.GET.keys():
            if request.GET['tag']:
                tag_filter = int(request.GET['tag'])
        # OJO: Esto es solo para DSL ^^^^
        
        return populate_search_filter(queryset, search_term, use_use_distinct=True, genre=genre_filter, content_rating_system=crs_filter, tag=tag_filter)

    # form = MovieForm
admin.site.register(Movie, MovieAdmin)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'imdb_id', 'avatar_url')
admin.site.register(Person, PersonAdmin)

class MovieStorageTypeAdmin(admin.ModelAdmin):
    list_display = ('get_movie_title', 'is_original', 'storage_type', 'media_format', 'resolution')
    list_filter = ('storage_type', 'media_format', )
    def get_movie_title(self, obj):
        return obj.movie.title
    get_movie_title.short_description = 'Pelicula'
    get_movie_title.admin_order_field = 'movie__title'
admin.site.register(MovieStorageType, MovieStorageTypeAdmin)

class MoviePersonAdmin(admin.ModelAdmin):
    list_display = ('get_movie_title', 'get_movie_year', 'get_person_name', 'role')
    list_filter = ('role', )

    def get_movie_title(self, obj):
        return obj.movie.title
    get_movie_title.short_description = 'Pelicula'
    get_movie_title.admin_order_field = 'movie__title'

    def get_movie_year(self, obj):
        return obj.movie.year
    get_movie_year.short_description = 'Año'
    get_movie_year.admin_order_field = 'movie__year'

    def get_person_name(self, obj):
        return obj.person.name
    get_person_name.short_description = 'Participante'
    get_person_name.admin_order_field = 'person__name'

admin.site.register(MoviePerson, MoviePersonAdmin)
