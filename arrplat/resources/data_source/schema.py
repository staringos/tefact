from extensions import ma
from .models import DataSource, DataSourceType, DataSourceStatus
from marshmallow_enum import EnumField


class DataSourceSchema(ma.ModelSchema):
    type = EnumField(DataSourceType, by_value=True)
    status = EnumField(DataSourceStatus, by_value=True)

    class Meta:
        model = DataSource
        exclude = ('username', 'password')
