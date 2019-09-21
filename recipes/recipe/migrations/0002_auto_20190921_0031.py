# Generated by Django 2.2.4 on 2019-09-21 00:31

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0003_country'),
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.UUIDField(blank=True, default=None, null=True)),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='meal_time',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='recipeingredient',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='recipeingredient',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='recipeingredient',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='procedure',
            name='steps',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=5000), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipe',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='authentication.Country'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='meal_culture',
            field=models.CharField(default='Native', max_length=249),
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='ingredients_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=5000), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=249, unique=True),
        ),
        migrations.AlterField(
            model_name='mealtype',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='procedure',
            name='body',
            field=models.TextField(blank=True, max_length=15000, null=True),
        ),
        migrations.AlterField(
            model_name='procedure',
            name='recipe',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='recipe.Recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=500), blank=True, null=True, size=8),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='meal_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='recipe.MealType'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='published_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='recipe.Ingredient'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='recipe.Recipe'),
        ),
    ]