from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createlisting, name="create"),
    path("<int:id>", views.item, name="item"),
    path("<int:id>/comments", views.comments, name="comments"),
    path("<int:id>/bidding", views.bidding, name="bidding"),
    path("<int:id>/bidclose", views.bidclose, name="bidclose"),
    path("watchlist", views.watchlists, name="watchlist"),
    path("category", views.category, name="category"),
    path("<int:id>/watch", views.watches, name="watch"),
    path("won", views.wonlist, name="won")
]
