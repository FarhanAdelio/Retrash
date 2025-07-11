# Generated by Django 5.1.4 on 2025-04-23 12:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('deskripsi', models.TextField(blank=True)),
                ('icon', models.CharField(default='fas fa-folder', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Kategori',
                'ordering': ['nama'],
            },
        ),
        migrations.CreateModel(
            name='Diskusi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('isi', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_solved', models.BooleanField(default=False)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('penulis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diskusi', to=settings.AUTH_USER_MODEL)),
                ('kategori', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diskusi', to='forum.kategori')),
            ],
            options={
                'verbose_name_plural': 'Diskusi',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Komentar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isi', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_solution', models.BooleanField(default=False)),
                ('diskusi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='komentar', to='forum.diskusi')),
                ('penulis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='komentar', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Komentar',
                'ordering': ['created_at'],
            },
        ),
    ]
