import json
from django.core.management.base import (
    BaseCommand,
    CommandError
)

from feat_modeling.models import Skill


ATTRIBUTES = {
    "Carisma": Skill.ATTRIBUTES.CHARISMA,
    "Constitución": Skill.ATTRIBUTES.CONSTITUTION,
    "Destreza": Skill.ATTRIBUTES.DEXTERITY,
    "Fuerza": Skill.ATTRIBUTES.STRENGTH,
    "Inteligencia": Skill.ATTRIBUTES.INTELLIGENCE,
    "Sabiduría": Skill.ATTRIBUTES.WISDOM
}

ARMOR_PENALTIES = {
    None: Skill.ARMOR_PENALTY.NONE,
    "normal": Skill.ARMOR_PENALTY.NORMAL,
    "weight": Skill.ARMOR_PENALTY.WEIGHT
}


class Command(BaseCommand):
    help = "Ingest a feat json file"

    def add_arguments(self, parser):
        parser.add_argument("file", help="File to ingest")

    def ingest_skill(self, skill_data):
        Skill.objects.create(
            name=skill_data['name'],
            governing_attr=ATTRIBUTES[skill_data['ability']],
            description=skill_data['description'],
            armor_penalty=ARMOR_PENALTIES[skill_data['armor-penalty']],
            trained_only=skill_data['requires_training']
        )

    def handle(self, file, *args, **kwargs):
        try:
            with open(file, 'r') as f:
                self.ingest_skill(json.load(f))
        except Exception as exc:
            print(f"Could not ingest {file}")
            raise CommandError(exc)
