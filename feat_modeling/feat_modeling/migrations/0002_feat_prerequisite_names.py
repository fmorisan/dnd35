# Generated by Django 3.0.4 on 2020-03-11 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feat_modeling', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feat',
            name='prerequisite_names',
            field=models.CharField(default='', max_length=700),
            preserve_default=False,
        ),
    ]
