from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from . import models
from . import forms

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        logout(request)
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = ''
            user_list = User.objects.all()
            for user in user_list:
                if user.email == form.cleaned_data['email']:
                    username = user.username
            user = authenticate(
                username=username,
                password=form.cleaned_data['password']
            )
            if user is None:
                return HttpResponseRedirect('/main/login')
            login(request, user)
            return HttpResponseRedirect('/main')
    context = {
        'form': form
    }
    return render(request, 'main/login_page.html', context)

def signup(request):
    if request.user.is_authenticated:
        logout(request)
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['name'],
                last_name=form.cleaned_data['surname']
            )
            return HttpResponseRedirect('/main/login/')
    context = {
        'form': form
    }
    return render(request, 'main/signup_page.html', context)

def main(request):
    context = {}
    return render(request, 'main/main_page.html', context)

def tours(request):
    tour_list = models.Tour.objects.all()
    context = {
        'tours': tour_list
    }
    return render(request, 'main/tours_page.html', context)

def tour_country(request, country):
    tour_list = models.Tour.objects.all()
    country_tours = tour_list.filter(country=country)
    context = {
        'tours': tour_list,
        'country': country,
        'country_tours': country_tours
    }
    return render(request, 'main/tour_country.html', context)

def review(request, tour_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/main/login/')

    tour_list = models.Tour.objects.all()
    tour = tour_list.get(pk=tour_id)

    form = forms.ReviewForm()

    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            new_review = models.Review(
                comment=form.cleaned_data['comment'],
                rates=form.cleaned_data['rate'],
                comment_date=timezone.now(),
                tour=tour,
                user=request.user
            )
            new_review.save()

    review_list = models.Review.objects.all()
    reviews = review_list.filter(tour=tour)

    context = {
        'reviews': reviews,
        'tours': tour_list,
        'tour': tour,
        'form': form
    }

    return render(request, 'main/review.html', context)

def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/main/login/')

    reservation_list = models.Reservation.objects.all().filter(user=request.user)

    context = {
        'name': request.user.first_name,
        'surname': request.user.last_name,
        'email': request.user.email,
        'reservation_list': reservation_list
    }

    return render(request, 'main/profile_page.html', context)

def reserve(request, tour_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/main/login/')

    tour_list = models.Tour.objects.all()
    my_tour = tour_list.get(pk=tour_id)
    country = my_tour.country
    country_tours = tour_list.filter(country=country)

    if len(models.Reservation.objects.all().filter(tour=my_tour).filter(user=request.user))==0:
        new_reservation = models.Reservation(tour=my_tour, user=request.user)
        new_reservation.save()
        print('Тур зарезервирован')
    return HttpResponseRedirect('/main/tours/direction/'+country)

def delete_reserve(request, reserve_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect

    models.Reservation.objects.all().get(pk=reserve_id).delete()

    return HttpResponseRedirect('/main/profile/')

def stat(request, country):
    tour_list = models.Tour.objects.all()
    approved_reservations = models.Reservation.objects.all().filter(approved=True)
    sold_tours = []

    for reservation in approved_reservations:
        if reservation.tour.country == country:
            sold_tours.append(reservation.tour)

    context = {
        'tours': tour_list,
        'sold_tours': sold_tours
    }
    return render(request, 'main/stat_page.html', context)

def choose_stat(request):
    tour_list = models.Tour.objects.all()

    context = {
        'tours': tour_list
    }
    return render(request, 'main/choose_stat.html', context)