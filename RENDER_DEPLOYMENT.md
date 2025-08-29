# Deploying to Render.com

This guide will help you deploy your Personal Website project to Render.com, a cloud hosting platform with a generous free tier.

## Prerequisites

-   A GitHub repository with your Personal Website code
-   A Render.com account (sign up at https://render.com)

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
-   **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
-   **Start Command**: `gunicorn personal_website.wsgi:application`

### 3. Set Environment Variables

Click on "Advanced" and add the following environment variables:

```
DEBUG=False
DJANGO_SECRET_KEY=your-generated-secret-key
ALLOWED_HOSTS=*.render.com,*.onrender.com,yourdomain.com,www.yourdomain.com
USE_SQLITE=True
USE_CLOUDINARY=False
SECURE_SSL_REDIRECT=True
```

### 4. Set Up Persistent Storage (Optional)

If you want your SQLite database and media files to persist between deployments:

1. Scroll down to "Disks" in the advanced settings
2. Add a disk:
    - **Name**: `data`
    - **Mount Path**: `/opt/render/project/src/data`
    - **Size**: 1 GB (minimum)

Then update these environment variables:

```
DATABASE_URL=sqlite:///./data/db.sqlite3
MEDIA_ROOT=data/media
```

### 5. Deploy the Service

Click "Create Web Service" to start the deployment process.

Render will automatically:

1. Clone your repository
2. Install dependencies
3. Run your build command
4. Start your application

### 6. Access Your Website

Once the deployment is complete, your website will be available at:

```
https://your-service-name.onrender.com
```

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

1. Check the logs for error messages
2. Verify your environment variables are set correctly
3. Make sure your database configuration is correct
4. Check if static files are being served properly

## Limitations of Render Free Tier

-   Your service will spin down after 15 minutes of inactivity
-   Limited to 750 hours of usage per month
-   Limited build minutes per month
-   Standard (ephemeral) storage is cleared on each deploy

With persistent disk storage, your data will be preserved between deployments, but your service will still spin down after inactivity periods.
