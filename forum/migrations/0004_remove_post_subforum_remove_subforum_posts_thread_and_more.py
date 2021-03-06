# Generated by Django 4.0.4 on 2022-04-12 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import forum.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0003_rename_pub_date_post_publication_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='subforum',
        ),
        migrations.RemoveField(
            model_name='subforum',
            name='posts',
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=models.SET(forum.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('subforum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.subforum')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='forum.thread'),
            preserve_default=False,
        ),
    ]
