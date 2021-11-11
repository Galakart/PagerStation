# Generated by Django 3.2.9 on 2021-11-10 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DirectMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capcode', models.CharField(max_length=7)),
                ('freq', models.CharField(max_length=9)),
                ('fbit', models.IntegerField()),
                ('message', models.TextField(max_length=1500)),
                ('is_sent', models.BooleanField(default=False)),
            ],
        ),
    ]
