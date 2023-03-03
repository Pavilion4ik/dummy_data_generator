from django import forms
from extra_views import InlineFormSetFactory
from fake_data_generator.models import Schema, Column, Data


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = "__all__"


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = "__all__"


class ColumnInlineForm(InlineFormSetFactory):
    model = Column
    form_class = ColumnForm

    fields = "__all__"

    factory_kwargs = {
        "extra": 1,
        "max_num": None,
        "can_order": False,
        "can_delete": True,
    }


class DataForm(forms.ModelForm):
    rows = forms.IntegerField(
        label="", widget=forms.NumberInput(attrs={"placeholder": "Number of rows"})
    )

    class Meta:
        model = Data
        fields = ("rows",)
