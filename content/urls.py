from django.urls import path
from . import views


app_name = 'content'
urlpatterns = [
    path('',views.index, name='index'),
    path('titles/',views.titles, name='titles'),
    path('titles/<int:title_id>/',views.book,name='book'),
    path('new_book/',views.new_book, name='new_book'),
    path('new_entry/<int:title_id>/',views.new_entry, name='new_entry'),
    path('edit_title/<int:title_id>/',views.edit_title,name='edit_title'),
    path('edit_entry/<int:entry_id>/',views.edit_entry,name='edit_entry'),
    path('delete_title/<int:title_id>/',views.delete_title, name='delete_title'),
    path('delete_entry/<int:entry_id>/',views.delete_entry, name='delete_entry'),
    path('search/',views.Search.as_view(),name='search'),
    path('add_or_remove_favorite/<int:title_id>/',views.add_or_remove_favorite, name='add_or_remove_favorite'),
    path('my_favorite',views.my_favorite, name='my_favorite'),
]