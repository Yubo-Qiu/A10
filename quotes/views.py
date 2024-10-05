import random
from django.shortcuts import render

quotes = [
    "I'm being baked, I'm being baked like a cake.",
    "If I lose to him, I will never speak to you again!",
    "If we tested only million instead of 14 million we'd have far fewer cases.",
]

images = [
    "/static/quotes/images/1.png",
    "/static/quotes/images/2.png",
    "/static/quotes/images/3.png",
]


def quote(request):
    selected_quote = random.choice(quotes)
    selected_image = random.choice(images)
    context = {"quote": selected_quote, "image": selected_image}
    return render(request, "quotes/quote.html", context)


def show_all(request):
    context = {"quotes": quotes, "images": images}
    return render(request, "quotes/show_all.html", context)


def about(request):
    return render(request, "quotes/about.html")
