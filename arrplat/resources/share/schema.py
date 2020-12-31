from extensions import ma
from .models import SharePage, ShareType
from marshmallow_enum import EnumField


class SharePageSchema(ma.ModelSchema):
    type = EnumField(ShareType, by_value=True)

    class Meta:
        model = SharePage
