# Generated by Django 4.0.4 on 2022-04-20 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0002_rename_collectionmodel_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='file',
            field=models.FileField(default='', upload_to='collection_csv'),
            preserve_default=False,
        ),
    ]
