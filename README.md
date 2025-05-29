# 🔐 Django Backend for React-Django Authentication App

Welcome to the backend of my full-stack authentication project built using Django and Django REST Framework. This project connects seamlessly with a React frontend and demonstrates robust authentication features, including email verification, token-based authentication, and password management. To demonstrate the functionality, a simple api for the url-shortner app is configured in here

## 📌 Project Features

- ✅ **Account Activation**: Email-based account verification after user registration.
- 🔐 **Token-Based Authentication**: Using JWT (JSON Web Tokens) to securely manage user sessions.
- 🔁 **Password Management**:
        - Reset password via email link.
        - Change password while logged in.
- ✏️ **Profile Management**: Authenticated users can update their profile details.

## 📁 Project Structure

        ├── accounts/       # Custom user model and authentication logic
        ├── url_shortner/   # Project settings and URLs
        ├── shorten_url/    # URL shortening logc
        ├── templates/
        ├── manage.py


## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.8+
- pip
- virtualenv (optional but recommended)

### Installation

1. **Clone the Repository**

        git clone https://github.com/SakarDahal04/URL-Shortner-project.git

2. **Create Virtual Environment and Install Dependencies**

        python -m venv venv
        source venv/bin/activate   # On Windows: venv\Scripts\activate
        pip install -r requirements.txt

3. **Environment Variables**

        SECRET_KEY=your-django-secret-key
        DEBUG=True
        ALLOWED_HOSTS=your_backend_domain localhost 127.0.0.1
        EMAIL_HOST=smtp.yourprovider.com
        EMAIL_PORT=587
        EMAIL_FROM=emai@example.com
        EMAIL_HOST_USER=your-email@example.com
        EMAIL_HOST_PASSWORD=your-email-password
        EMAIL_USE_TLS=True
        FRONTEND_URL=http://localhost:5173

4. **Run Migrations and Start Server**

        python manage.py makemigrations
        python manage.py migrate
        python manage.py runserver

    API Endpoints Overview:

        | Method  | Endpoint                                            | Description                       |
        | ------- | ----------------------------------------------------| --------------------------------- |
        | POST    | `/account/register/`                                | Register a new user               |
        | GET     | `/account/activate/<uidb64>/<token>/`               | Activate account via email        |
        | POST    | `/api/token/`                                       | Login and get JWT token           |
        | POST    | `/api/token/refresh/`                               | Refresh JWT token                 |
        | POST    | `/account/password-reset/`                          | Request password reset email      |
        | POST    | `/account/password-reset-confirm/<uidb64>/<token>/` | Reset password                    |
        | POST    | `/account/change-password/`                         | Change password (logged-in users) |
        | GET/PUT | `/account/user-update/`                             | got or update user information    |


5. **Technologies Used**
    - Django
    - Django REST Framework
    - djangorestframework-simplejwt
    - Custom User Model
    - Email Backend (SMTP)
    - CORS Headers

6. **🙋‍♂️ About Me**

    Hi, I'm Sakar Dahal, the creator of this site. I'm passionate about web development and built this project to understand how secure full-stack authentication systems work in practice.

    Frontend repo: [React Frontend](https://github.com/SakarDahal04/URL-Shortner-project)

7. **Contact**

    Feel free to contact with me via [LinkedIn](https://www.linkedin.com/in/sakar-dahal-30a560277/)


This project is a work in progress, and I'm continuously learning and improving. Contributions and feedback are welcome!