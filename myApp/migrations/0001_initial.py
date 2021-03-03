# Generated by Django 3.2b1 on 2021-03-02 02:28

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'publisher',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('sno', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('sname', models.CharField(max_length=100)),
                ('ssex', models.CharField(default='男', max_length=2, null=True)),
                ('sage', models.IntegerField(null=True)),
                ('sclass', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'student',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'users',
                'ordering': ['username'],
            },
            managers=[
                ('userManager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bname', models.CharField(blank=True, max_length=200, null=True)),
                ('publisher', models.ForeignKey(db_column='pid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='books', to='myApp.publisher')),
            ],
            options={
                'db_table': 'book',
            },
        ),
        migrations.CreateModel(
            name='Archives',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idcard', models.CharField(max_length=18, unique=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myApp.student')),
            ],
            options={
                'db_table': 'archives',
            },
        ),
    ]
