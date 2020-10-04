from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Manufactor
from .serializers import ManufactorSerializer


class ManufactorAPIView(APIView):
    def get(self, request, pk=None):
        manufactors = Manufactor.objects.all() if pk is None else Manufactor.objects.filter(pk=pk)
        serializer = ManufactorSerializer(manufactors, many=True)
        return Response({"manufactors": serializer.data})

    def post(self, request):
        manufactor = request.data.get("manufactor")

        serializer = ManufactorSerializer(data=manufactor)
        if serializer.is_valid(raise_exception=True):
            manufactor_saved = serializer.save()
        return Response({"success": "Manufactor '{}' was created successfully".format(
            manufactor_saved.name)})

    # при обновлении
    def put(self, request, pk):
        saved_manufactor = get_object_or_404(Manufactor.objects.all(), pk=pk)
        data = request.data.get('manufactor')
        serializer = ManufactorSerializer(instance=saved_manufactor,
                                          data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            manufactor_saved = serializer.save()

        return Response({
            "success": "Manufactor '{}' updated successfully".format(
                manufactor_saved.name)
            })

    def delete(self, request, pk):
        manufactor = get_object_or_404(Manufactor.objects.all(), pk=pk)
        manufactor.delete()
        return Response({
            "message": "Manufactor with id '{}' has been deleted".format(pk)
            }, status=204)
