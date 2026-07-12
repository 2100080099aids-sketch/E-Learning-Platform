from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.models import LessonProgress
from .models import Profile
from django.http import HttpResponse
from django.contrib.auth.models import User

def register(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("/")

    return render(request, "users/register.html")
def user_login(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("/")

    return render(request, "users/login.html")
def user_logout(request):

    logout(request)

    return redirect("/")
@login_required(login_url="/login/")
def dashboard(request):

    courses = request.user.enrolled_courses.all()

    course_progress = []

    for course in courses:

        total_lessons = course.lessons.count()

        completed_lessons = LessonProgress.objects.filter(
            user=request.user,
            lesson__course=course,
            completed=True
        ).count()

        if total_lessons > 0:
            progress = int((completed_lessons / total_lessons) * 100)
        else:
            progress = 0

        course_progress.append({
            "course": course,
            "progress": progress,
            "completed": completed_lessons,
            "total": total_lessons,
        })

    return render(
        request,
        "users/dashboard.html",
        {
            "course_progress": course_progress,
        }
    )
@login_required(login_url="/login/")
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "users/profile.html",
        {
            "profile": profile
        }
    )

def make_admin(request):
    user = User.objects.get(username="mani")

    user.is_staff = True
    user.is_superuser = True
    user.save()

    # Read the user again from the database
    user.refresh_from_db()

    return HttpResponse(
        f"""
        Username: {user.username}<br>
        is_staff: {user.is_staff}<br>
        is_superuser: {user.is_superuser}
        """
    )