# Generated by Django 3.1.4 on 2021-01-18 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_posts_imgurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='time',
            field=models.CharField(default='00:00', max_length=12),
        ),
    ]
