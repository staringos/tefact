from extensions import ma
from .models import DataSource


class DataSourceSchema(ma.ModelSchema):

    class Meta:
        model = DataSource
        exclude = ('username', 'password')
