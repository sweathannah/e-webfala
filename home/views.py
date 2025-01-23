from django.shortcuts import render

# Create your views here.



def home(request):
    courses = [
        {
            "id": 1,
            "title": "Web Development Masterclass",
            "description": "Learn to build modern, responsive websites...",
            "price": 4400,
            "image_url": "https://placehold.co/400x225",
        },
        {
            "id": 2,
            "title": "Backend Development Bootcamp",
            "description": "Dive deep into server-side development...",
            "price": 5500,
            "image_url": "https://placehold.co/400x225",
        },
        {
            "id": 3,
            "title": "Frontend Development Bootcamp",
            "description": "Learn to build modern, responsive websites...",
            "price": 4400,
            "image_url": "https://placehold.co/400x225",
        },
    ]
    return render(request, "home.html", {"courses": courses})
