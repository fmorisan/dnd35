# Generated by Django 3.0.4 on 2020-03-11 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feat_modeling', '0004_auto_20200311_0116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
    ]
