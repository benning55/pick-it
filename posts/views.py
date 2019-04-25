from django.shortcuts import render

posts = [
    {
        'owner': 'Benning',
        'model': 'Yamaha yzf-r3 2019',
        'date_post': '25/04/2019',
        'prices': [{
            'hour': 50,
            'day': 100,
            'week': 1000,
            'month': 5000
        }],
        'pic': 'images/r3.jpg'
    },
    {
        'owner': 'Muse',
        'model': 'Yamaha yzf-r15 2017',
        'date_post': '25/04/2019',
        'prices': [{
            'hour': 50,
            'day': 100,
            'week': 1000,
            'month': 5000
        }],
        'pic': 'images/r15.jpg'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'posts/home.html', context=context)


def about(request):
    return render(request, 'posts/about.html')
