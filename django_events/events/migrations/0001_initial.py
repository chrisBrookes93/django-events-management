# Generated by Django 3.0.7 on 2020-06-26 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField(default='')),
                ('date_time', models.DateTimeField(help_text='Format: YYYY-MM-DD HH:MM:SS')),
            ],
        ),
    ]
