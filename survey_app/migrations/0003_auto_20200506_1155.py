# Generated by Django 3.0.5 on 2020-05-06 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey_app', '0002_survey'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Content')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400, verbose_name='Name')),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='Display order')),
                ('description', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.RemoveField(
            model_name='question',
            name='pub_date',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_text',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='is_published',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='template',
        ),
        migrations.AddField(
            model_name='question',
            name='choices',
            field=models.TextField(blank=True, help_text="The choices field is only used if the question type\nif the question type is 'radio', 'select', or\n'select multiple' provide a comma-separated list of\noptions for this question .", null=True, verbose_name='Choices'),
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='survey_app.Survey', verbose_name='Survey'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('text', 'text (multiple line)'), ('short-text', 'short text (one line)'), ('radio', 'radio'), ('select', 'select'), ('select-multiple', 'Select Multiple'), ('select_image', 'Select Image'), ('integer', 'integer'), ('float', 'float'), ('date', 'date')], default='text', max_length=200, verbose_name='Type'),
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.AddField(
            model_name='category',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='survey_app.Survey', verbose_name='Survey'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='survey_app.Question', verbose_name='Question'),
        ),
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions', to='survey_app.Category', verbose_name='Category'),
        ),
    ]
