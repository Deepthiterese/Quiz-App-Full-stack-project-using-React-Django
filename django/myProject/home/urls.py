from django.urls import path
from .views import UserRegistrationView
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import TokenValidation
from .views import CourseDetailAPIView
from .views import CourseCreateView
from .views import QuizListView
from .views import UserLoginView
from .views import QuizQuestionsByCourseView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('api/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/validity/', TokenValidation.as_view(), name='validated-view'),
    path('courses/', CourseCreateView.as_view(), name='course-list'),
    path('courses/<slug:slug>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('quiz/', QuizListView.as_view(), name='quiz-detail'),
    path('api/quiz-questions/<slug:slug>/', QuizQuestionsByCourseView.as_view(), name='quiz_questions_by_course'),
]