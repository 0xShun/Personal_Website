# Personal Website

A Django-based personal website with articles, projects, and research sections.

## Setup Instructions

1. Clone the repository:

```bash
git clone <repository-url>
cd personal_website
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a local settings file:

```bash
cp personal_website/settings_template.py personal_website/settings.py
```

5. Update the settings file with your configuration:

-   Set your `SECRET_KEY`
-   Configure email settings
-   Update database settings if needed
-   Set `DEBUG = False` in production

6. Apply migrations:

```bash
python manage.py migrate
```

7. Create a superuser:

```bash
python manage.py createsuperuser
```

8. Run the development server:

```bash
python manage.py runserver
```

## Security Guidelines

1. **Never commit sensitive information**:

    - Keep `settings.py` in `.gitignore`
    - Use environment variables for sensitive data
    - Never commit API keys or passwords

2. **Email Configuration**:

    - Use Gmail App Password instead of your main password
    - Keep email credentials in environment variables
    - Use a separate email account for the website

3. **Production Deployment**:

    - Set `DEBUG = False`
    - Use a proper web server (e.g., Nginx, Apache)
    - Enable HTTPS
    - Use a production-grade database
    - Set up proper logging

4. **File Uploads**:
    - Validate file types and sizes
    - Store uploads outside the web root
    - Use unique filenames
    - Implement proper access controls

## Project Structure

```
personal_website/
├── Main/                 # Main app with core functionality
├── Articles/            # Articles app
├── Projects/           # Projects app
├── Research/          # Research app
├── media/             # User-uploaded files
├── static/            # Static files
├── templates/         # Base templates
└── personal_website/  # Project settings
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
