# Generated by Django 3.0.8 on 2020-07-10 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotAccessInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('chat_id', models.TextField(blank=True, null=True)),
                ('last_date', models.DateTimeField(blank=True, null=True)),
                ('first_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
