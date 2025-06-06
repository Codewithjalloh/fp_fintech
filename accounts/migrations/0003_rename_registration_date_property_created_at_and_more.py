# Generated by Django 5.0.2 on 2025-04-15 07:59

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_address_alter_user_employment_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='registration_date',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='property',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('verified', 'Verified'), ('rejected', 'Rejected')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='property',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='estimated_value',
            field=models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='monthly_income',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.CreateModel(
            name='UserDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('national_id', 'National ID'), ('passport', 'Passport'), ('employment_letter', 'Employment Letter'), ('bank_statement', 'Bank Statement'), ('tax_clearance', 'Tax Clearance'), ('other', 'Other')], max_length=50)),
                ('document_file', models.FileField(upload_to='user_documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
