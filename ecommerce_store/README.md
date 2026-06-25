# CodeAlpha_EcommerceStore

A simple e-commerce web application built with **Django** and **MySQL**, created for the CodeAlpha Full Stack Development Internship — Task 1.

## Features

- Product listing and detail pages
- User registration and login (Django's built-in auth)
- Shopping cart (add, increase/decrease quantity, remove)
- Order checkout and order history
- Admin panel for managing products and orders

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS (Django templates)
- **Database:** MySQL (via XAMPP)

## Setup Instructions (VS Code + XAMPP)

### 1. Start MySQL in XAMPP

Open the XAMPP Control Panel and click **Start** next to MySQL.

### 2. Create the database

Open `http://localhost/phpmyadmin` in your browser and create a new database named:

```
codealpha_ecommerce
```

(Just create the empty database — Django will create the tables for you.)

### 3. Open the project folder in VS Code

```
File > Open Folder > select the ecommerce_store folder
```

### 4. Create a virtual environment and install dependencies

Open a terminal in VS Code (`` Ctrl+` ``):

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
```

> **Note:** `mysqlclient` sometimes fails to install on Windows with a plain `pip install`. If it errors out, download the matching `.whl` file from
> https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient (or use `pip install mysqlclient --only-binary :all:`) and try again.

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create an admin account

```bash
python manage.py createsuperuser
```

### 7. Run the server

```bash
python manage.py runserver
```

Visit:
- **Store:** http://127.0.0.1:8000/
- **Admin panel:** http://127.0.0.1:8000/admin/

### 8. Add some products

Log in to the admin panel and add a few products (name, price, stock, image) so the homepage isn't empty.

## Project Structure

```
ecommerce_store/
├── ecommerce_store/      # Project settings, URLs
├── store/                # Main app: models, views, templates
│   ├── models.py         # Product, Cart, CartItem, Order, OrderItem
│   ├── views.py          # All page logic
│   ├── urls.py           # App routes
│   └── templates/store/  # HTML templates
├── static/css/style.css  # Styling
├── media/products/       # Uploaded product images
└── manage.py
```

## Notes

- Built as part of the **CodeAlpha Full Stack Development Internship**.
- Database credentials in `settings.py` assume XAMPP's default MySQL setup (`root` user, no password). Change them if your local setup differs.
