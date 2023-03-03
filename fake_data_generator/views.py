from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin
from extra_views import UpdateWithInlinesView, CreateWithInlinesView
from sweetify.views import SweetifySuccessMixin
from fake_data_generator.forms import SchemaForm, ColumnInlineForm, DataForm
from fake_data_generator.generator import generate_csv
from fake_data_generator.models import Schema, Data


class Login(LoginView):
    template_name = "registration/login.html"
    success_url = reverse_lazy("fakedata:schema-list")


class SchemasListView(LoginRequiredMixin, generic.ListView):
    model = Schema
    queryset = Schema.objects.all()
    paginate_by = 7
    template_name = "fake_data/schemas_list.html"


class SchemaCreateView(LoginRequiredMixin, SweetifySuccessMixin, CreateWithInlinesView):
    model = Schema
    form_class = SchemaForm
    inlines = [
        ColumnInlineForm,
    ]
    success_url = reverse_lazy("fake_data_generator:schemas-list")
    sweetify_success_message = "Schema was created successfully."
    template_name = "fake_data/schema_form.html"

    def get_success_url(self):
        if "action" in self.request.POST:
            if self.request.POST["action"] == "add_column":
                return reverse_lazy(
                    "fake_data_generator:schema-edit", kwargs={"pk": self.object.id}
                )
            if self.request.POST["action"] == "submit":
                return reverse_lazy("fake_data_generator:schemas-list")
        return reverse_lazy("fake_data_generator:schemas-list")


class SchemaEditView(LoginRequiredMixin, SweetifySuccessMixin, UpdateWithInlinesView):
    model = Schema
    form_class = SchemaForm
    inlines = [
        ColumnInlineForm,
    ]
    template_name = "fake_data/schema_form.html"
    success_message = "Added"

    def get_success_url(self):
        if "action" in self.request.POST:
            if self.request.POST["action"] == "add_column":
                return reverse_lazy(
                    "fake_data_generator:schema-edit", kwargs={"pk": self.object.pk}
                )
            return reverse_lazy("fakedata:schemas-list")


class SchemaDeleteView(LoginRequiredMixin, SweetifySuccessMixin, generic.DeleteView):
    model = Schema
    template_name = "fake_data/fakeschema_confirm_delete.html"
    success_url = reverse_lazy("fake_data_generator:schema-list")
    success_message = "Schema was delete"


def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


class DataSetsView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Schema
    form_class = DataForm
    template_name = "fake_data/datasets.html"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(DataSetsView, self).get_context_data(**kwargs)
        schema = self.get_object()
        context["column"] = schema.column.all()
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        schema = self.get_object()
        dataset = Data.objects.create(schema=schema, rows=int(request.POST["rows"]))
        if is_ajax(request):
            generate_csv(dataset)
            link = Data.objects.filter(schema=schema).first().download_link
            html = render_to_string(
                "fake_data/table.html",
                context={"fakeschema": schema, "download_link": link},
                request=request,
            )
            return JsonResponse(
                {
                    "msg": html,
                    "link": link,
                }
            )
        return HttpResponseRedirect(
            reverse_lazy("fake_data_generator:schema-detail", kwargs={"pk": schema.pk})
        )
