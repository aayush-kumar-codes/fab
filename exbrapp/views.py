from rest_framework.response import Response
from rest_framework.views import APIView
from fabapp.models import User, Exhibition, ExhibitFab
from exbrapp.models import Exhibitor
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from exbrapp.serializers import (ExhibitorSerializer)
from exbrapp.permissions import IsExhibitor
from fabapp.serializers import UserDetailSerializer, ExhibitFabricators


class ExhibitorRequire(APIView):
    permission_classes = (IsAuthenticated, IsExhibitor)

    def post(self, request, format=None, pk=None):
        exhibhition = Exhibition.objects.get(pk=pk)
        serializer = ExhibitorSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save(user=self.request.user,
                            exhibition_id=exhibhition.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        serializer = Exhibitor.objects.filter(user=request.user)
        if serializer is not None:
            exhibhit = ExhibitorSerializer(serializer, many=True)
            return Response(exhibhit.data)
        else:
            return Response([])


class ExhibhitDetails(APIView):
    permission_classes = (IsAuthenticated, IsExhibitor)

    def get_object(self, pk):
        try:
            return Exhibitor.objects.get(pk=pk, user=self.request.user)
        except Exhibitor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        exi = self.get_object(pk)
        serailizer = ExhibitorSerializer(exi)
        return Response(serailizer.data)

    def put(self, request, pk, format=None):
        exi = self.get_object(pk)
        serializer = ExhibitorSerializer(exi, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        exi = self.get_object(pk)
        exi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Fabricatorslist(APIView):
    permission_classes = (IsAuthenticated, IsExhibitor)

    def get(self, request, format=None, pk=None):
        exi = ExhibitFab.objects.filter(exhibition_id=pk)
        serializer = ExhibitFabricators(exi, many=True)
        user_list = []
        for data in serializer.data:
            user = User.objects.get(id=data['user'])
            serial = UserDetailSerializer(user, many=False)
            user_list.append(serial.data)

        return Response(user_list)


class Fabricator_dt(APIView):
    permission_classes = (IsAuthenticated, IsExhibitor)

    def get(self, request, format=None, pk=None, user_pk=None):
        exi = ExhibitFab.objects.get(exhibition_id=pk, user_id=user_pk)
        serializer = ExhibitFabricators(exi, many=False)
        print(serializer.data)
        user = User.objects.get(id=serializer.data['user'])
        serial = UserDetailSerializer(user, many=False)
        return Response(serial.data)
