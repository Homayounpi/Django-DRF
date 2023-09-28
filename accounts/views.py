from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializer import UserRegisterSerializer, UserSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator


class UserRegister(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)

            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


# a = {'username': 'ali', 'email': 'ali@gmail.com', 'password': 'root', 'password2': 'root'}

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()

    def list(self, request):
        srz_data = UserSerializer(instance=self.queryset,many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        srz_data = UserSerializer(instance=user)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        if user !=request.user:
            return Response({'message': 'you are not the owner'})
        srz_data = UserSerializer(instance=user, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        if user !=request.user:
            return Response({'message': 'you are not the owner'})
        user.is_active = False
        user.save()

        return Response({'message': 'user deactivated'}, status=status.HTTP_200_OK)


class UserViewSet2(viewsets.ViewSet):
    queryset = User.objects.all()

    def list(self, request):
        srz_data = UserSerializer(instance=self.queryset, many=True)
        return Response(data=srz_data.data)


class UserApi(APIView):
    """
        all user
    """
    def get(self, request):
        queryset = User.objects.all()
        # page_number = self.request.query_params.get('page', 1)
        # page_size = self.request.query_params.get('limit', 2)
        # paginator = Paginator(queryset, page_size)
        # srz_data = UserSerializer(instance=paginator.page(page_number), many=True)
        srz_data = UserSerializer(instance=queryset, many=True)
        return Response(data=srz_data.data)


class Large(PageNumberPagination):
    page_size = 2


class UserListApi(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = Large

