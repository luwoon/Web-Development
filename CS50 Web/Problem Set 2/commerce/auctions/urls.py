from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('<int:listing_id>/', views.listing, name="listing"),
    path('<int:listing_id>/watchlist/', views.watchlist, name="watchlist"),
    path('<int:listing_id>/bid/', views.bid, name="bid"),
    path('<int:listing_id>/close_listing/', views.close_listing, name="close_listing"),
    path('watchlist/', views.watchlist_page, name="watchlist_page"),
    path('categories/', views.categories, name='categories'),
    path('categories/<str:category_name>/', views.category_listings, name='category_listings'),    
]
