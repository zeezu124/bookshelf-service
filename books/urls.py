from django.urls import path

from .views import LibraryViewSet

urlpatterns = [
    path("books/<str:user>", LibraryViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='books.user'),
    path("books/<str:user>/<str:b_id>", LibraryViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    }), name='books.user.b_id')
]
