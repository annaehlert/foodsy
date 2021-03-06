# Generated by Django 3.0.8 on 2020-07-20 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0018_auto_20200717_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(max_length=20, null=True, verbose_name='kategoria'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(related_name='categories', to='general.Category', verbose_name='kategoria'),
        ),
        migrations.CreateModel(
            name='Rewrite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Profile')),
            ],
        ),
    ]
