from django import forms
from django.forms.utils import ErrorDict, ErrorList
from django.views.generic.list import ListView


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
        a = self.model_cls.objects.select_related().filter(**search_filter)
        return a
    def get_filter_dict(self):
        filter_dict = {}
        for field in self.fields:
            if field in self.data and self.data[field]:
                filter_dict["{0}__contains".format(field)] = self.data[field]

        return filter_dict


class ModelSearchViewBase(ListView):
    KEY_SEARCH_POST = 'search-post'

    template_name = None
    model = None
    form_class = None
    paginate_by = 5

    def get_queryset(self):

        queryset = []
        if self.request.session.has_key(self.KEY_SEARCH_POST):
            queryset = self._get_input_filter_queryset()

        return queryset

    def post(self, request, *args, **kwargs):
        self.request.session[self.KEY_SEARCH_POST] = self.request.POST
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self._is_search_post_info_del():
            del self.request.session[self.KEY_SEARCH_POST]
        return super().get(request, *args, **kwargs)

    def _is_search_post_info_del(self):
        if self.request.method == 'GET' \
                and "page" not in self.request.GET \
                and self.request.session.has_key(self.KEY_SEARCH_POST):

            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            search_form = self.form_class(self.request.POST)
        else:
            search_form = self.form_class()

        ctx['form'] = search_form
        return ctx

    def _get_input_filter_queryset(self):
        search_form = self.form_class(self.request.session[self.KEY_SEARCH_POST])
        return search_form.get_filter_queryset()





