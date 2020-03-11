from django.db import models


class Skill(models.Model):
    class ATTRIBUTES:
        STRENGTH = 'str'
        DEXTERITY = 'dex'
        CONSTITUTION = 'con'
        INTELLIGENCE = 'int'
        WISDOM = 'wis'
        CHARISMA = 'cha'

    class ARMOR_PENALTY:
        NONE = 0
        NORMAL = 1
        WEIGHT = 2

    GOVERNING_ATTRIBUTE_CHOICES = (
        (ATTRIBUTES.STRENGTH, ATTRIBUTES.STRENGTH),
        (ATTRIBUTES.DEXTERITY, ATTRIBUTES.DEXTERITY),
        (ATTRIBUTES.CONSTITUTION, ATTRIBUTES.CONSTITUTION),
        (ATTRIBUTES.INTELLIGENCE, ATTRIBUTES.INTELLIGENCE),
        (ATTRIBUTES.WISDOM, ATTRIBUTES.WISDOM),
        (ATTRIBUTES.CHARISMA, ATTRIBUTES.CHARISMA)
    )

    ARMOR_PENALTY_CHOICES = (
        (ARMOR_PENALTY.NONE, "no"),
        (ARMOR_PENALTY.NORMAL, "normal"),
        (ARMOR_PENALTY.WEIGHT, "weight")
    )

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    trained_only = models.BooleanField(default=True)
    governing_attr = models.CharField(
        max_length=3,
        choices=GOVERNING_ATTRIBUTE_CHOICES
    )
    armor_penalty = models.IntegerField(
        choices=ARMOR_PENALTY_CHOICES
    )

    def __str__(self):
        return f"Skill: <{self.name}> ({self.governing_attr})"


class Attribute(models.Model):
    name = models.CharField(max_length=30)
