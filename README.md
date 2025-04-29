# PlotPay

PlotPay is a Django-based web application for managing property loans and payments. The platform facilitates loan applications, disbursements, and repayments with a focus on property-related financing.

## Features

- User authentication and authorization
- Property management
- Loan application processing
- Loan disbursement tracking
- Repayment management
- Admin dashboard for loan management
- Mobile money integration for payments

## Tech Stack

- **Backend**: Django 5.0.2
- **Database**: SQLite (Development), PostgreSQL (Production)
- **Authentication**: Django Allauth
- **Form Handling**: Django Crispy Forms with Bootstrap 5
- **Storage**: Django Storages with Boto3 for AWS S3


## Prerequisites

- Python 3.8+
- pip
- PostgreSQL (for production)
- AWS S3 account (for media storage in production)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PlotPay
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

4. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
PlotPay/
├── accounts/         # User account management
├── loans/           # Loan application and management
├── core/            # Core project settings and utilities
├── config/          # Project configuration
├── static/          # Static files (CSS, JS, images)
├── templates/       # HTML templates
├── media/           # User uploaded media
└── manage.py        # Django management script
```

## Admin Interface

The admin interface provides comprehensive management tools for:
- Loan applications
- Loan disbursements
- Repayments
- User management
- Property management

Access the admin interface at `/admin/` after creating a superuser.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]

## Support

For support, please contact [your contact information] 
