TableBook
TableBook is a web application built with Django that allows users to book tables at cafes and managers to manage their cafes and bookings.
It includes user and manager roles, booking validation rules, cafe management, and an admin panel.

Features
User Features:

Register as a user or manager

Browse available cafes

Book tables for specific date and time

View personal booking history

Cancel bookings (up to 1 hour before booking time)

Manager Features:

Add, edit, and manage owned cafes

View all bookings for their cafes

Filter bookings by Today, Upcoming, or Custom Date Range

See booking summaries and statistics

Admin Features:

Manage users and cafes via Django Admin panel

Other Features:

Local timezone adjustment for bookings

Success and error notifications

Mobile-friendly basic responsive design

Technology Stack
Backend: Django 5

Frontend: Django Templates, HTML5, CSS3, JavaScript

Database: PostgreSQL (or SQLite for development)

Authentication: Django built-in authentication system

Installation
Clone the repository

bash
Copy
Edit
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Create and activate a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # (Linux/macOS)
venv\Scripts\activate      # (Windows)
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Apply database migrations

bash
Copy
Edit
python manage.py migrate
Create a superuser (admin account)

bash
Copy
Edit
python manage.py createsuperuser
Run the development server

bash
Copy
Edit
python manage.py runserver
Access the app

User view: http://localhost:8000/

Admin panel: http://localhost:8000/admin/

Usage Notes
Booking rules:

Bookings can only be cancelled at least 1 hour before the booked time.

Double-booking the same time by the same user is prevented.

Cafe table availability decreases automatically after each booking.

Timezone:

All booking times are adjusted to the user's local browser timezone for clarity.

Admin access:

Only superusers can delete users and manage all data globally through the Django Admin panel.
