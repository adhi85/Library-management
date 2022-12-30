from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Book, User
from django.contrib import messages
from .forms import NewUserForm,NewBookForm
from django.db.models import Q
# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth


def home(request):

    book = Book.objects.order_by('-added_date')[:5]
    book_trending = Book.objects.order_by('copies')[:5]

    context = {'book': book, 'book_trending': book_trending}
    return render(request, 'base/home.html', context)


def sign_in_admin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if (user.is_superuser == True):
                    login(request, user)

                    return redirect('home')
            else:
                    messages.error(
                        request, 'Please enter the correct username and password for a admin account.')
                    return redirect('sign_in_admin')
        else:
             messages.error(
                 request, 'Please enter the correct username and password for a admin account.')
             return redirect('sign_in_admin')

    else:
      return render(request, 'base/signin_admin.html')

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                if (user.is_superuser == True):
                    messages.error(request, "Please use Admin Sign in if you are an Admin.")
                else:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "base/login.html", {"form": form})


def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "base/register.html", {"form": form})


def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')


@login_required(login_url='/login')
def mycart(request):
    user = request.user
    book1 = user.book1
    if (book1 != "no"):
        buk1 = Book.objects.get(name=book1)
    else:
        buk1 = Book.objects.all()
    book2 = user.book2
    if (book2 != "no"):
        buk2 = Book.objects.get(name=book2)
    else:
        buk2 = Book.objects.all()
    context = {'user': user, "buk1": buk1, "buk2": buk2}
    return render(request, 'base/mycart.html', context)


@login_required(login_url='/login')
def confirm(request, pk):

    # if cache.get(pk):
    #     book = cache.get(pk)

    # else:
    #     book = Book.objects.get(id=pk)
    #     cache.set(pk, book)
    book = Book.objects.get(id=pk)
    user = request.user

    def delete_copy(book):
        book.copies = book.copies - 1
        book.save()

    if request.method == 'POST':
        if (user.book1 != "no" and user.book2 != "no"):
            messages.error(request, 'You cannot borrow more than 2 books.')

        elif (user.book1 == "no" and book.name != user.book2):
            print("hi 1")
            user.book1 = book.name
            delete_copy(book)
            user.save()
            return redirect('mycart')
        elif (user.book2 == "no" and book.name != user.book1):
            print("hi 2")
            user.book2 = book.name
            delete_copy(book)
            user.save()
            return redirect('mycart')
        else:
            messages.error(request, 'You cannot borrow the same book again.')

    return render(request, 'base/confirm.html', {'book': book})


@login_required(login_url='/login')
def return_book(request, pk):

    # if cache.get(pk):
    #     book = cache.get(pk)

    # else:
    #     book = Book.objects.get(id=pk)
    #     cache.set(pk, book)

    book = Book.objects.get(id=pk)
    user = request.user

    def add_copy(book):
        book.copies += 1
        book.save()

    if request.method == 'POST':
        if (user.book1 == book.name):
            user.book1 = "no"
            print("hello 1")
            add_copy(book)
            user.save()
            return redirect('mycart')

        elif (user.book2 == book.name):
            user.book2 = "no"
            print("hello 2")
            user.save()
            add_copy(book)
            return redirect('mycart')
        else:
            messages.error(request, 'ERROR returning book')

    return render(request, 'base/return.html', {'book': book})


def allbooks(request):
    all = Book.objects.all()

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    book = Book.objects.filter(
        Q(name__icontains=q) |
        Q(author__icontains=q)
    )

    return render(request, 'base/allbooks.html', {'book': book, 'all': all})

def deletebook(request):
    all = Book.objects.all()

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    book = Book.objects.filter(
        Q(name__icontains=q) |
        Q(author__icontains=q)
    )

    return render(request, 'base/deletebooks.html', {'book': book, 'all': all})

@login_required(login_url='/login')
def addBook(request):
    form = NewBookForm()
    
    if request.method == "POST":
        form = NewBookForm(request.POST)
        if form.is_valid():
            
            f=form.save(commit=False)
            f.save()

            return redirect('allbooks') 
        else:
            form = NewBookForm()
    return render(request, 'base/addbook.html', {'form': form})

@login_required(login_url='/login')
def delete(request, pk):
    book = Book.objects.get(id=pk)
    if request.method == 'POST':
        book.copies = 0
        book.save()
        return redirect('allbooks')
        
    return render(request, 'base/delete.html', {'book': book})

@login_required(login_url='/login')
def list(request):
    ad = request.user
    if ad.is_superuser != True:
        return redirect('allbooks')
    users = User.objects.all()
    return render(request, 'base/list.html', {'users': users})