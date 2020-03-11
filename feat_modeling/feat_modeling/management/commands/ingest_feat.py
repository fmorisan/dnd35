import json
from django.core.management.base import (
    BaseCommand,
    CommandError
)

from feat_modeling.models import Feat

MODE_TRANSLATION = {
    name: value for value, name in Feat.MODE_CHOICES
}

TYPE_TRANSLATION = {
    name: value for value, name in Feat.TYPE_CHOICES
}


class Command(BaseCommand):
    help = "Ingest a feat json file"

    def add_arguments(self, parser):
        parser.add_argument("file", help="File to ingest")

    def ingest_feat(self, feat_data):
        Feat.objects.create(
            name=feat_data['name'].strip(),
            feat_id=feat_data['id'],
            mode=MODE_TRANSLATION[feat_data["mode"]],
            feat_type=TYPE_TRANSLATION[feat_data["category"]],
            parent_name=feat_data['father'].strip(),
            benefit=feat_data['benefit'],
            prerequisite_names=json.dumps(feat_data['prerequisites'])
        )

    def handle(self, file, *args, **kwargs):
        try:
            with open(file, 'r') as f:
                self.ingest_feat(json.load(f))
        except Exception as exc:
            print(f"Could not ingest {file}")
            raise CommandError(exc)
