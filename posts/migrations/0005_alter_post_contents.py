# Generated by Django 4.2 on 2023-04-27 12:46

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_postcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='contents',
            field=tinymce.models.HTMLField(),
        ),
    ]
