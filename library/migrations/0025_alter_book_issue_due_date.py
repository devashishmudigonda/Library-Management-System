# Generated by Django 4.2.5 on 2023-09-05 15:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0024_alter_book_issue_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_issue',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 13, 21, 12, 31, 449908), help_text='Date the book is due to'),
        ),
    ]
