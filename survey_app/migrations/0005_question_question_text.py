# Generated by Django 3.0.5 on 2020-05-12 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_app', '0004_survey_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_text',
            field=models.CharField(default=0, max_length=300, verbose_name='header'),
            preserve_default=False,
        ),
    ]
