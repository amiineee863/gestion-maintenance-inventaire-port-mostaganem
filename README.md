🚀 How to Run the Project (Local Setup on Linux)

1️⃣ Create virtual environment
python3 -m venv env

2️⃣ Activate virtual environment
source env/bin/activate

3️⃣ Install Django
pip install django

4️⃣ Install project dependencies
pip install -r requirements.txt

5️⃣ Apply migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create admin user (superuser)
python manage.py createsuperuser

7️⃣ Run the server
python manage.py runserver

8️⃣ Open in browser
http://127.0.0.1:8000/

9️⃣ Admin panel:
http://127.0.0.1:8000/admin/


