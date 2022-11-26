from django.urls import path
from .views import (
    home,
    post_detail,
    post_create,
    post_update,
    post_delete
)

app_name = 'posts'


urlpatterns = [
    path("", home, name="home"),
    path('create/', post_create, name='post-create'),
    path("post/<int:id>/", post_detail, name="post-detail"),
    path('update/<int:id>/', post_update, name='post-update'),
    path('delete/<int:id>/', post_delete, name='post-delete')
]
