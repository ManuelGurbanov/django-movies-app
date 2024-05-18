from django.contrib import admin
from django.urls import path, include
from movies.views import home, add_movie, OptionalLoginView, CustomLogoutView, RegisterView
from movies.views import movie_detail, rate_movie
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('add_movie/', add_movie, name='add_movie'),
    path('login/', OptionalLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('<int:movie_id>/', movie_detail, name='movie_detail'),
    path('<int:movie_id>/rate/', rate_movie, name='rate_movie'),
]