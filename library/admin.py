from django.contrib import admin
from library.models import Students, Book, BookInstance, Book_Issue
# Register your models here.
admin.site.register(Students)
admin.site.register(Book)
admin.site.register(Book_Issue)
admin.site.register(BookInstance)