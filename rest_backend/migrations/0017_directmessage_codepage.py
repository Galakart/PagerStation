# Generated by Django 3.2.9 on 2021-12-03 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_backend', '0016_newschannel_newsmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='directmessage',
            name='codepage',
            field=models.PositiveSmallIntegerField(choices=[(1, 'lat'), (2, 'cyr'), (3, 'linguist')], default=2, verbose_name='Тип кодировки'),
            preserve_default=False,
        ),
    ]
