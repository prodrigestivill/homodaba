from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils.translation import gettext as _
from django.utils.text import slugify


from data.models import Movie, TitleAka
from data.models import get_first_or_create_tag, get_or_create_country

from data.utils import trace
from data.utils.imdbpy_facade import get_imdb_movie, get_imdb_titles

import re
import xml.etree.ElementTree as ET

"""
>>> from data.models import Movie
>>> zombieland = Movie.objects.filter(title='Zombieland')[0]
>>> xml_movie = ET.fromstring(zombieland.imdb_raw_data)
>>> xml_movie.findall("//certificates/item")

"""

class Command(BaseCommand):
    help = _("""Optimiza la base de datos y reduce el numero de relaciones de 
peliculas con otras entidades como TitleAka y MoviePerson.

Opciones:
--title-akas, Elimina todos los TitleAka actuales y crea nuevos buscando solo
las primeras coincidencias de:
    - Pais/es origen de la pelicula
    - Spanish
    - English

Antes de ejecutar conviene borrar la tabla primero con el argumento:
'--clear-akas'""")

    def add_arguments(self, parser):
        parser.add_argument(
            '--title-akas',
            action='store_true',
            help='Optimiza y limpia de innecesarios TitleAka.',
        )
        parser.add_argument(
            '--clear-akas',
            action='store_true',
            help='Borra la tabla de akas al principio.',
        )
        parser.add_argument(
            '--movie-id',
            type=str,
            help='Solo chequea la pelicula con ese id (ojo, id de la bbdd, NO imdb_id)',
        )

    def handle(self, *args, **options):
        verbosity = options['verbosity']
        trace.set_verbosity(verbosity)

        if 'clear_akas' in options and options['clear_akas']:
            TitleAka.objects.all().delete()
        
        query_movies = Movie.objects

        if 'movie_id' in options and options['movie_id']:
            query_movies =  Movie.objects.filter(id=int(options['movie_id']))

        for movie in query_movies.all():
            trace.debug('>> %s (%s) [id:%s]' % (movie.title, movie.get_countries_as_text(), movie.id))
            title_akas = {}
            new_titles = {}

            if movie.imdb_id:
                imdb_movie = get_imdb_movie(movie.imdb_id)

                # Completando paises de la peli
                if movie.countries.count() == 0 and 'countries' in imdb_movie.keys():
                    for c in imdb_movie['countries']:
                        movie.countries.add(get_or_create_country(
                            country=c
                        ))
                    movie.save()

                new_titles, title_akas = get_imdb_titles(imdb_movie)

                if len(title_akas.keys()) > 0:
                    trace.debug(" * Los akas para la pelicula '%s' son:" % movie.title)

                    movie.title_akas.clear()

                    for country in title_akas.keys():
                        trace.debug("    - %s [%s]" % (title_akas[country], country))
                    
                        db_title_aka = get_first_or_create_tag(
                            TitleAka, title=title_akas[country]
                        )

                        if db_title_aka.country:
                            if db_title_aka.country != country:
                                # El problema aqui es que el aka deberia permitir varios paises... 
                                # pero tenemos un poco en el aire que hacemos con TitleAka (yo 
                                # ultimamente pienso que tendriamos que borrarla... asi que por 
                                # ahora solo informamos en modo debug)
                                trace.debug("Tenemos este titulo como aka con distinto pais titulo:'%s' pais_db:'%s' pais_title:'%s'" % (
                                    title_akas[country], db_title_aka.country, country
                                ))
                        else:
                            db_title_aka.country = country
                            db_title_aka.save()
                        
                        movie.title_akas.add(db_title_aka)
                    
                    movie.save()
                
                trace.debug(" * Los titulos antiguos para la pelicula '%s' son:" % movie.title)
                trace.debug("    - %s: '%s'" % ('title', movie.title))
                trace.debug("    - %s: '%s'" % ('title_original', movie.title_original))
                trace.debug("    - %s: '%s'" % ('title_preferred', movie.title_preferred))
                
                if len(new_titles.keys()) == 3:
                    trace.debug(" * Los titulos nuevos para la pelicula '%s' son:" % movie.title)
                    trace.debug("    - %s: '%s'" % ('title', new_titles['title']))
                    trace.debug("    - %s: '%s'" % ('title_original', new_titles['title_original']))
                    trace.debug("    - %s: '%s'" % ('title_preferred', new_titles['title_preferred']))

                    change_movie = False
                    if movie.title != new_titles['title']:
                        movie.title = new_titles['title']
                        change_movie = True

                    if movie.title_original != new_titles['title_original']:
                        movie.title_original = new_titles['title_original']
                        change_movie = True

                    if movie.title_preferred != new_titles['title_preferred']:
                        movie.title_preferred = new_titles['title_preferred']
                        change_movie = True
                    
                    if change_movie:
                        movie.save()

                else:
                    trace.error("La pelicula '%s' no tiene titulos nuevos. [movie.id='%s']" % (movie.title, movie.id))
                    if len(new_titles.keys()) > 0:
                        trace.debug(" * Los titulos nuevos para la pelicula '%s' son:" % movie.title)
                        if 'title' in new_titles:
                            trace.debug("    - %s: '%s'" % ('title', new_titles['title']))
                        if 'title_original' in new_titles:
                            trace.debug("    - %s: '%s'" % ('title_original', new_titles['title_original']))
                        if 'title_preferred' in new_titles:
                            trace.debug("    - %s: '%s'" % ('title_preferred', new_titles['title_preferred']))
                
                    


"""
xml = ET.fromstring(movie.imdb_raw_data)
aka_elements = xml.findall("akas/item")
valid_akas = []
if len(aka_elements) > 0:
    for aka_el in aka_elements:
        clean_aka = re.compile(' \(.*').sub('', aka_el.text)
        if not clean_aka in valid_akas:
            valid_akas.append(clean_aka)

if len(valid_akas) == 0:
    print('INFO: No se encontraron akas para "%s"' % movie.get_complete_title())
else:
    for aka in valid_akas:
        movie.title_akas.add(
            get_first_or_create_tag(
                TitleAka, title=aka
            )
        )
    movie.save()
"""



"""
print(dir(full_title_aka))
# Matches especiales: (World-wide, English title)

# https://regex101.com/r/0oNv7M/1
regex_countries = re.compile(r"\(([a-zA-Z0-9 ]+)\)")
match_countries = []
for m in regex_countries.finditer(full_title_aka):
    match_countries.append(m)

if len(match_countries) == 0:
    print(" * No encontramos el pais en '%s'" % full_title_aka)
    continue
elif len(match_countries) > 1:
    print(" * Encontramos varios paises en '%s'" % full_title_aka)

march_country = match_countries[0].group(1)

print(" - %s" % march_country)

if march_country in title_akas.keys():
    print(" * Ya tenemos el pais '%s' en title_akas." % march_country)
elif march_country == "Spain" or march_country in movie_countries:
    title_akas[march_country] = full_title_aka.replace(" %s" % match_countries[0].group(0), "")
"""