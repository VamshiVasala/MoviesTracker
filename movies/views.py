from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Movie, Review, Profile,RecommendedMovie,Reaction
from .forms import MovieForm
from django.http import JsonResponse
from .serializers import MovieSerializer,ReviewSerializer,ProfileSerializer,ReactionS 
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pdb
import json
from .Ai import newData
from django.db.models import OuterRef, Subquery
from .recommend import recommendation

@api_view(['GET'])
def get_movies_api(request):
    
    Allmovies = Movie.objects.filter(status='watched')
    movieExp = Movie.objects.filter(status='watched').exclude(user=request.user)
    reviewExp = Review.objects.all().exclude(user=request.user)
    reaction_data=Reaction.objects.filter(user=request.user)
    CountReaction=Reaction.objects.all()
    reactionSerializer=ReactionS(reaction_data,many=True)
    countserializer=ReactionS(CountReaction,many=True)
    serializer = MovieSerializer(Allmovies, many=True)
    serializerEmp = MovieSerializer(movieExp, many=True)
    serializerReview = ReviewSerializer(reviewExp, many=True)
    displayData=recommendMovies(request)
    displayDataSerializer=MovieSerializer(displayData,many=True)

    return Response({
            'movies': serializer.data,
            'reviews': serializerReview.data,
            'moviesExplore':serializerEmp.data,
            'reactions':reactionSerializer.data,
            'recommendedMovies':displayDataSerializer.data,
            'countserializer':countserializer.data
        })


def explore(request):
    return render(request, 'movies/explore.html')


@login_required
def home(request):  
    movies = Movie.objects.all().filter(user=request.user)
    return render(request, 'movies/home.html', {'movies': movies})


def movie_list(request):
    movies = Movie.objects.all().filter(user=request.user)
    return render(request, 'movies/movie_list.html', {'movies': movies})

# Sign Up
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup')
        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, bio='')
        login(request, user)
        return redirect('home')
    return render(request, 'movies/signup.html')


def profile(request, username):

    profile = get_object_or_404(Profile, user__username=username)

    movies= Movie.objects.all().filter(status='watched',user=profile.user_id)


    reviews_with_movie = (
        Review.objects.filter(user=profile.user_id)
        .annotate(
            movie_title=Subquery(
                movies.filter(id=OuterRef('movie_id')).values('title')[:1]
            ),
            movie_year=Subquery(
                movies.filter(id=OuterRef('movie_id')).values('year')[:1]
            ),
            movie_image=Subquery(
                movies.filter(id=OuterRef('movie_id')).values('image_url')[:1]
            ),
        )
        .values('id', 'opinion', 'stars', 'movie_title', 'movie_year', 'movie_image')
    )

    return render(request, 'movies/profile_view.html', {'profile': profile,'movies':reviews_with_movie})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'movies/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect
from .forms import MovieForm
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def add_movie(request):
    api=settings.TMDB_API_KEY
    context = {
        "tmdb_api_key": api
    }
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            
  
            return redirect('movie_list')
    else:
        form = MovieForm()  

    return render(request, 'movies/add_movie.html', {
    'form': form,
    'TMDB_API_KEY': api
})




@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        stars = int(request.POST.get("stars", 0))
        opinion = request.POST.get("opinion", "")
        Review.objects.create(movie=movie, user=request.user, stars=stars, opinion=opinion)
        data=newData(movie.genres,movie.cast)
        flat_data = []
        if data is None:
            
            data = []   
        for genre_list in data:
            flat_data.extend(genre_list)
        for movie_dict in flat_data:
            RecommendedMovie.objects.update_or_create(
                title=movie_dict.get("title", ""),
                user=request.user,  # save the current user
                recommend_for=movie,

                defaults={
                    "year_of_release": movie_dict.get("year_of_release", ""),
                    "short_synopsis": movie_dict.get("short_synopsis", ""),
                    "main_cast": ", ".join(movie_dict.get("main_cast_names", [])),
                    "poster_url": movie_dict.get("poster_url", ""),
                    "language":movie_dict.get("language"),
                    "typeOfFilm":movie_dict.get("type"),
                    "genre":movie_dict.get("genre")
                }
            )



        messages.success(request, f"✅ Review added for '{movie.title}'!")
        return redirect('watched')


def edit_review(request, movie_id):
    movie=get_object_or_404(Review, movie_id=movie_id)
    if request.method=='POST':
        movie.opinion=request.POST.get("opinion","")
        movie.stars=int(request.POST.get("stars",0))
        movie.save()
        return redirect('watched')

def movie_list(request):
    movies = Movie.objects.all().filter(user=request.user)
    return render(request, 'movies/movie_list.html', {'movies': movies})


from django.shortcuts import get_object_or_404

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('home')
    return render(request, 'movies/delete_confirm.html', {'movie': movie})


@login_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    form = MovieForm(request.POST, request.FILES, instance=movie)

    if request.method == 'POST': 

        if form.is_valid():
   
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)
    
    return render(request, 'movies/edit_movie.html', {'form': form})

 

@login_required
def update_status(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Movie.STATUS_CHOICES):
            movie.status = new_status
            movie.save()
        else:
            return redirect('movie_list')
    return render(request, 'movies/movieslist.html')



def watching(request):
    movies = Movie.objects.all().filter(user=request.user)
    movies=movies.filter(status='watching')
    return render(request, 'movies/watching.html', {'movies': movies})

def get_data(request):
    movies = Movie.objects.filter(status='watched',user=request.user).values('image_url','reviews','title','year','id')
    reviews = Review.objects.all().values('id','opinion', 'stars','movie_id')
    
    data = {
        'movies': list(movies),   
        'reviews': list(reviews),
    }
    return JsonResponse(data)


def watched(request):
    movies = Movie.objects.filter(user=request.user)
    reviews = Review.objects.all()

    return render(request, 'movies/watched.html', {'movies': movies, 'reviews': reviews})

def reviewData(request):
    reviews = Review.objects.all().values('id','opinion', 'stars','movie_id')
    
    data = {
        'reviews': list(reviews),
    }
    return JsonResponse(data)


def followRequest(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        requestProfile=body['requestProfile']
        profileUser=body['profileUser']
        follower = get_object_or_404(Profile, user__username=requestProfile)
        followed = get_object_or_404(Profile, user__username=profileUser)
        follower.following.add(followed)
        followed.followers.add(follower)
        followed.save()
        follower.save()
        return JsonResponse({'status': 'success', 'message': f'You are now following .'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    
def profile_data(request):
    profile = get_object_or_404(Profile, user__username=request.user.username)
    listOfFollowers = []

    if getattr(profile, 'followers', None):

        for follower in profile.following.all():
            listOfFollowers.append(follower.user.username)
    return JsonResponse({'followers': listOfFollowers})
    

def UnfollowRequest(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        requesUser=body['requestProfile']
        profileUser=body['profileUser']
        reqProfile=get_object_or_404(Profile,user__username=requesUser)
        profUser=get_object_or_404(Profile,user__username=profileUser)
        reqProfile.following.remove(profUser)
        profUser.followers.remove(reqProfile)
        profUser.save()
        reqProfile.save()
        return JsonResponse({'status': 'success', 'message': f'You have unfollowed .'})
    

def search(request):
    return render(request, 'movies/search.html')

def AISuggestions(request):
    data=RecommendedMovie.objects.all().filter(user=request.user)
    if data==None:
        return redirect('AISuggestions')
    return render(request, 'movies/AISuggestions.html', {'movies': data})

from rest_framework.pagination import PageNumberPagination

class TenPerPagePagination(PageNumberPagination):
    page_size = 10


from rest_framework import viewsets
from .models import RecommendedMovie
from .serializers import RecommendedMovieSerializer
from rest_framework.filters import SearchFilter, OrderingFilter

class RecommendedMovieViewSet(viewsets.ModelViewSet):
    serializer_class = RecommendedMovieSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    pagination=TenPerPagePagination
    search_fields = ['title', 'main_cast', 'language', 'genre']
    ordering_fields = ['year_of_release', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user  
        return RecommendedMovie.objects.filter(user=user)



def analysis(request):
    return render(request, 'movies/analysis.html')



def search(request):
    return render(request, 'movies/search.html')

@api_view(['POST'])
def reaction(request):
    body = request.data 

    movie_id = body.get('id')
    movie = get_object_or_404(Movie, id=movie_id)
    reaction, created = Reaction.objects.get_or_create(user=request.user)
    if body.get('flag')==True:    

        if movie in reaction.likedMovies.all():
            reaction.likedMovies.remove(movie)
        else:
            if movie in reaction.dislikedMovies.all():
                reaction.dislikedMovies.remove(movie)
            reaction.likedMovies.add(movie)

    else:

        if movie in reaction.dislikedMovies.all():
            reaction.dislikedMovies.remove(movie)
        else:
            if movie in reaction.likedMovies.all():

                reaction.likedMovies.remove(movie)
            reaction.dislikedMovies.add(movie)
    reaction.save()
    return JsonResponse({'status': 'success', 'message': 'Reaction recorded.'})


def recommendMovies(request):
    Usermovie = Movie.objects.filter(status='watched',user=request.user)
    RemMovie = Movie.objects.filter(status='watched').exclude(user=request.user)
    userGenres=[]
    userCast=[]
    for umovie in Usermovie:
        userGenres.append(umovie.genres)
        userCast.append(umovie.cast)

    remData=[]
    for r in RemMovie:
        movieData={
            'title':r.title,
            'genres':r.genres,
            'cast':r.cast,
            'id':r.id,
        }
        remData.append(movieData)


    recIds=recommendation(userGenres,userCast,remData)
    recMovies=[]
    for rid in recIds:
        recMovies.append(get_object_or_404(Movie, id=rid))
    return recMovies