from django.shortcuts import render

# Create your views here.
def custom_login_view(request):
    error_message = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            error_message = 'Invalid email or password'

    return render(request, 'accounts/login.html', {'error_message': error_message})
