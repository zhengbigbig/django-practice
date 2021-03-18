# Generated by Django 3.2b1 on 2021-03-17 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drf', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password_hash', models.CharField(db_column='password', max_length=20)),
                ('age', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'user_drf',
            },
        ),
    ]