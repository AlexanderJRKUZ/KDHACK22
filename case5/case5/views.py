from threading import BrokenBarrierError
from xmlrpc.server import MultiPathXMLRPCServer
from django.forms import CharField
from django.shortcuts import redirect, render
from user.models import User
from user.models import Booking
from http import cookies
import datetime


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def reg(request):
    return render(request, 'reg.html')

def check(book_by_time, date, time, timeend):
    for i in range(book_by_time.count()):
        el = book_by_time.objects.filter(id__iexact=i)
        print(time, timeend, el.time, el.timeend)
        if time <= el.time <= timeend or time <= el.timeend <= timeend or el.time <= time and el.timeend >= timeend:
            return False
    return True

        
    

def booking(request):
    
    if request.method == 'POST':
        dt = request.POST.get('date').split('-')
        dt = tuple(map(int, dt))
        a, b, c = dt[0], dt[1], dt[2]
        date = datetime.date(a, b, c)

        t = request.POST.get('time').split(':')
        t = tuple(map(int, t))
        a, b = t[0], t[1]
        time = datetime.time(a, b)

        te = request.POST.get('timeend').split(':')
        te = tuple(map(int, te))
        a, b = te[0], te[1]
        timeend = datetime.time(a, b)

        hall = request.POST.get('hall')
        book_by_hall = Booking.objects.filter(hall__iexact=hall)
        book_by_date = book_by_hall.filter(date__iexact=date)
        book_by_time = book_by_date.filter(approved__iexact=True)
        if check(book_by_time, date, time, timeend):
            print('here')
            book = Booking()

            dt = request.POST.get('date').split('-')
            dt = tuple(map(int, dt))
            a, b, c = dt[0], dt[1], dt[2]
            date = datetime.date(a, b, c)

            t = request.POST.get('time').split(':')
            t = tuple(map(int, t))
            a, b = t[0], t[1]
            time = datetime.time(a, b)

            te = request.POST.get('timeend').split(':')
            te = tuple(map(int, te))
            a, b = te[0], te[1]
            timeend = datetime.time(a, b)

            book.title = request.POST.get('event_name')
            book.description = request.POST.get('event_disc')
            book.type = request.POST.get('event_type')
            book.hall = request.POST.get('hall')
            book.chairs = request.POST.get('chair')
            book.TVs = request.POST.get('LG')
            book.brown_tables = request.POST.get('brown_table')
            book.white_tables = request.POST.get('white_table')
            book.bebra_trees = request.POST.get('bebra')
            book.journal_tables = request.POST.get('jour_table')
            book.sofas = request.POST.get('sofa')
            book.bar_stools = request.POST.get('bar_chair')
            book.speakers = request.POST.get('stereo')
            book.mic = request.POST.get('radio')
            book.mixer = request.POST.get('mixer')
            book.beige_tables = request.POST.get('beig_table')
            book.tables =  request.POST.get('table')
            book.user_id = int(request.COOKIES['id'])
            book.save()
    return render(request, 'booking.html')

def adminpanel(request):
    return render(request, 'adminpanel.html')

def home(request):
    return render(request, 'home.html')

def profile(request):
    user = User
    x = int(request.COOKIES['id'])
    u = user.objects.filter(id__iexact=x)
    ctx = {
        'user': u.latest('login').name,
    }
    return render(request, 'profile.html', ctx)

def login(request):
    rsn = render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = User.objects.filter(login__iexact=username)
        if not (user.count() == 0):
            print(user.latest('login').id)
            if username == user.latest('login').login and password == user.latest('login').password:
                rsn.set_cookie('id', user.latest('login').id, max_age=315336000)
                # return redirect('/profile')
    return rsn


def singup(request):
    user = User()
    ctx = {
        'name': user.name 
    }
    rsn = render(request, 'singup.html', ctx)
    if request.method == 'POST':
        user.login = request.POST.get('login')
        user.name =  request.POST.get('name')
        user.tg = request.POST.get('tg')
        user.email = request.POST.get('email')
        user.password = request.POST.get('password')
        user.save()
        rsn.set_cookie('id', str(user.id), max_age=315336000)
        # return redirect('/profile')
    return rsn
