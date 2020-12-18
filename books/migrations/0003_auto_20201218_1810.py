# Generated by Django 3.1.4 on 2020-12-18 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_file_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='title',
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='files/', verbose_name='Filename'),
        ),
    ]
