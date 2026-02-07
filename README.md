Gestion de Maintenance & Inventaire - EP Mostaganem

Django web application for managing equipment, maintenance requests, and technical interventions.

How to run the project on Linux:
```
1. Create virtual environment
python3 -m venv env

2. Activate virtual environment
source env/bin/activate

3. Install Django
pip install django

4. Install project dependencies
pip install -r requirements.txt

5. Apply migrations
python manage.py makemigrations
python manage.py migrate

6. Create admin user
python manage.py createsuperuser

7. Run the server
python manage.py runserver

8. Open in browser
http://127.0.0.1:8000/

9. Admin panel
http://127.0.0.1:8000/admin/
