from typing import Dict

from oarepo_model_builder.datatypes import DataTypeComponent
from langcodes.language_lists import CLDR_LANGUAGES
from oarepo_model_builder_ui.config import UI_ITEMS

from marshmallow import fields as ma_fields
import marshmallow as ma


class UIPropertySchema(ma.Schema):

    def load(
        self,
        data,
        *,
        many=None,
        partial=None,
        unknown=None,
    ):
        # remove UI_ITEMS from data
        if many:
            x: Dict
            ui_items = [self.remove_ui_items(x) for x in data]
        else:
            ui_items = self.remove_ui_items(data)
        # perform normal validation
        ret = super().load(data, many=many, partial=partial, unknown=unknown)
        # add UI_ITEMS to data
        if many:
            for ui, d in zip(ui_items, ret):
                self.add_ui_items(d, ui)
        else:
            self.add_ui_items(ret, ui_items)
        return ret

    def remove_ui_items(self, data):
        if not data:
            return {}
        ui_items = {}
        for k in list(data.keys()):
            split_key = k.split('.')
            if len(split_key) < 2:
                continue
            if split_key[0] in UI_ITEMS or split_key[0] == 'enum':
                ui_items[k] = data.pop(k)
        return ui_items

    def add_ui_items(self, data, ui_items):
        data.update(ui_items)

#
# def create_ui_property_schema():
#     return UIPropertyValidator
#
#     # TODO: inefficient as it adds cca 300 fields on schema but ok for now
#     fields = {}
#     for fld in UI_ITEMS:
#         for lang in ["key", *CLDR_LANGUAGES]:
#             fields[f"{fld}.{lang}"] = ma_fields.String(required=False, data_key=f"{fld}.{lang}", attribute=f"{fld}.{lang}")
#     fields["i18n.key"] = ma_fields.String(required=False)
#     return type("UIPropertyValidator", (ma.Schema,), fields)
#
#
# UIPropertySchema = create_ui_property_schema()



class DataTypeUIComponent(DataTypeComponent):
    class ModelSchema(UIPropertySchema):
        pass


from .model import UIModelComponent
components = [
    DataTypeUIComponent,
    UIModelComponent
]