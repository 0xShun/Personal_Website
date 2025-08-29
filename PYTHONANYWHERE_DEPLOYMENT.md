# Deploying to PythonAnywhere

This guide will help you deploy your Personal Website project to PythonAnywhere.

## Steps for Deployment

### 1. Create a PythonAnywhere Account

-   Sign up at https://www.pythonanywhere.com/
-   Choose a free account or a paid plan based on your needs

### 2. Clone Your Repository

-   Open a Bash console in PythonAnywhere
-   Clone your repository:
    ```
    git clone https://github.com/0xShun/Personal_Website.git
    ```

### 3. Set Up a Virtual Environment

```bash
cd Personal_Website
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Create Environment File

-   Create a `.env` file in the personal_website directory:

```bash
cd personal_website
cp .env.production .env
nano .env  # Edit the environment variables
```

### 5. Set Up the Database

```bash
python manage.py migrate
python manage.py collectstatic
```

### 6. Create a Web App in PythonAnywhere

-   Go to the Web tab in PythonAnywhere
-   Click "Add a new web app"
-   Choose "Manual configuration"
-   Choose Python 3.9 (or your preferred version)

### 7. Configure the Web App

-   Set the virtual environment path: `/home/yourusername/Personal_Website/venv`
-   Set the WSGI file path to use the pythonanywhere_wsgi.py file
    -   Edit the WSGI file provided by PythonAnywhere
    -   Replace its contents with your `pythonanywhere_wsgi.py` code
    -   Update the paths in the WSGI file to match your PythonAnywhere username

### 8. Set Up Static Files

-   In the Web tab, under "Static files":
    -   URL: `/static/`
    -   Directory: `/home/yourusername/Personal_Website/personal_website/staticfiles`

### 9. Configure Media Files (if needed)

Since you're using Cloudinary for media storage, you don't need to configure local media file serving.

### 10. Reload the Web App

-   Click the "Reload" button in the Web tab

### 11. Visit Your Site

-   Your site should now be accessible at `yourusername.pythonanywhere.com`

## Troubleshooting

### Check the Error Logs

-   In the Web tab, check the "Error log" link if your site doesn't work
-   Common issues include path problems in the WSGI file or missing dependencies

### Database Issues

-   Make sure your database settings are correct in the .env file
-   For SQLite, ensure the path is absolute and points to a directory where you have write access

### Static Files Not Loading

-   Run `python manage.py collectstatic` again
-   Verify the static files directory in PythonAnywhere configuration

### Update Your Site

To update your site after making changes to your GitHub repository:

```bash
cd ~/Personal_Website
git pull
source venv/bin/activate
python personal_website/manage.py migrate
python personal_website/manage.py collectstatic --noinput
```

Then reload your web app from the Web tab.
