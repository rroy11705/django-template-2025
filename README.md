# Django Structured Template (2025 Edition)

A modern, production-ready Django template with clean architecture, best practices, and comprehensive tooling for 2025.

[![Django CI](https://github.com/yourusername/django-template-2025/actions/workflows/test.yml/badge.svg)](https://github.com/yourusername/django-template-2025/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/yourusername/django-template-2025/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/django-template-2025)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-5.0-green.svg)](https://djangoproject.com)

## ✨ Features

- **🏗️ Clean Architecture**: FastAPI-style structure with organized apps and services
- **⚙️ Smart Settings**: Environment-based configuration with `django-environ`
- **🔐 Production Ready**: Security settings, database optimization, and deployment configs
- **🧪 Testing Suite**: pytest, coverage, and CI/CD with GitHub Actions
- **📝 Sample Apps**: Users (custom auth) and Blog with full CRUD operations
- **🛠️ Developer Tools**: Pre-commit hooks, code formatting, and linting
- **📚 API Documentation**: Django REST Framework with comprehensive serializers

## 📁 Project Structure

```
django-template-2025/
├── apps/                          # Domain-specific applications
│   ├── users/                     # User management & authentication
│   │   ├── models.py              # Custom User model
│   │   ├── serializers.py         # DRF serializers
│   │   ├── views.py               # API endpoints
│   │   ├── urls.py                # App routing
│   │   ├── services.py            # Business logic layer
│   │   └── admin.py               # Admin configuration
│   └── blog/                      # Blog functionality
│       ├── models.py              # Post, Category, Comment models
│       ├── serializers.py         # Blog serializers
│       ├── views.py               # Blog API views
│       ├── urls.py                # Blog routing
│       ├── services.py            # Blog business logic
│       └── admin.py               # Blog admin
├── config/                        # Django configuration
│   ├── settings/
│   │   ├── base.py               # Common settings
│   │   ├── dev.py                # Development settings
│   │   └── prod.py               # Production settings
│   ├── urls.py                   # Root URL configuration
│   ├── wsgi.py                   # WSGI configuration
│   └── asgi.py                   # ASGI configuration
├── requirements/                  # Environment-specific dependencies
│   ├── base.txt                  # Core requirements
│   ├── dev.txt                   # Development tools
│   └── prod.txt                  # Production dependencies
├── tests/                        # Test suite
├── .github/workflows/            # CI/CD configuration
└── manage.py                     # Django management script
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+ 
- PostgreSQL (for production)
- Redis (optional, for caching)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/django-template-2025.git
   cd django-template-2025
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements/dev.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000/admin/` to access the admin interface.

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Enable debug mode | `False` |
| `DATABASE_URL` | Database connection string | `sqlite:///db.sqlite3` |
| `REDIS_URL` | Redis connection string | `redis://127.0.0.1:6379/1` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |

### Database Configuration

**Development (SQLite)**:
```env
DATABASE_URL=sqlite:///db.sqlite3
```

**Production (PostgreSQL)**:
```env
DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

## 🏗️ Architecture Patterns

### Service Layer Pattern

Business logic is separated into service classes:

```python
# apps/users/services.py
class UserAuthService:
    @staticmethod
    def register_user(email: str, username: str, **kwargs) -> User:
        user = User.objects.create_user(email=email, username=username, **kwargs)
        UserEmailService.send_welcome_email(user)
        return user
```

### Clean Separation of Concerns

| Layer | Responsibility | Location |
|-------|---------------|----------|
| **Models** | Data logic, constraints | `models.py` |
| **Views** | Request/response handling | `views.py` |
| **Serializers** | Data validation, I/O | `serializers.py` |
| **Services** | Business logic | `services.py` |
| **URLs** | Routing | `urls.py` |

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps

# Run specific app tests
pytest apps/users/

# Run with coverage report
pytest --cov=apps --cov-report=html
```

## 🛠️ Development Tools

### Pre-commit Hooks

Install pre-commit hooks for code quality:

```bash
pre-commit install
```

### Code Formatting

**Quick Setup:**
```bash
# Install pre-commit hooks (formats code automatically)
pre-commit install

# Manual formatting
black apps/ config/ --line-length=127
isort apps/ config/ --profile=black --line-length=127
flake8 apps/ config/

# Or use the provided script
python3 format_code.py
```

**Note:** The CI pipeline will check code formatting. If you see formatting errors, run the commands above locally and commit the changes.

## 📊 API Endpoints

### Users API
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `POST /api/users/logout/` - User logout
- `GET /api/users/profile/` - User profile
- `PUT /api/users/profile/` - Update profile

### Blog API
- `GET /api/blog/posts/` - List posts
- `POST /api/blog/posts/` - Create post
- `GET /api/blog/posts/{slug}/` - Post detail
- `PUT /api/blog/posts/{slug}/edit/` - Update post
- `DELETE /api/blog/posts/{slug}/delete/` - Delete post

## 🚢 Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure Redis for caching
- [ ] Set up static files serving
- [ ] Configure email backend
- [ ] Set up SSL/HTTPS
- [ ] Configure logging
- [ ] Set up monitoring (Sentry)

### Environment-Specific Settings

**Development**: Uses `config.settings.dev`
- SQLite database
- Debug toolbar enabled
- Console email backend

**Production**: Uses `config.settings.prod`
- PostgreSQL database
- Redis caching
- Security headers enabled
- Logging configured

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Django](https://djangoproject.com/) - The web framework for perfectionists
- [Django REST Framework](https://www.django-rest-framework.org/) - Powerful REST API toolkit
- [django-environ](https://django-environ.readthedocs.io/) - Environment variable management

---

**Built with ❤️ for the Django community in 2025**

For questions or support, please open an issue or reach out to the maintainers.