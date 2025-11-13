
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'recommended-movies', views.RecommendedMovieViewSet, basename='recommendedmovie')


urlpatterns = [
    path('', views.home, name='home'),
    path('movie_list/', views.movie_list, name='movie_list'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_movie, name='add_movie'),
    path('watching/', views.watching, name='watching'),
    path('watched/', views.watched, name='watched'),
    path('get_data/', views.get_data, name='get_data'),
    path('delete/', views.delete_movie, name='delete_confirm'),
    path('reviewData/', views.reviewData, name='reviewData'),
    path('delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('edit/<int:movie_id>/', views.edit_movie, name='edit_movie'), 
    path('add_review/<int:movie_id>/', views.add_review, name='add_review'),
    path('edit_review/<int:movie_id>/', views.edit_review, name='edit_review'),
    path('movies/<int:movie_id>/update_status/', views.update_status, name='update_status'),
    path('get_movies_api/', views.get_movies_api, name='get_movies_api'),
    path('explore/', views.explore, name='explore'),
    # path('profile_create/', views.profile_create, name='profile_create'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('followRequest/', views.followRequest, name='followRequest'),
    path('UnfollowRequest/', views.UnfollowRequest, name='UnfollowRequest'),
    path('profile_data/', views.profile_data, name='profile_data'),
    path('search/', views.search, name='search'),
    path('AISuggestions/', views.AISuggestions, name='AISuggestions'),
    path('explore/analysis/', views.analysis, name='analysis'),
    path('search/', views.search, name='search'),
    path('reaction/', views.reaction, name='reaction'),
]


#Including DRF router URLs at the end
urlpatterns += [
    path('api/', include(router.urls)),
]