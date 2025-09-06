# LibraryProject

A Django web application for learning Django fundamentals and building a library management system.

## Project Overview

This project serves as the foundation for developing Django applications as part of the ALX Django Learning Lab. The LibraryProject will demonstrate core Django concepts including models, views, templates, and URL routing.

## Features

- Django project setup and configuration
- Development server for local testing
- Modular Django app structure
- Database integration capabilities
- Admin interface for content management

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Django 5.2.5
- Git for version control

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/Introduction_to_Django/LibraryProject
   ```

2. **Install Django (if not already installed):**
   ```bash
   pip install django
   ```

3. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

4. **Access the application:**
   Open your web browser and navigate to `http://127.0.0.1:8000/`

## Project Structure

```
LibraryProject/
├── manage.py              # Django's command-line utility
├── README.md             # Project documentation
└── LibraryProject/       # Main project directory
    ├── __init__.py       # Python package marker
    ├── settings.py       # Project configuration
    ├── urls.py          # URL routing configuration
    ├── wsgi.py          # WSGI deployment configuration
    └── asgi.py          # ASGI deployment configuration
```

## Key Files Explained

- **`manage.py`**: Command-line utility for interacting with the Django project
- **`settings.py`**: Contains all configuration settings for the Django project
- **`urls.py`**: URL declarations for the project - acts as a "table of contents" for your Django site
- **`wsgi.py`**: Entry point for WSGI-compatible web servers to serve your project
- **`asgi.py`**: Entry point for ASGI-compatible web servers for async support

## Development Commands

### Starting the Server
```bash
python manage.py runserver
```

### Creating a New App
```bash
python manage.py startapp app_name
```

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating a Superuser
```bash
python manage.py createsuperuser
```

## Learning Objectives

Through this project, you will learn:

- Django project structure and organization
- How to configure Django settings
- URL routing and view functions
- Template system and static files
- Model-View-Template (MVT) architecture
- Database integration with Django ORM
- Admin interface customization

## Development Roadmap

- [x] Initial Django project setup
- [x] Development server configuration
- [ ] Create library app
- [ ] Design database models
- [ ] Implement views and templates
- [ ] Add user authentication
- [ ] Implement CRUD operations
- [ ] Admin interface customization

## Contributing

This is a learning project. Feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Resources

- [Django Official Documentation](https://docs.djangoproject.com/)
- [Django Tutorial](https://docs.djangoproject.com/en/5.2/intro/tutorial01/)


## Troubleshooting

### Common Issues

**Django admin command not found:**
```bash
# Use Python module instead
python -m django startproject ProjectName
```

**Development server won't start:**
- Check if port 8000 is already in use
- Ensure you're in the correct directory with manage.py
- Verify Django is installed: `pip list | grep -i django`

**Import errors:**
- Make sure you're in the virtual environment (if using one)
- Verify Python path and Django installation

## License

This project is part of the ALX Software Engineering Program and is intended for educational purposes.

## Acknowledgments

- ALX Africa for the learning opportunity
- Django Software Foundation for the amazing framework
- The Python community for continuous support

---
