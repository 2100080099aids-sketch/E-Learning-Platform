from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),

    path(
        "course/<int:course_id>/",
        views.course_detail,
        name="course_detail",
    ),

    path(
        "lesson/<int:lesson_id>/",
        views.lesson_detail,
        name="lesson_detail",
    ),

    path(
        "lesson/<int:lesson_id>/complete/",
        views.complete_lesson,
        name="complete_lesson",
    ),

    path(
        "enroll/<int:course_id>/",
        views.enroll,
        name="enroll",
    ),
    path(
    "certificate/<int:course_id>/",
    views.certificate,
    name="certificate",
    ),
    path(
    "wishlist/<int:course_id>/",
    views.toggle_wishlist,
    name="toggle_wishlist",
    ),
    path(
    "review/<int:course_id>/",
    views.add_review,
    name="add_review",
),

path(
    "quiz/<int:course_id>/",
    views.quiz,
    name="quiz",
),

]