# Generated by Django 2.1.5 on 2019-02-15 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InstabotMV', '0004_auto_20190215_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lastlogin',
            name='cred',
            field=models.ForeignKey(on_delete=None, to='InstabotMV.Creds'),
        ),
    ]