from django.shortcuts import render, get_object_or_404
from Courses.models import Course


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
