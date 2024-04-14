from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from autoslug import AutoSlugField

class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(unique=True)

    def __str__(self):
        return self.username
    

class Course(models.Model):
    course_name = models.CharField(max_length=250, unique=True)
    slug = AutoSlugField(populate_from='course_name', unique=True, always_update=True, null=True)
    course_price = models.CharField(max_length=10, default=None)
    course_offer_price = models.CharField(max_length=10, default=None)
    course_description = models.TextField()
    course_type = models.CharField(max_length=10, choices=[('paid', 'Paid'), ('free', 'Free')])  # True for Paid, False for Unpaid
    course_status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    thumbnail = models.ImageField(
        upload_to=course_name,
        blank=True,
        null=True, 
        default='course/default.png'
    )
    
    create_at = models.DateField(null=True, blank=True, auto_now=True)
    update_at = models.DateField(null=True, blank=True, auto_now=True)
    delete_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.course_name}"



class Quizzes (models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    quiz_title= models.CharField(max_length=50, default=None)
    description = models.TextField()
    time_limit = models.IntegerField()
    randomize_questions = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No')])
    attempts_allowed= models.IntegerField()

    
    slug = AutoSlugField(populate_from='quiz_title', unique=True, null=True)

    
    def __str__(self):
        return f"Quiz on {self.course_id}"
    


        
class QuizQuestions(models.Model):
    quiz_id = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=3, choices=[('MCQ', 'Multiple Choice Question'),('TF', 'True/False Question'),('SA', 'Short Answer Question')])
    points= models.CharField(max_length=50, default=None)
  
   

    def __str__(self):
        return f"{self.question_text}"


class QuizChoices(models.Model):
    
    question = models.ForeignKey(QuizQuestions, on_delete=models.CASCADE,related_name='choices')
    choice_text = models.TextField()
    is_correct = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No')])
    
    def __str__(self):
        return f"{self.choice_text} ({'Correct' if self.is_correct == 'yes' else 'Incorrect'})"

    
class QuizAttendance (models.Model):
    user_id   = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz_id   = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    start_time= models.DateTimeField(auto_now_add=True)
    end_time= models.DateTimeField(auto_now=True)
    score=models.CharField(max_length=10)
    status=models.CharField(max_length=50, choices=[('in_progress', 'in_progress'), ('completed', 'completed')])
    
    def __str__(self):
        return f"{self.status} - {self.user_id.username}'s - Quiz on  {self.quiz_id.quiz_title}"


