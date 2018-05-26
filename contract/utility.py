from django import forms
from django.forms.utils import ErrorDict, ErrorList


class EmptyChoiceField(forms.ChoiceField):
    EMPTY_CHOICE_LABEL = "選択してください"

    def __init__(self, choices=(), empty_label=EMPTY_CHOICE_LABEL, required=True, widget=None, label=None,
                 initial=None, help_text=None, **kwargs):

        # prepend an empty label if it exists (and field is not required!)
        choices = tuple([('', empty_label)] + list(choices))

        super().__init__(choices=choices, required=required, widget=widget, label=label,
                         initial=initial, help_text=help_text, **kwargs)


class ModelSearchFormBase(forms.Form):
    model_cls = None

    def get_filter_queryset(self):
        search_filter = self.get_filter_dict()
        return self.model_cls.objects.filter(**search_filter)

    def get_filter_dict(self):
        filter_dict = {}
        for field in self.fields:
            if self.data[field]:
                filter_dict["{0}__contains".format(field)] = self.data[field]

        return filter_dict




