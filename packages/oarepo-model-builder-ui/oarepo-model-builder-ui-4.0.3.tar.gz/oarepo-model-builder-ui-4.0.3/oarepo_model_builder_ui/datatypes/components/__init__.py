from oarepo_model_builder.datatypes import DataTypeComponent
from langcodes.language_lists import CLDR_LANGUAGES
from oarepo_model_builder_ui.config import UI_ITEMS

from marshmallow import fields as ma_fields
import marshmallow as ma

def create_ui_property_schema():
    # TODO: inefficient as it adds cca 300 fields on schema but ok for now
    fields = {}
    for fld in UI_ITEMS:
        for lang in ["key", *CLDR_LANGUAGES]:
            fields[f"{fld}.{lang}"] = ma_fields.String(required=False, data_key=f"{fld}.{lang}", attribute=f"{fld}.{lang}")
    fields["i18n.key"] = ma_fields.String(required=False)
    return type("UIPropertyValidator", (ma.Schema,), fields)


UIPropertySchema = create_ui_property_schema()



class DataTypeUIComponent(DataTypeComponent):
    class ModelSchema(UIPropertySchema):
        pass


from .model import UIModelComponent
components = [
    DataTypeUIComponent,
    UIModelComponent
]