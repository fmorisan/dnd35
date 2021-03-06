# Generated by Django 3.0.4 on 2020-03-11 01:16

from django.db import migrations
import json


def migrate_forwards(apps, schema):
    Feat = apps.get_model('feat_modeling', 'Feat')

    for feat in Feat.objects.all():
        prerequisites = json.loads(feat.prerequisite_names)
        feats = (
            Feat.objects.filter(name__in=prerequisites)
            | Feat.objects.filter(name=feat.parent_name)
        )
        if feats.exists():
            feat.prerequisites.set(feats)
            feat.save()


class Migration(migrations.Migration):

    dependencies = [
        ('feat_modeling', '0003_feat_prerequisites'),
    ]

    operations = [
        migrations.RunPython(
            migrate_forwards,
            migrations.RunPython.noop
        )
    ]
