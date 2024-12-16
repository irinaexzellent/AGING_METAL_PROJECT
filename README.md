# ABOUT PROJECT

The project is under development.
Implemented in the project: 
1. dynamic creation of tables and output using DataTables
2. dynamic generation of data addition forms.

# TECHNOLOGIES USED

Python, Django, jQuery, HTML, CSS

# How to start a project:

Clone the repository:

```
git clone https://github.com/irinaexzellent/AGING_METAL_PROJECT
```

Create and activate a virtual environment:

```
python3 -m venv env
```
```
source venv/Scripts/activate
```

```
cd AGING_METAL_PROJECT
```

Install dependencies from file requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

```
cd aging_metal
python manage.py makemigrations
python manage.py migrate
```
Add test data to the database:
```
Path to the database: AGING_METAL_PROJECT/aging_metal/db.sqlite3
```
```
Path to the test data: AGING_METAL_PROJECT/aging_metal/test_data.sql
```
```
python manage.py runserver
```
The project is available: http://127.0.0.1:8000/

# Author

* **Irina Ikonnikova** -  [IrinaIkonnikova](https://github.com/irinaexzellent)
