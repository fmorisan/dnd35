from django.db import models
from django.contrib.contenttypes.models import (
    ContentType
)


class Feat(models.Model):
    class MODES:
        NORMAL = 0
        STACKABLE = 1
        REPEATABLE = 2

    class TYPES:
        GENERAL = 0
        METAMAGIC = 1
        SPECIAL = 2
        OBJECT_CREATION = 3

    MODE_CHOICES = (
        (MODES.NORMAL, 'normal'),
        (MODES.STACKABLE, 'stackable'),
        (MODES.REPEATABLE, 'repeatable')
    )

    TYPE_CHOICES = (
        (TYPES.GENERAL, 'general'),
        (TYPES.METAMAGIC, 'metamagic'),
        (TYPES.SPECIAL, 'special'),
        (TYPES.OBJECT_CREATION, 'object-creation')
    )

    feat_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=120)
    mode = models.IntegerField(
        choices=MODE_CHOICES
    )
    feat_type = models.IntegerField(
        choices=TYPE_CHOICES
    )
    benefit = models.TextField(
        max_length=500
    )
    parent_name = models.CharField(
        max_length=120,
        blank=True
    )
    prerequisites = models.ManyToManyField(
        'Feat',
        related_name='required_by',
        blank=True
    )
    prerequisite_names = models.CharField(
        max_length=700
    )
    effects = models.ManyToManyField(
        'NumericalFeatEffect',
        blank=True
    )
    requisites = models.ManyToManyField(
        'NumericalFeatRequisite',
        blank=True
    )

    def __str__(self):
        return f"Feat <{self.name}>"


class NumericalFeatEffect(models.Model):
    modifier = models.IntegerField()
    modify = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    modify_item_id = models.IntegerField()

    @property
    def modified_stat(self):
        return self.modify.get_object_for_this_type(id=self.modify_item_id)

    def __str__(self):
        return (
            f"NumericalFeatEffect: <{self.modifier} to {self.modified_stat}>"
        )


class NumericalFeatRequisite(models.Model):
    required_value = models.IntegerField
    required = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    required_item_id = models.IntegerField()

    @property
    def required_stat(self):
        return self.modify.get_object_for_this_type(id=self.required_item_id)

    def __str__(self):
        return (
            f"NumericalFeatEffect: <{self.required_value} {self.required_stat}>"  # NOQA
        )
