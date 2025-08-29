# Security Policy

## Sensitive Information

This project handles sensitive information in a secure way. Please follow these guidelines when working on this codebase:

### Environment Variables

-   All sensitive information should be stored in environment variables.
-   Never commit `.env` files to the repository.
-   Use `.env.example` as a template for required environment variables.
-   For development, create a `.env.local` file which is excluded from version control.

### Secrets and API Keys

-   Never hardcode secrets, API keys, or credentials in the source code.
-   Use environment variables loaded through python-dotenv for all sensitive values.
-   Generate strong, unique secrets for production environments.

### Django Settings

-   The `settings.py` file should not be committed to the repository.
-   Use `settings_template.py` as a reference for creating your local settings.
-   Keep `DEBUG=False` in production environments.
-   Use secure cookie settings in production (HTTPS-only, secure flags).

### Database Credentials

-   Database credentials should never be committed to the repository.
-   Use environment variables for database connection strings.
-   Use different credentials for development and production environments.

### SSL/TLS

-   Always use HTTPS in production.
-   Set `SECURE_SSL_REDIRECT=True` in production settings.
-   Use appropriate HSTS settings as configured.

### Media Files

-   User-uploaded content is stored in Cloudinary for security and performance.
-   Keep Cloudinary API credentials secure and never commit them to the repository.

## Reporting Security Issues

If you discover a security vulnerability within this project, please send an email to [shawnmichael.sudaria04@gmail.com](mailto:shawnmichael.sudaria04@gmail.com). All security vulnerabilities will be promptly addressed.

## Production Deployment Checklist

Before deploying to production:

1. Ensure `DEBUG=False` in production settings
2. Generate a strong, random SECRET_KEY
3. Set secure SSL settings
4. Configure proper ALLOWED_HOSTS
5. Review database security
6. Set up proper backup procedures
7. Enable rate limiting for critical endpoints
8. Review input sanitization for all forms
9. Ensure all sensitive environment variables are properly set
