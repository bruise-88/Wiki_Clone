from django.urls import path, include

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.showpage, name="pagerequest"),
    path("/searchresults", views.search, name="search"),
    path("/newpage", views.newpage, name="newpage"),
    path("/editpage", views.editpage, name="editpage"),
    path("/randompage", views.randompage, name="randompage")
]
