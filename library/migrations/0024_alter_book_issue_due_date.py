# Generated by Django 4.1.7 on 2023-07-19 12:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0023_alter_book_id_alter_book_issue_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_issue',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 27, 18, 0, 44, 206503), help_text='Date the book is due to'),
        ),
    ]
