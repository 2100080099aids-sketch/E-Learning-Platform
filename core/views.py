from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, LessonProgress, Wishlist, Review
from .models import Quiz, QuizResult



def home(request):

    query = request.GET.get("q")

    if query:

        courses = Course.objects.filter(
            title__icontains=query
        )

    else:

        courses = Course.objects.all()

    return render(
        request,
        "home.html",
        {
            "courses": courses,
            "query": query,
        }
    )
@login_required(login_url="/login/")
def enroll(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    course.students.add(request.user)

    return redirect("/")
def course_detail(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    lessons = course.lessons.all().order_by("order")

    reviews = Review.objects.filter(course=course)

    return render(
        request,
        "course_detail.html",
        {
            "course": course,
            "lessons": lessons,
            "reviews": reviews,
        }
    )
def lesson_detail(request, lesson_id):

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id
    )

    return render(
        request,
        "lesson_detail.html",
        {
            "lesson": lesson
        }
    )
@login_required
def complete_lesson(request, lesson_id):

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id
    )

    LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={
            "completed": True
        }
    )

    return redirect(
        "lesson_detail",
        lesson_id=lesson.id
    )
@login_required
def certificate(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    total_lessons = course.lessons.count()

    completed_lessons = LessonProgress.objects.filter(
        user=request.user,
        lesson__course=course,
        completed=True
    ).count()

    if total_lessons == 0:
        progress = 0
    else:
        progress = int((completed_lessons / total_lessons) * 100)

    if progress < 100:
        return redirect("dashboard")

    return render(
        request,
        "certificate.html",
        {
            "course": course,
            "progress": progress
        }
    )
@login_required
def toggle_wishlist(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    wishlist_item = Wishlist.objects.filter(
        user=request.user,
        course=course
    )

    if wishlist_item.exists():

        wishlist_item.delete()

    else:

        Wishlist.objects.create(
            user=request.user,
            course=course
        )

    return redirect("/")
@login_required
def add_review(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":

        rating = request.POST["rating"]
        comment = request.POST["comment"]

        Review.objects.update_or_create(
            user=request.user,
            course=course,
            defaults={
                "rating": rating,
                "comment": comment,
            }
        )

    return redirect("course_detail", course_id=course.id)
@login_required
def quiz(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    questions = Quiz.objects.filter(course=course)

    if request.method == "POST":

        score = 0

        for question in questions:

            answer = request.POST.get(str(question.id))

            if answer == question.correct_answer:
                score += 1

        QuizResult.objects.update_or_create(
            user=request.user,
            course=course,
            defaults={
                "score": score
            }
        )

        return render(
            request,
            "quiz_result.html",
            {
                "course": course,
                "score": score,
                "total": questions.count()
            }
        )

    return render(
        request,
        "quiz.html",
        {
            "course": course,
            "questions": questions
        }
    )