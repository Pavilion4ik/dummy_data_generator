from django.contrib.auth.views import LoginView
from django.urls import path

from fake_data_generator.views import (
    SchemasListView,
    SchemaCreateView,
    SchemaEditView,
    DataSetsView,
    SchemaDeleteView,
)

urlpatterns = [
    path("schemas/", SchemasListView.as_view(), name="schemas-list"),
    path("schemas/create/", SchemaCreateView.as_view(), name="schema-create"),
    path("schemas/edit/<int:pk>/", SchemaEditView.as_view(), name="schema-edit"),
    path("schemas/<int:pk>/", DataSetsView.as_view(), name="schema-detail"),
    path("schemas/<int:pk>/delete/", SchemaDeleteView.as_view(), name="schema-delete"),
    path("login/", LoginView.as_view(), name="login"),
]

app_name = "fake_data_generator"
