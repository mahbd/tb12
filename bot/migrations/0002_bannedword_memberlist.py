# Generated by Django 3.0.8 on 2020-07-10 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannedWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MemberList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_name', models.TextField(blank=True, null=True)),
                ('member_id', models.TextField(blank=True, null=True)),
                ('user_name', models.TextField(blank=True, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.BotAccessInfo')),
            ],
        ),
    ]