# Generated by Django 4.2 on 2023-09-12 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_data', '0006_alter_filedata_file_alter_filedata_file_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filedata',
            name='file_name',
        ),
        migrations.AddField(
            model_name='filedata',
            name='filename',
            field=models.CharField(blank=True, max_length=123, unique=True, verbose_name='Имя файла'),
        ),
    ]
