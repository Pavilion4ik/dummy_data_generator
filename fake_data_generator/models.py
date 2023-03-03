from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator
from django.db import models


class User(AbstractUser):
    ...


class Schema(models.Model):
    class Quotes(models.TextChoices):
        SINGLE_QUOTE = "'", "Single-quote(')"
        DOUBLE_QUOTE = '"', 'Double-quote(")'

    class Separators(models.TextChoices):
        COMMA = ",", "Comma(,)"
        SEMICOLON = ";", "Semicolon(;)"
        TAB = "\t", "Tab(\t)"
        SPACE = " ", "Space( )"
        PIPE = "|", "Pipe(|)"

    name = models.CharField(max_length=255)
    quote = models.CharField(
        choices=Quotes.choices, default=Quotes.DOUBLE_QUOTE, max_length=25
    )
    separator = models.CharField(
        choices=Separators.choices, default=Separators.COMMA, max_length=25
    )
    created_at = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return (
            f"The actual schema has:"
            f"name: {self.name},"
            f"quotes: {self.quote},"
            f"separator: {self.separator}"
        )

    class Meta:
        ordering = ["-created_at"]


class Column(models.Model):
    class Types(models.TextChoices):
        FULL_NAME = "Full_name", "Full name (a combination of first name and last name)"
        JOB = "Job", "Job"
        EMAIL = "Email", "Email"
        DOMAIN = "Domain", "Domain name"
        PHONE = "Phone", "Phone number"
        COMPANY = "Company", "Company name"
        TEXT = "Text", "Text (with a specified range for a number of sentences)"
        AGE = "Age", "Age (with specified range)"
        ADDRESS = "Address", "Address"
        DATE = "Date", "Date"

    name = models.CharField(max_length=30)
    type = models.CharField(choices=Types.choices, max_length=20)
    order = models.PositiveIntegerField(default=0)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name="column")

    class Meta:
        ordering = ["order"]

    def clean(self):
        super(Column, self).clean()
        if not self.order:
            self.order = Column.objects.filter(schema=self.schema).count() + 1


class Data(models.Model):
    class Status(models.TextChoices):
        PROCESSING = 0, "Processing..."
        READY = 1, "Ready"

    schema = models.ForeignKey(
        Schema, on_delete=models.CASCADE, related_name="schema_data"
    )
    created_at = models.DateField(auto_now_add=True)
    status = models.IntegerField(choices=Status.choices, default=0)
    rows = models.PositiveIntegerField(null=False)
    download_link = models.URLField(
        max_length=200, validators=[URLValidator(schemes=["http", "https"])]
    )
