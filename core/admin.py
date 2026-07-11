from django.contrib import admin
from .models import (
    Course,
    Lesson,
    LessonProgress,
    Wishlist,
    Review,
    Quiz,
    QuizResult,
)

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(LessonProgress)
admin.site.register(Wishlist)
admin.site.register(Review)
admin.site.register(Quiz)
admin.site.register(QuizResult)