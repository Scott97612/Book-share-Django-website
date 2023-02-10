from django.urls import path
from . import views

app_name = 'content'
urlpatterns = [
    path('',views.index, name='index'),
    path('titles/',views.titles, name='titles'),
    path('titles/<int:title_id>/',views.book,name='book'),
    path('new_book/',views.new_book, name='new_book'),
    path('new_entry/',views.new_entry, name='new_entry'),
    path('edit_title/',views.edit_title,name='edit_title'),
    path('edit_entry/',views.edit_entry,name='edit_entry'),
]