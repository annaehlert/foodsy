# Generated by Django 3.0.8 on 2020-07-17 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0015_auto_20200717_0825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='post',
        ),
        migrations.AddField(
            model_name='category',
            name='post',
            field=models.ManyToManyField(related_name='post', to='general.Post'),
        ),
    ]
