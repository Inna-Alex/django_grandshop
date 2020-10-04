from rest_framework import viewsets

from .models import Category
from .serializers import CategorySerializer


# CRUD
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
