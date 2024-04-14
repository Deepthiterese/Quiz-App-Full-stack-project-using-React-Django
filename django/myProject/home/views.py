from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer,QuizzesSerializer

from rest_framework.permissions import IsAuthenticated
from .models import Course,Quizzes
from django.core import mail
from django.core.mail import EmailMessage, get_connection
from .models import QuizAttendance,QuizChoices,QuizQuestions
from .serializers import CourseSerializer,QuizQuestionsSerializer,QuizChoicesSerializer,QuizAttendanceSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.http import Http404
from rest_framework.generics import ListAPIView



User = get_user_model()

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')

        user = CustomUser.objects.filter(email=email).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response_data = {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class TokenValidation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        return Response({"message": f"Welcome {username}"})




class CourseCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'slug'



    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    
#class QuizDetailView(APIView):
    #model=Quizzes,Course
  
    #def get(self, request,slug,*args, **kwargs):
       
       # course = get_object_or_404(Course, slug=slug)
       # quiz = Quizzes.objects.filter(course=course).first()
       # quizQuestion = QuizQuestions.objects.filter(quiz=quiz)
       # choices = QuizChoices.objects.filter(quiz=quiz)

        
       # data = {
           # 'course':Course.course_name,
            #'quiz': quizQuestion,
               # 'quizQuestion': {
                   # 'choices': [choice.choice_text for choice in choices]
                      # }
           # }
            
       ## return Response(serializer.data)
    
    
#class QuizDetailView(generics.RetrieveAPIView):
    #queryset = Quizzes.objects.all()
    #serializer_class = QuizzesSerializer
    #lookup_field = 'slug' 



#class QuizDetailView(APIView):
    #def get(self, request, *args, **kwargs):
        # Retrieve all quizzes
        #quizzes = Quizzes.objects.all()

        # Serialize the quizzes and their questions
        #serialized_quizzes = []
        #for quiz in quizzes:
            # Retrieve quiz questions related to the quiz
            #question_text = QuizQuestions.objects.filter(quiz_id=quiz)
            
            # Retrieve quiz choices related to the quiz questions
            ##data = {
                #'quiz_name': quiz.quiz_title,
                #'questions': QuizQuestionsSerializer(question_text, many=True).data,
                #'choices': [{'id': choice.id, 'choice_text': choice.choice_text} for choice in choice_text]
            ##serialized_quizzes.append(data)

        # Return the serialized quiz data
       # return Response(serialized_quizzes)

class QuizListView(generics.ListAPIView):
    queryset = Quizzes.objects.all()
    serializer_class = QuizzesSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Prefetch related quiz questions and choices using the correct relationship paths
        queryset = queryset.prefetch_related('quizquestions_set__choices')
        return queryset
    
    
#class QuizDetailView(APIView):
   # def get(self, request, quiz_id):
       # try:
           # quiz = Quizzes.objects.get(id=quiz_id)
           # serializer = QuizzesSerializer(quiz)
            #return Response(serializer.data)
       # except Quizzes.DoesNotExist:
           # raise Http404("Quiz does not exist")
    
class QuizQuestionsByCourseView(ListAPIView):
    serializer_class = QuizQuestionsSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        course = get_object_or_404(Course, slug=slug)
        return QuizQuestions.objects.filter(quiz_id__course_id=course)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)