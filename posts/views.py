from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView
from .models import Car, Image, Price, Renting
from .form import CarRegisterForm, ImageCarRegisterForm, PriceCarRegisterForm, ReviewCarForm, RentingCarForm



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

