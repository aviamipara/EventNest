# EventNest - Premium Event Management System

**EventNest** is a comprehensive, full-stack web application designed to simplify event planning and management. Built with **Django (Python)**, it offers a seamless experience for users to discover, book, and manage events ranging from weddings to corporate conferences.

---

## 🚀 Key Features

### 🔐 User Module
-   **Secure Authentication**: Sign up and login with email verification (OTP).
-   **Profile Management**: customized dashboard to view booking history and update personal details.
-   **Security**: CSRF protection, encrypted passwords, and secure session management.

### 📅 Event Management
-   **Dynamic Listings**: Browse events by category (Wedding, Corporate, Party, etc.).
-   **Smart Filtering**: Filter events by date, price, and category.
-   **Event Details**: Comprehensive view with images, descriptions, pricing, and location.
-   **Like/Favorite**: Users can "heart" events to save them for later.

### 🎟️ Booking System
-   **Custom Booking Engine**: Users can book specific events or create fully custom event requests.
-   **Real-time Availability**: Checks ticket/slot availability before confirming bookings.
-   **Status Tracking**: Track booking status (Pending, Confirmed, Rejected) from the user dashboard.

### 🎨 Frontend Experience
-   **Modern UI/UX**: Responsive design using Bootstrap 5 and custom CSS.
-   **Interactive Elements**: Real-time form validation, smooth animations (AOS), and dynamic sliders (Swiper.js).

---

## 🛠️ Technology Stack

-   **Backend**: Python 3.x, Django 5.x
-   **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
-   **Database**: SQLite (Development) / PostgreSQL (Production ready)
-   **APIs**: Django REST Framework (for mobile/external integration)

---

## ⚙️ Installation Guide

Follow these steps to set up the project locally:

### 1. Prerequisites
-   Python 3.10 or higher installed.
-   Git (optional).

### 2. Clone/Download the Repository
```bash
git clone https://github.com/yourusername/EventNest.git
cd EventNest\EventManagement\EventNestBackend
```

### 3. Set Up Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Admin)
```bash
python manage.py createsuperuser
# Follow the prompts to create an admin account
```

### 7. Run the Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 📂 Project Structure

```
EventNestBackend/
├── core/                   # Main Application Logic
│   ├── models.py           # Database Tables (Event, Booking, User)
│   ├── views.py            # Business Logic & Request Handling
│   ├── urls.py             # URL Routing
│   ├── serializers.py      # API Convertors
│   ├── templates/          # HTML Files
│   └── static/             # CSS, JS, Images
├── EventNestBackend/       # Project Configuration
│   ├── settings.py         # Global Settings
│   └── urls.py             # Main URL Entry Point
├── manage.py               # Command-line Utility
├── requirements.txt        # Project Dependencies
└── db.sqlite3              # Database File
```

---

## 🤝 Contribution
Feel free to fork this project and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)
