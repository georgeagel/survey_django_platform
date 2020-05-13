# Generated by Django 3.0.5 on 2020-04-26 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('is_published', models.BooleanField(verbose_name='Users can see it and answer it')),
                ('need_logged_user', models.BooleanField(verbose_name='Only authenticated users can see it and answer it')),
                ('display_by_question', models.BooleanField(verbose_name='Display by question')),
                ('template', models.CharField(blank=True, max_length=255, null=True, verbose_name='Template')),
            ],
            options={
                'verbose_name': 'survey',
                'verbose_name_plural': 'surveys',
            },
        ),
    ]
