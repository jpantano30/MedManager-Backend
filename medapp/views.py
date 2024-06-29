from rest_framework import viewsets, permissions, status
from .models import Medication
from .serializers import MedicationSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


import logging
logger = logging.getLogger(__name__)

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Medication.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        logger.info(f"Received data: {data}")
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    # def list(self, request, *args, **kwargs):
    #     logger.info(f"Headers: {request.headers}")
    #     logger.info(f"User: {request.user}")
    #     return super().list(request, *args, **kwargs)
    # # list method: Overridden to log request headers and the user making the request before the standard list operation (getting the list of medications).
    # # list = handling get requests intended to return a list 
    # # self = instance of class 
    # # request = http request object - hand meta data like headers, method used, who made request 
    # # *args & **kwargs = allow the method to accept an arbitrary number of positional and keyword arguments which can be passed to the method from other parts of the django app or from django
    # # the rest logs information - the headers of the request, the user who made the request
    # # calls the list method of the medicationViewSet class using super() 

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        logger.info(f"Received data: {data}")
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # manages instances of Django's built in User model
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'token_obtain_pair', 'token_refresh']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    # method: dynamically sets the permissions based on action. Public endpoints like registering a user and getting tokens are set to allowAny and the other require authentication 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    # method: handles creation of new user. Validates and saves user data and returns new user data with 201 http status("The HTTP 201 Created success status response code indicates that the request has succeeded and has led to the creation of a resource." https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/201)

    @action(detail=False, methods=['get', 'put'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        # action: a custom aaction to retrieve or update the authenticated user's profile. Responds based on the HTTP method (GET & PUT). 

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

class MyTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)
# both of these classes are custom classes that come from the rest_framework_simplejwt package.Setting AllowAny lets unauthenticated users get or refresh their tokens 