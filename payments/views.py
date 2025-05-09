from django.shortcuts import render, get_object_or_404
import stripe
from django.conf import settings
from django.http import JsonResponse
from Courses.models import Course, Enrollment
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def payments(request):
    """
    Handles payment requests by retrieving the course ID from the request, 
    fetching the corresponding course object, and rendering the payments template.

    Args:
        request: The HTTP request object containing the course ID.

    Returns:
        A rendered HTML response with the payments template and course context.
    """
    course_id = request.GET.get("course_id")
    course = get_object_or_404(Course, id=course_id)

    context = {"course": course}
    return render(request, "payments.html", context)


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def create_checkout_session(request, course_id):
    course = Course.objects.get(id=course_id)

    # Create a Checkout session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': course.title,
                    'description': course.description,
                },
                'unit_amount': int(course.price * 100),  # Stripe expects the price in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(f"{reverse('payments:success')}?course_id={course_id}"),  # Pass course_id
        cancel_url=request.build_absolute_uri(reverse('payments:cancel')),
    )

    return JsonResponse({
        'id': checkout_session.id
    })

# 500636026177885273260561599432254783725
# @login_required
def success(request):
    course_id = request.GET.get('course_id')  # Retrieve course_id from query params
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    # Check if the user is already enrolled
    if Enrollment.objects.filter(user=user, course=course).exists():
        return render(request, 'success.html', {'message': 'You are already enrolled in this course.'})

    # Create the enrollment
    Enrollment.objects.create(user=user, course=course)
    return render(request, 'success.html', {'message': 'Enrollment successful!'})

def cancel(request):
    return render(request, 'cancel.html')
