# Deploying to Render.com

This guide will help you deploy your Personal Website project to Render.com, a cloud hosting platform with a generous free tier.

## Prerequisites

-   A GitHub repository with your Personal Website code
-   A Render.com account (sign up at https://render.com)

## Project Structure Requirements

For a successful deployment to Render, ensure your project structure is:

```
Repository/
└── personal_website/       # Root directory that you'll set in Render
    ├── manage.py           # Django manage.py file
    ├── requirements.txt    # Dependencies file (moved inside this directory)
    ├── personal_website/   # Django project settings directory
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── Main/               # Django app directories
    ├── Articles/
    ├── Projects/
    └── Research/
```

> **Note**: Make sure the requirements.txt file is placed inside the personal_website directory.

## Steps for Deployment

### 1. Create a New Web Service on Render

1. Log in to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Choose the repository that contains your Personal Website project

### 2. Configure the Web Service

Fill in the following details:

-   **Name**: Choose a name for your service (e.g., "personal-website")
-   **Root Directory**: `personal_website` (the directory containing manage.py)
-   **Environment**: Python
-   **Region**: Choose the region closest to your users
-   **Branch**: main (or your preferred branch)
-   **Build Command**: `chmod +x build.sh && ./build.sh`
-   **Start Command**: `gunicorn personal_website.wsgi:application`

### 3. Set Environment Variables

Click on "Advanced" and add the following environment variables:

```
DEBUG=False
DJANGO_SECRET_KEY=django-insecure-h@iw6v$e8_7jskl3&g7y@t)^!6%6p1zcet9_sc^c)%vua5&+_e
ALLOWED_HOSTS=*.render.com,*.onrender.com,yourdomain.com,www.yourdomain.com
USE_SQLITE=False
DATABASE_URL=postgresql://username:password@hostname/database?sslmode=require
USE_CLOUDINARY=False
SECURE_SSL_REDIRECT=True
```

> **Note**: For security in a production environment, you should use a different secret key than what's shown in this example.

### 4. PostgreSQL Database Setup

For a more reliable database solution, Render offers a free PostgreSQL database:

1. From your Render dashboard, click "New" and select "PostgreSQL"
2. Configure your database:
    - **Name**: Choose a name (e.g., `personal-website-db`)
    - **Database**: Pick a database name (or leave as default)
    - **User**: A database user is created automatically
    - **Region**: Choose the same region as your web service
3. Click "Create Database"
4. Once created, copy the "Internal Database URL" from the database dashboard
5. Update your web service's `DATABASE_URL` environment variable with this value

#### Using Neon PostgreSQL

If you're using Neon.tech for your PostgreSQL database instead of Render's PostgreSQL:

1. Make sure your DATABASE_URL includes the `sslmode=require` parameter:

    ```
    DATABASE_URL=postgresql://username:password@hostname/database?sslmode=require
    ```

2. The code has been updated to automatically detect Neon databases and apply the correct SSL settings.

#### Testing Database Connection

To test your database connection:

1. After deployment, go to your web service logs
2. Check for any database connection errors
3. You can also SSH into your Render instance and run the test script:
    ```
    python test_db.py
    ```

### 5. Deploy the Service

Click "Create Web Service" to start the deployment process.

Render will automatically:

1. Clone your repository
2. Install dependencies
3. Run your build command
4. Start your application

The deployment process may take a few minutes. You can monitor the progress in the Render dashboard.

### 6. Access Your Website

Once the deployment is complete, your website will be available at:

```
https://your-service-name.onrender.com
```

## PostgreSQL Database Management

Your site is using a PostgreSQL database on Render. Here's how to manage it:

### Accessing Your Database

You can connect to your database using any PostgreSQL client with these credentials:

-   **Host**: dpg-d2otorbipnbc73a84bo0-a.oregon-postgres.render.com (for external access)
-   **Port**: 5432
-   **Database**: personal_site_database_36eu
-   **Username**: personal_site_database_36eu_user
-   **Password**: LrAVZCvDjdjWpAMOxR7oyJgWJDpEfi2J

### Using psql Command Line

To connect via command line:

```
PGPASSWORD=LrAVZCvDjdjWpAMOxR7oyJgWJDpEfi2J psql -h dpg-d2otorbipnbc73a84bo0-a.oregon-postgres.render.com -U personal_site_database_36eu_user personal_site_database_36eu
```

### Database Backups

Render automatically creates daily backups of your PostgreSQL database that are retained for 7 days on the free plan.

## Custom Domain Setup (Optional)

To use your own domain with Render:

1. Go to your web service settings
2. Click on "Custom Domain"
3. Follow the instructions to configure your domain's DNS settings

## Monitoring and Logs

-   View logs by clicking on your web service and selecting the "Logs" tab
-   Monitor resource usage in the "Metrics" tab

## Updating Your Site

To update your site:

1. Push changes to your GitHub repository
2. Render will automatically deploy the updates

## Troubleshooting

If your site isn't working properly:

-   **Database connection errors**:

    -   Check if your DATABASE_URL is correct
    -   For Neon PostgreSQL, ensure the SSL parameters are included
    -   Verify the database server is up and running
    -   Common errors:
        -   `SSL connection has been closed unexpectedly`: Add `?sslmode=require` to your connection string
        -   `Error loading psycopg2 or psycopg module`: Make sure both psycopg2-binary and psycopg are in requirements.txt
        -   Connection timeouts: Neon free tier may hibernate, try accessing the database first

-   **Static files not loading**:

    -   Check if collectstatic ran successfully during build
    -   Verify STATIC_URL and STATIC_ROOT settings
    -   Make sure whitenoise is configured correctly

-   **Media files not accessible**:

    -   If not using Cloudinary, check if disk storage is mounted correctly
    -   Verify media files permissions

-   **Application errors**:

    -   Check the logs for detailed error messages
    -   Try setting DEBUG=True temporarily to see detailed error pages
    -   Verify all environment variables are set correctly

## Limitations of Render Free Tier

-   Your web service will spin down after 15 minutes of inactivity
-   Limited to 750 hours of usage per month
-   Limited build minutes per month
-   Standard (ephemeral) storage is cleared on each deploy
-   PostgreSQL database limited to 1GB storage
-   Maximum of 10 connections to PostgreSQL database
-   PostgreSQL databases on free plans are suspended after 90 days of inactivity

Using PostgreSQL instead of SQLite means your database will persist between deployments without needing a disk mount. Your web service will still spin down after periods of inactivity, but your database will remain available.
