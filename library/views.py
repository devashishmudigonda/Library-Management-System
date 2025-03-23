from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .forms import StudentsForm, BookForm, Book_IssueForm, Book_instanceForm
from .models import Students, Book, Book_Issue, BookInstance
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# CONSTANTS
CollegeKeyPass = 1234


# @login_required(login_url="login")

# def homePage(request):
#     return render(request, "home.html", {"username": request.user.username})


# loginpage
def loginPage(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return HttpResponse("Username or Password is incorrect!!!")
    return render(request, "login.html")


# logoutpage
def logoutPage(request):
    logout(request)
    return redirect("login")


# registerpage
def registerPage(request):
    if request.method == "POST":
        username = request.POST["username"]
        ckp = int(request.POST["clgkeypass"])
        email = request.POST["email"]
        pass1 = request.POST["password1"]
        pass2 = request.POST["password2"]

        if ckp == CollegeKeyPass:
            if pass1 != pass2:
                return HttpResponse("Passwords Did Not Matched")
            else:
                my_user = User.objects.create_user(username, email, pass1)
                my_user.save()
                return redirect("login")
        else:
            return HttpResponse("College Key Pass is Incorrect")
    return render(request, "register.html")


# @login_required(login_url="login")
def index(request):
    return render(request, "index.html")


@login_required(login_url="login")
def add_new_student(request):
    if request.method == "POST":
        form = StudentsForm((request.POST))
        if form.is_valid():
            form.save()
            return redirect("/show_students")
    else:
        form = StudentsForm
    return render(request, "add_new_student.html", {"form": form})


@login_required(login_url="login")
def add_new_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form = form.save()
            book_instance = BookInstance(book=form)
            book_instance.save()
            return redirect("/view_books")
    else:
        form = BookForm
        form_instance = Book_instanceForm
        return render(
            request, "add_new_book.html", {"form": form, "form_instance": form_instance}
        )


@login_required(login_url="login")
def add_new_book_instance(request):
    if request.method == "POST":
        form = Book_instanceForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/view_books")
    return HttpResponse("Problem")


@login_required(login_url="login")
def add_book_issue(request):
    if request.method == "POST":
        form = Book_IssueForm(request.POST)
        if form.is_valid():
            # save data
            unsaved_form = form.save(commit=False)
            book_to_save = BookInstance.objects.get(id=unsaved_form.book_instance.id)
            book_to_save.Is_borrowed = True
            book_to_save.save()
            form.save()
            form.save_m2m()
        return redirect("/view_books_issued")
    else:
        print("helloooo")
        context = {
            "form": Book_IssueForm,
            "book": BookInstance.objects.filter(Is_borrowed=False),
        }
        return render(request, "add_book_issue.html", context=context)


@login_required(login_url="login")
def view_students(request):
    students = Students.objects.order_by("-id")
    return render(request, "view_students.html", {"students": students})


@login_required(login_url="login")
def view_books(request):
    books = BookInstance.objects.order_by("id")
    return render(request, "view_books.html", {"books": books})


@login_required(login_url="login")
def view_bissue(request):
    issue = Book_Issue.objects.order_by("-id")
    return render(request, "issue_records.html", {"issue": issue})


@login_required(login_url="login")
def edit_student_data(request, roll):
    try:
        if request.method == "POST":
            std = Students.objects.get(id=request.session["id"])
            form = StudentsForm((request.POST), instance=std)
            if form.is_valid():
                form.save()
            del request.session["id"]
            return redirect("/show_students")
        else:
            student_to_edit = Students.objects.get(roll_number=roll)
            student = StudentsForm(instance=student_to_edit)
            request.session["id"] = student_to_edit.id
            return render(request, "edit_student_data.html", {"student": student})
    except Exception as error:
        print(f"{error} occured at edit_student_data view")


@login_required(login_url="login")
def edit_book_data(request, id):
    return HttpResponse(
        f"<label>A book with ID: {id} could not be edited...</label><h2>The feature is comming soon</h2>"
    )


@login_required(login_url="login")
def delete_student(request, roll):
    return HttpResponse(
        f"<h2>Delete Student</h2><label>Student with Roll Number: {roll} could not be deleted...</label><h2>The feature is comming soon</h2>"
    )
    pass


@login_required(login_url="login")
def delete_book(request, id):
    # obj = get_object_or_404(Book, id=id)
    book_to_delete = get_object_or_404(Book, id=id)
    book_to_delete.delete()
    # book_to_save = Book.objects.get(id=id)
    # book_to_save.delete()
    # return redirect("view_books/")
    return HttpResponse(
        f"<h2>Delete Book</h2><label>Book with ID: {id} could not be deleted..</label><h2>The feature is comming soon</h2>"
    )


@login_required(login_url="login")
def return_issued_book(request, id):
    book_issue = get_object_or_404(Book_Issue, id=id)
    if book_issue:
        book_to_save = BookInstance.objects.get(id=book_issue.book_instance.id)
        book_to_save.Is_borrowed = False

        book_to_save.save()

        book_issue.delete()

        return redirect("/view_books_issued")
    return HttpResponse("book not found")


@login_required(login_url="login")
def edit_issued(request, id):
    obj = Book_Issue.objects.get(id=id)
    return HttpResponse(
        f"<h2>Edit Issued Book</h2><label>Book <i>{obj.book_instance.book.book_title}</i> issued to <i>{obj.student.fullname}</i> could not be edited..</label><h2>The feature is comming soon</h2>"
    )
