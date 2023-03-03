# dummy_data_generator

Features
* Any user can log in to the system with a username and password.
* Any logged-in user can create any number of data schemas to create datasets with fake data.
* Each such data schema has a name and a list of columns with names and specified data types.
* Users can build the data schema with any number of columns of any type described above.
* Each column also has its own name (which will be a column header in the CSV file).

Technology Stack:
* Python 3.11
* Django
* HTML
* Bootstrap
* CSS
* AJAX

```shell
git clone https://github.com/Pavilion4ik/dummy_data_generator.git
cd dummy_data_generator
python -m venv venv
source venv/scripts/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser #create user for tests
python manage.py runserver  #starts Django server
```

Check it online!
https://blin4ik.pythonanywhere.com

Admin-user credentials for web-site:

username: admin

password: qwerqaz.v