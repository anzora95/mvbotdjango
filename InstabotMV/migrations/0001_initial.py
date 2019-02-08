# Generated by Django 2.1.5 on 2019-02-08 20:41

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('insta_user', models.CharField(max_length=150)),
                ('insta_pass', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'AppUser',
                'verbose_name_plural': 'AppUsers',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BlackList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insta_black_list', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChildTag',
            fields=[
                ('tag_name', models.CharField(max_length=100)),
                ('hashtag_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insta_comment', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Creds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insta_user', models.CharField(max_length=150)),
                ('insta_pass', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cred',
                'verbose_name_plural': 'Creds',
            },
        ),
        migrations.CreateModel(
            name='Features',
            fields=[
                ('id_feature', models.IntegerField(primary_key=True, serialize=False)),
                ('feature_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='HashtagList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'HashtagList',
                'verbose_name_plural': 'HashtagLists',
            },
        ),
        migrations.CreateModel(
            name='LastLogin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cred', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstabotMV.Creds')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'lastLogin',
                'verbose_name_plural': 'lastLogin',
            },
        ),
        migrations.CreateModel(
            name='List_Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insta_tag', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstabotMV.HashtagList')),
            ],
            options={
                'verbose_name': 'List_Tag',
                'verbose_name_plural': 'List_Tags',
            },
        ),
        migrations.CreateModel(
            name='LocateList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insta_locate', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_id', models.CharField(max_length=300)),
                ('status', models.IntegerField()),
                ('datetime', models.TextField()),
                ('code', models.TextField()),
                ('owner_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('settings_name', models.TextField()),
                ('settings_val', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField()),
                ('tags', models.CharField(max_length=1000)),
                ('likemedia', models.BooleanField()),
                ('followuser', models.BooleanField()),
                ('dontlikemedia', models.BooleanField()),
                ('dontfollow', models.BooleanField()),
                ('randomlylike', models.BooleanField()),
                ('search', models.BooleanField()),
                ('antispamfilter', models.BooleanField()),
                ('custowordfilter', models.BooleanField()),
                ('creds', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstabotMV.Creds')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
        ),
        migrations.CreateModel(
            name='thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=1000)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstabotMV.Task')),
            ],
        ),
        migrations.CreateModel(
            name='Username',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=300)),
                ('username_id', models.CharField(max_length=300)),
                ('unfollow_count', models.IntegerField()),
                ('last_followed_time', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UsList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insta_us_name', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='childtag',
            name='dad_tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstabotMV.HashtagList'),
        ),
    ]
