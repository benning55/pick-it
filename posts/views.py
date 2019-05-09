from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView
from .models import Car, Image, Price, Renting, Contract, Report
from .form import CarRegisterForm, ImageCarRegisterForm, PriceCarRegisterForm, ReviewCarForm, RentingCarForm, \
    CarUpdateForm, ImageUpdateForm, PriceUpdateForm, ReportForm
import re

def home(request):
    context = Car.objects.all()
    paginator = Paginator(context, 2)  # Show 25 contacts per page
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'posts/home.html',{'contacts': contacts})


class PostListView(ListView):
    model = Car
    template_name = 'posts/home.html'
    context_object_name = 'cars'
    ordering = '-date_posted'


class PostDetailView(DetailView):
    model = Car
    template_name = 'posts/detail.html'



def detail(request, car_id):
    context = {}
    post = Car.objects.get(pk=car_id)
    if request.method == 'POST':
        review_form = ReviewCarForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.car = Car.objects.get(id=car_id)
            review.reviewer = request.user
            review.save()
            messages.success(request, f'You had just review {post.car_model}')
            return redirect('detail', car_id=car_id)
    else:
        context['post'] = post
        context['review_form'] = ReviewCarForm()

    return render(request, 'posts/detail.html', context=context)


@login_required
def rent_post(request, car_id):
    context = {}
    car = Car.objects.get(pk=car_id)
    if request.method == 'POST':
        renting_form = RentingCarForm(request.POST, request.FILES or None)
        current_user = request.user
        if renting_form.is_valid():
            start = renting_form.cleaned_data['date_time_start']
            end = renting_form.cleaned_data['date_time_end']
            final = end - start
            rent = renting_form.save(commit=False)
            rent.user = current_user
            rent.car = car
            rent.time_use = final
            rent.save()
            current_site = get_current_site(request)
            mail_subject = 'Someone want to rent your car!' + car.owner.username
            message = render_to_string('posts/mail_notify.html', {
                'user': current_user,
                'domain': current_site.domain,
                'car': car,
                'rent': rent.id
            })
            to_email = car.owner.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, f'Your Car has been register')
            return redirect('rent_post', car_id)
        else:
            messages.error(request, f'The form is not correct')
            return redirect('rent_post', car_id)
    else:
        context['renting_form'] = RentingCarForm()

    return render(request, 'posts/rent_post.html', context=context)


def rent_decide(request, rent_id):
    context = {}
    rented = Renting.objects.get(pk=rent_id)

    total = rented.time_use.total_seconds()
    real_time = display_time(total, 3)

    car_owner = rented.car.price_set.all()
    for prices in car_owner:
        hour = prices.hour
        day = prices.day
        week = prices.week
        month = prices.month

    f = (re.findall('\d+', real_time))
    print(f)

    box = ""

    result = real_time.find('month')
    result1 = real_time.find('week')
    result2 = real_time.find('day')
    result3 = real_time.find('hour')

    total_money = 0

    if result > 0:
        box += 'm'

    if result1 > 0:
        box += 'w'

    if result2 > 0:
        box += 'd'

    if result3 > 0:
        box += 'h'

    if box == 'mwdh':
        total_money += month * int(f[0])
        total_money += week * int(f[1])
        total_money += day * int(f[2])
        total_money += hour * int(f[3])
    elif box == 'mwd':
        total_money += month * int(f[0])
        total_money += week * int(f[1])
        total_money += day * int(f[2])
    elif box == 'mwh':
        total_money += month * int(f[0])
        total_money += week * int(f[1])
        total_money += hour * int(f[2])
    elif box == 'mdh':
        total_money += month * int(f[0])
        total_money += day * int(f[1])
        total_money += hour * int(f[2])
    elif box == 'wdh':
      total_money += week * int(f[0])
      total_money += day * int(f[1])
      total_money += hour * int(f[2])
    elif box == 'wd':
      total_money += week * int(f[0])
      total_money += day * int(f[1])
    elif box == 'wh':
      total_money += week * int(f[0])
      total_money += hour * int(f[1])
    elif box == 'mw':
      total_money += month * int(f[0])
      total_money += week * int(f[1])
    elif box == 'md':
      total_money += month * int(f[0])
      total_money += day * int(f[1])
    elif box == 'mh':
      total_money += month * int(f[0])
      total_money += hour * int(f[1])
    elif box == 'dh':
      total_money += day * int(f[0])
      total_money += hour * int(f[1])
    elif box == 'm':
      total_money += month * int(f[0])
    elif box == 'w':
      total_money += week * int(f[0])
    elif box == 'd':
      total_money += day * int(f[0])
    elif box == 'h':
      total_money += hour * int(f[0])


    context['long'] = real_time
    context['total_money'] = total_money
    context['rented'] = rented

    return render(request, 'posts/rent_decide.html', context=context)


intervals = (
    ('month', 2419200), # 60 * 60 * 24 * 7 * 4
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )


def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(int(value), name))
    return ', '.join(result[:granularity])


def rent_accept(request, rent_id):
    context = {}
    rented = Renting.objects.get(pk=rent_id)
    rents = Renting.objects.all()
    count = 0
    for rent in rents:
        if rent.user == rented.user and rent.car == rented.car:
            count += 1
    if count < 1:
        Contract.objects.create(
            user=rented.user,
            car=rented.car,
            status='1'
        )

    current_site = get_current_site(request)
    mail_subject = 'Your request have been accept'
    message = render_to_string('posts/mail_accept.html', {
        'user': rented.user,
        'domain': current_site.domain,
        'car': rented.car,
        'phone': rented.car.owner.profile.phone
    })
    to_email = rented.user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    context['rented'] = rented.car

    return render(request, 'posts/rent_status.html', {'context': context, 'status': 'You have been accept thank you for using us!'})


def rent_decline(request, rent_id):
    rented = Renting.objects.get(pk=rent_id)
    current_site = get_current_site(request)
    mail_subject = 'Your request have been decline'
    message = render_to_string('posts/mail_decline.html', {
        'user': rented.user,
        'domain': current_site.domain,
        'car': rented.car,
        'phone': rented.car.owner.profile.phone
    })
    to_email = rented.user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()

    return render(request, 'posts/rent_status.html', {'status': 'You have decline the request thank you for your time.'})


@login_required
def create_post(request):
    context = {}
    ImageCarRegisterFormSet = formset_factory(ImageCarRegisterForm, extra=6, max_num=6)
    if request.method == 'POST':
        car_form = CarRegisterForm(request.POST)
        image_form = ImageCarRegisterFormSet(request.POST, request.FILES or None)
        price_form = PriceCarRegisterForm(request.POST)
        current_user = request.user

        if car_form.is_valid():
            car = car_form.save(commit=False)
            car.owner = User.objects.get(id=current_user.id)
            car.save()
            if image_form.is_valid():
                for img in image_form:
                    Image.objects.create(
                        path=img.cleaned_data.get("path"),
                        car=car
                    )
            if price_form.is_valid():
                Price.objects.create(
                    hour=price_form.cleaned_data['hour'],
                    day=price_form.cleaned_data['day'],
                    week=price_form.cleaned_data['week'],
                    month=price_form.cleaned_data['month'],
                    car=car
                )
                messages.success(request, f'Your Car has been register')
    else:
        car_form = CarRegisterForm()
        image_form = ImageCarRegisterFormSet()
        price_form = PriceCarRegisterForm()

    context['car_form'] = car_form
    context['image_form'] = image_form
    context['price_form'] = price_form

    return render(request, 'posts/new_post.html', context=context)


def about(request):
    return render(request, 'posts/about.html')


def delete(request, car_id):

    car = Car.objects.get(pk=car_id)

    car.delete()

    return redirect('profile')


def update(request, car_id):

    cars = Car.objects.get(pk=car_id)
    prices = Price.objects.select_related().filter(car=cars.id).first()
    ImageFormSet = formset_factory(ImageCarRegisterForm, extra=5, max_num=10)

    if request.method == 'POST':
        car_form = CarRegisterForm(request.POST, instance=cars)
        image_form = ImageFormSet(request.POST, request.FILES or None)
        price_form = PriceCarRegisterForm(request.POST, instance=prices)
        if car_form.is_valid() and price_form.is_valid():
            cared = car_form.save(commit=False)
            cared.owner = cars.owner
            cared.save()
            priced = price_form.save(commit=False)
            priced.car = cars
            priced.save()
            if image_form.is_valid():
                for img_form in image_form:
                    if img_form.cleaned_data.get('image_id'):
                        img = Image.objects.get(id=img_form.cleaned_data.get('image_id'))
                        if img:
                            img.path = img_form.cleaned_data.get('path')
                            img.save()
                    else:
                        if img_form.cleaned_data.get('path'):
                            Image.objects.create(
                                path=img_form.cleaned_data.get('path'),
                                car=cars
                            )

            messages.success(request, f'Your post has been updated!')
            return redirect('update', cars.id)

    else:
        car_form = CarRegisterForm(instance=cars)

        data = []

        for img in cars.image_set.all():
            data.append(
                {
                    'path': img.path,
                    'image_id': img.id
                }
            )
        print(data)
        price_form = PriceCarRegisterForm(instance=prices)

        image_form = ImageFormSet(initial=data)

    context = {
        'car_form': car_form,
        'image_form': image_form,
        'price_form': price_form
    }
    return render(request, 'posts/update.html', context)


def report(request, car_id):

    cars = Car.objects.get(pk=car_id)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            Report.objects.create(
                type=form.cleaned_data.get('type'),
                text=form.cleaned_data.get('text'),
                reported=cars
            )
            messages.success(request, f'Your Report has been sent')
            return redirect('report', car_id)
    else:
        form = ReportForm()

    context = {
        'form': form
    }

    return render(request, 'posts/report.html', context=context)

