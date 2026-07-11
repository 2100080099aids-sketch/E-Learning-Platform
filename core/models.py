from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.CharField(max_length=100, default="Unknown")
    category = models.CharField(max_length=100, default="General")
    duration = models.CharField(max_length=50, default="0 Hours")
    rating = models.FloatField(default=4.5)
    price = models.IntegerField()

    image = models.ImageField(
        upload_to="course_images/",
        blank=True,
        null=True
    )

    students = models.ManyToManyField(
        User,
        blank=True,
        related_name="enrolled_courses"
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    duration = models.CharField(max_length=20)

    order = models.PositiveIntegerField(default=1)

    video = models.FileField(
        upload_to="lesson_videos/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class LessonProgress(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE
    )

    completed = models.BooleanField(default=False)

    completed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"
class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
class Review(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveIntegerField(default=5)

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
class Quiz(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    question = models.CharField(max_length=300)

    option1 = models.CharField(max_length=200)

    option2 = models.CharField(max_length=200)

    option3 = models.CharField(max_length=200)

    option4 = models.CharField(max_length=200)

    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question 
class QuizResult(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    score = models.IntegerField(default=0)

    completed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"