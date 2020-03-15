import math

from django.db import models
from feat_modeling.models import (
    Skill,
    Feat
)


class CharacterClass(models.Model):
    class ATTACK_CLASS:
        POOR = 1
        NORMAL = 2
        GREAT = 3

    ATTACK_CLASS_CHOICES = (
        (ATTACK_CLASS.POOR, 'poor'),
        (ATTACK_CLASS.NORMAL, 'normal'),
        (ATTACK_CLASS.GREAT, 'great')
    )

    name = models.CharField(max_length=120)
    attack_class = models.IntegerField(
        choices=ATTACK_CLASS_CHOICES
    )

    def __str__(self):
        return f"Class: <{self.name}>"


class Character(models.Model):
    ATTRIBUTES = Skill.ATTRIBUTES

    name = models.CharField(max_length=120)
    character_class = models.ForeignKey(
        CharacterClass,
        on_delete=models.CASCADE
    )
    character_level = models.IntegerField()
    skill_set = models.ManyToManyField(
        Skill,
        through='SkillContainer',
        through_fields=(
            'character',
            'skill_class',
        )
    )

    feats = models.ManyToManyField(
        Feat
    )

    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    charisma = models.IntegerField()

    def get_attribute_modifier(self, skill):
        attribute = {
            self.ATTRIBUTES.STRENGTH: self.strength,
            self.ATTRIBUTES.DEXTERITY: self.dexterity,
            self.ATTRIBUTES.CONSTITUTION: self.constitution,
            self.ATTRIBUTES.INTELLIGENCE: self.intelligence,
            self.ATTRIBUTES.WISDOM: self.wisdom,
            self.ATTRIBUTES.CHARISMA: self.charisma
        }[skill.skill_class.governing_attribute]
        return (attribute - 10) // 2

    def _get_skill(self, skill_name):
        return self.skill_set.get(name=skill_name)

    def get_skill_modifier(self, skill_name):
        skill = self._get_skill(skill_name)
        return skill.ranks + self.get_attribute_modifier(skill)

    def get_base_attack(self):
        return math.floor(
            [
                1,
                .75,
                .5
            ][self.character_class.attack_class] * self.character_level
        )

    def get_ranged_attack(self):
        return self.get_base_attack() + self.get_skill_modifier(self.ATTRIBUTES.DEXTERITY)

    def get_melee_attack(self):
        return self.get_base_attack() + self.get_skill_modifier(self.ATTRIBUTES.STRENGTH)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for skill in Skill.objects.all():
            self.skill_set.add(skill)


class SkillContainer(models.Model):
    skill_class = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
    )
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    ranks = models.IntegerField(default=0)
