import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from django.utils import timezone

# Create test user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123',
    phone_number='+1234567890',
    national_id='123456789',
    date_of_birth='1990-01-01',
    address='123 Test Street',
    employment_status='employed',
    monthly_income=5000.00
)

print('Test user created successfully!')
print(f'Username: {user.username}')
print(f'Email: {user.email}')
print(f'Password: testpass123') 