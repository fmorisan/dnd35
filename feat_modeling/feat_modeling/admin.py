from django.contrib import admin

from feat_modeling.models import (
    Feat,
    Skill
)
from feat_modeling.models.feat import (
    NumericalFeatEffect,
    NumericalFeatRequisite
)

admin.site.register(Feat)
admin.site.register(Skill)
admin.site.register(NumericalFeatEffect)
admin.site.register(NumericalFeatRequisite)
