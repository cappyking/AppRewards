from functools import partial
from urllib import response
from prompt_toolkit import Application
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.decorators import *
from myapp.serializers import *
from .models import AppLib, MasterTaskHolder
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView

# api for login as admin and adding tasks
class adminops(APIView):
    @permission_classes([IsAdminUser])
    def get(self, request, format=None):
        apps = AppLib.objects.all()
        serializer = AppSerializer(apps, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AdminTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Saved")

#api for user operations. GET for getting all tasks and related data while PUT is uploading image proofs
class userops(APIView):
    permission_classes([IsAuthenticated])

    def put(self, request, format=None):
        app = MasterTaskHolder.objects.get(
            title=request.data['title'], user=request.user)
        serializer = ImageUploadSerializer(
            app, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(app, serializer.validated_data)
        return Response("Posted")

    def get(self, request, format=None):
        user = request.user
        apps = MasterTaskHolder.objects.filter(user=user)
        totalpoints = 0
        for app in apps:
            if (app.status == 'C'):
                totalpoints += app.point
        serializer = AppLogSerializer(apps, many=True)
        payload = {
            "Name": str(user),
            "Total Points": totalpoints,
            "Data": serializer.data
        }
        if app:
            return Response(payload)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

#api for login
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

# api for register

class RegisterAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

# General API to grab app does not require authentication adn permissions
@api_view(['GET'])
@permission_classes([AllowAny])
def getapps(request, id):
    try:
        app = AppLib.objects.get(pk=id)
        serializer = AppSerializer(app, many=False)
        if app:
            return Response(serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
