# Generated by Django 4.2.6 on 2023-10-30 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_category_post_category_alter_authorprofile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
