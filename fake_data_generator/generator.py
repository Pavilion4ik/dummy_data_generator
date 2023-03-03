from django.conf import settings
from faker import Faker
import csv

from fake_data_generator.models import Data, Schema, Column


def generate_fake_data(data_type: int):
    fake = Faker()
    data = {
        "Full_name": fake.name(),
        "Job": fake.job(),
        "Email": fake.email(),
        "Domain": fake.domain_name(),
        "Phone": fake.phone_number(),
        "Company": fake.company(),
        "Text": fake.sentences(),
        "Age": fake.random_int(),
        "Address": fake.address(),
        "Date": fake.date(),
    }
    return data[data_type]


def generate_csv(dataset: Data):
    schema = Schema.objects.get(id=dataset.schema.id)
    columns = Column.objects.filter(schema=schema).order_by("order").values()

    quote = schema.quote
    separator = schema.separator
    print(quote)

    csv.register_dialect(
        "new_dialect",
        delimiter=separator,
        quotechar=quote[0],
        quoting=csv.QUOTE_ALL,
    )

    fieldnames = [column["name"] for column in columns]

    with open(
        settings.MEDIA_ROOT + f"/schema_{schema.name}_dataset{dataset.id}.csv",
        "w",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, dialect="new_dialect")
        writer.writeheader()
        for i in range(dataset.rows):
            row = {}
            for column in columns:
                value = generate_fake_data(column["type"])
                row[column["name"]] = value

            writer.writerow(row)
        dataset.status = 1
        dataset.download_link = (
            f"{settings.MEDIA_URL}schema_{schema.name}_dataset{dataset.id}.csv"
        )
        dataset.save()
