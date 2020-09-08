# Generated by Django 3.1 on 2020-09-08 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GenreTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título (Internacional)')),
                ('title_original', models.CharField(blank=True, max_length=200, null=True, verbose_name='Título (Original)')),
                ('title_preferred', models.CharField(blank=True, max_length=200, null=True, verbose_name='Título (Idioma preferido)')),
                ('imdb_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='IMDB ID')),
                ('kind', models.CharField(choices=[('movie', 'Película'), ('tv series', 'Serie de television')], default='movie', max_length=20, verbose_name='Clase de pélicula')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='Resumen')),
                ('poster_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Cartel (URL)')),
                ('poster_thumbnail_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Cartel en miniatura (URL)')),
                ('year', models.IntegerField(blank=True, null=True, verbose_name='Año')),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Puntuación')),
                ('is_scraped', models.BooleanField(default=False, verbose_name='Scrapeado')),
                ('imdb_raw_data', models.TextField(blank=True, null=True, verbose_name='RAW DATA IMDB')),
                ('genres', models.ManyToManyField(to='data.GenreTag')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('canonical_name', models.CharField(max_length=200, verbose_name='Nombre (Canónico)')),
                ('imdb_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='IMDB ID')),
                ('avatar_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Foto (URL)')),
                ('avatar_thumbnail_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Foto en miniatura (URL)')),
                ('is_director', models.BooleanField(default=False, verbose_name='Director')),
                ('is_writer', models.BooleanField(default=False, verbose_name='Escritor')),
                ('is_actor', models.BooleanField(default=False, verbose_name='Actor')),
                ('is_scraped', models.BooleanField(default=False, verbose_name='Scrapeado')),
                ('imdb_raw_data', models.TextField(blank=True, null=True, verbose_name='RAW DATA IMDB')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TitleAka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MovieStorageType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_original', models.BooleanField(default=True, verbose_name='Original')),
                ('storage_type', models.CharField(choices=[('hard-drive', 'Disco duro'), ('net-share', 'Compartido de red'), ('dvd', 'DVD'), ('bluray', 'BLURAY'), ('ultra-bluray', 'ULTRA BLURAY'), ('vhs', 'VHS')], default='dvd', max_length=20, verbose_name='Tipo de almacenamiento')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre del almacenamiento')),
                ('path', models.CharField(blank=True, max_length=512, null=True, verbose_name='Ubicación')),
                ('media_format', models.CharField(choices=[('AVI', 'AVI'), ('BLURAY', 'BLURAY'), ('BLURAY-ISO', 'BLURAY-ISO'), ('DVD', 'DVD'), ('DVD-ISO', 'DVD-ISO'), ('ISO', 'ISO'), ('M2TS', 'M2TS'), ('M4V', 'M4V'), ('MKV', 'MKV'), ('MP4', 'MP4'), ('ULTRA-BLURAY', 'ULTRA-BLURAY')], default='DVD', max_length=20, verbose_name='Formato')),
                ('resolution', models.CharField(blank=True, max_length=20, null=True, verbose_name='Resolución')),
                ('version', models.CharField(blank=True, max_length=512, null=True, verbose_name='Versión')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.movie', verbose_name='pelicula')),
            ],
        ),
        migrations.CreateModel(
            name='MoviePerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('director', 'Director'), ('writer', 'Guionista'), ('actor', 'Actor/Actriz')], default='director', max_length=20, verbose_name='Rol')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.movie', verbose_name='pelicula')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.person', verbose_name='participante')),
            ],
            options={
                'verbose_name': 'participante',
                'verbose_name_plural': 'participantes',
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='tags',
            field=models.ManyToManyField(to='data.Tag'),
        ),
        migrations.AddField(
            model_name='movie',
            name='title_akas',
            field=models.ManyToManyField(to='data.TitleAka'),
        ),
    ]
