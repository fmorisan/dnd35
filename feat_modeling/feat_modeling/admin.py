import itertools
from django.contrib import admin
from django.contrib.contenttypes.models import (
    ContentType
)
from django import forms

from feat_modeling.models import (
    Feat,
    Skill,
    CharacterClass,
    Character
)
from feat_modeling.models.feat import (
    NumericalFeatEffect,
    NumericalFeatRequisite
)
from feat_modeling.models.character import (
    SkillContainer,
)


def get_modifiable_choices():
    return itertools.chain(
        (
            (None, None),
        ),
        (
            (f"{instance._meta.label_lower}|{instance.id}", instance)
            for instance in NumericalFeatEffect.modifiables()
        )
    )


class NumericalFeatEffectForm(forms.ModelForm):
    modifier = forms.IntegerField()
    modifies = forms.ChoiceField(
        choices=get_modifiable_choices(),
        required=True
    )

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def is_valid(self, *args, **kwargs):
        return super().is_valid(*args, **kwargs)

    def save(self, *args, **kwargs):
        affected, id = self.cleaned_data['modifies'].split("|")
        self.instance.modify = ContentType.objects.get_by_natural_key(*affected.split('.'))
        self.instance.modify_item_id = int(id)

        return super().save(*args, **kwargs)

    class Meta:
        model = NumericalFeatEffect
        fields = []


class NumericalFeatEffectInline(admin.TabularInline):
    model = NumericalFeatEffect
    form = NumericalFeatEffectForm


class NumericalFeatRequisiteInline(admin.TabularInline):
    model = NumericalFeatRequisite


class SkillContainerInline(admin.TabularInline):
    model = SkillContainer


class FeatAdmin(admin.ModelAdmin):
    inlines = [
        NumericalFeatEffectInline,
        NumericalFeatRequisiteInline
    ]


class CharacterAdmin(admin.ModelAdmin):
    inlines = [
        SkillContainerInline
    ]


admin.site.register(Feat, FeatAdmin)
admin.site.register(Skill)
admin.site.register(NumericalFeatEffect)
admin.site.register(NumericalFeatRequisite)
admin.site.register(Character, CharacterAdmin)
admin.site.register(CharacterClass)
