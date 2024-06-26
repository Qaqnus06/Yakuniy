# Generated by Django 5.0.4 on 2024-05-03 04:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_post_likes_follow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='follow',
            new_name='follower',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='user',
        ),
        migrations.AddField(
            model_name='follow',
            name='followed',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='follow',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
