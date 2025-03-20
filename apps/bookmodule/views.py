from django.http import HttpResponse
from django.shortcuts import render 
from .models import Book
from .models import Address
from django.db.models import Q
from django.db.models import Sum, Avg, Max, Min, Count

def index(request):
    name = request.GET.get('name', 'world')  # Get the 'name' parameter from the query string
    #return HttpResponse(f"Hello, {name}!")
    return render(request, "bookmodule/index.html" , {"name": name})

def index2(request, val1 = 0): #add the view function (index2)
    return HttpResponse("value1 = "+str(val1))

def viewbook(request, bookId):
 # assume that we have the following books somewhere (e.g. database)
    book1 = {'id':123, 'title':'Continuous Delivery', 'author':'J. Humble and D. Farley'}
    book2 = {'id':456, 'title':'Secrets of Reverse Engineering', 'author':'E. Eilam'}
    targetBook = None
    if book1['id'] == bookId: targetBook = book1
    if book2['id'] == bookId: targetBook = book2
    context = {'book':targetBook} # book is the variable name accessible by the template
    return render(request, 'bookmodule/show.html', context)

def index(request):
   return render(request, "bookmodule/index.html")
def list_books(request):
   return render(request, 'bookmodule/list_books.html')
def viewbook(request, bookId):
   return render(request, 'bookmodule/one_book.html')
def aboutus(request):
   return render(request, 'bookmodule/aboutus.html')
def links_page(request):
    return render(request, 'bookmodule/links.html')
def text_formatting(request):
    return render(request, 'bookmodule/text_formatting.html')
def listing(request):
    return render(request, 'bookmodule/listing.html')
def tables(request):
    return render(request, 'bookmodule/tables.html')
def search(request):
    return render(request, 'bookmodule/search.html')
def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]

def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower(): contained = True
            if not contained and isAuthor and string in item['author'].lower():contained = True
            if contained: newBooks.append(item)
        return render(request, 'bookmodule/bookList.html', {'books':newBooks})
    else :
        return render(request, 'bookmodule/search.html')
    
def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='and')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def complex_query(request):
    mybooks = Book.objects.filter(author__isnull=False) \
        .filter(title__icontains='and') \
        .filter(edition__gte=2) \
        .exclude(price__lte=100)[:10]
    
    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')

def task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/task1.html', {'books': books})

def task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & 
        (Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/task2.html', {'books': books})

def task3(request):
    books = Book.objects.filter(
        Q(edition__lte=3) & 
        ~Q(title__icontains='qu') & 
        ~Q(author__icontains='qu')
    )
    return render(request, 'bookmodule/task3.html', {'books': books})

def task4(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/task4.html', {'books': books})

def task5(request):
    total_books = Book.objects.count()
    total_price = Book.objects.aggregate(Sum('price'))['price__sum']
    avg_price = Book.objects.aggregate(Avg('price'))['price__avg']
    max_price = Book.objects.aggregate(Max('price'))['price__max']
    min_price = Book.objects.aggregate(Min('price'))['price__min']

    return render(request, 'bookmodule/task5.html', {
        'total_books': total_books,
        'total_price': total_price,
        'avg_price': avg_price,
        'max_price': max_price,
        'min_price': min_price,
    })


def task6(request):
    cities = Address.objects.annotate(num_students=Count('student'))
    return render(request, 'bookmodule/task6.html', {'cities': cities})
