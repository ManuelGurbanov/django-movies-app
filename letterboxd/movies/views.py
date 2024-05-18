from django.shortcuts import render, redirect
from .models import Movie
from .forms import MovieForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    order_by = request.GET.get('order_by', 'name')
    movies = Movie.objects.all().order_by(order_by)
    ratings = MovieRating.objects.filter(user=request.user)
    director = Movie.director

    context = {
        'movies': movies,
        'ratings': ratings,
        'order_by': order_by,
        'director': director,
    }

    return render(request, 'movies/home.html', context)

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MovieForm()

    return render(request, 'movies/add_movie.html', {'form': form})

#

    
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return redirect('home')
    

from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)  # Debug print statement for form errors
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        return response

    def get_success_url(self):
        return reverse_lazy('login')




#Login
class OptionalLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Nombre o Contraseña icorrectos")
        return super().form_invalid(form)
    

#Puntuación de Películas
from django.shortcuts import  get_object_or_404

@login_required(login_url='login')  # Ensure users are authenticated
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    ratings = MovieRating.objects.filter(movie=movie)
    user_rating = ratings.filter(user=request.user).first()

    context = {
        'movie': movie,
        'ratings': ratings,
        'user_rating': user_rating,
    }

    return render(request, 'movies/movie_detail.html', context)

from .models import MovieRating
@login_required(login_url='login')  # Ensure users are authenticated
def rate_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    score = int(request.POST['rating'])
    # Create or update the rating
    rating, created = MovieRating.objects.get_or_create(movie=movie, user=request.user)
    rating.score = score
    rating.save()

    return redirect('movie_detail', movie_id=movie.id)