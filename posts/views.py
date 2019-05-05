from django.contrib import messages
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


def home(request):
    context = {
        'posts': Car.objects.all()
    }
    return render(request, 'posts/home.html', context=context)


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
            rent = renting_form.save(commit=False)
            rent.user = current_user
            rent.car = car
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
    rented = Renting.objects.get(pk=rent_id)

    context = {}

    context['rented'] = rented

    return render(request, 'posts/rent_decide.html', context=context)


def rent_accept(request, rent_id):
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

    return render(request, 'posts/rent_status.html', {'status': 'You have been accept thank you for using us!'})


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
    ImageCarRegisterFormSet = formset_factory(ImageCarRegisterForm, extra=3, max_num=6)
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
    ImageFormSet = formset_factory(ImageCarRegisterForm, extra=2, max_num=10)

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

