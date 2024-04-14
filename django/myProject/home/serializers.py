from rest_framework import serializers
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.mail import send_mail
from .models import Course,Quizzes,QuizQuestions,QuizChoices,QuizAttendance



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'first_name','last_name','phone_number')
        extra_kwargs = {'password': {'write_only': True}}

        def validate_email(self, value):
            if CustomUser.objects.filter(email=value).exists():
                raise ValidationError("This email address is already in use.")
                return value
    
    
        def send_welcome_email(email):
            subject = 'Welcome to Quizz App'
            message = 'Thank you for registering/login to our platform'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list=[email]
            send_mail(subject,message,from_email,recipient_list)



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_price', 'course_offer_price', 'course_description','course_type' ,'course_status','thumbnail','slug']
        read_only_fields = ['slug']


class QuizChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizChoices
        fields = ['id', 'choice_text', 'is_correct']



class QuizQuestionsSerializer(serializers.ModelSerializer):
    choices = QuizChoicesSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestions
        fields = ['id', 'question_text', 'choices']




class QuizzesSerializer(serializers.ModelSerializer):
    questions = QuizQuestionsSerializer(many=True, read_only=True, source='quizquestions_set')

    class Meta:
        model = Quizzes
        fields = ['id', 'quiz_title', 'questions']





        
class QuizAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttendance
        fields = '__all__'
        
        



