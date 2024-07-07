from rest_framework import viewsets, permissions, status, response
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Medication, MedicationLog
from .serializers import MedicationSerializer, UserSerializer, MedicationLogSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # filter to return meds for user 
        return Medication.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # connect medication to user before saving
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        # handle updates to medication making sure user is the same
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        # create a new med for user
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class MedicationLogViewSet(viewsets.ModelViewSet):
    queryset = MedicationLog.objects.all()
    serializer_class = MedicationLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # return medication log for current user 
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # create a med log 
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)

# Django's built in User model
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 

    def get_permissions(self):
        if self.action in ['create', 'token_obtain_pair', 'token_refresh']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    # method: dynamically sets the permissions based on action. Public endpoints like registering a user and getting tokens are set to allowAny and the other require authentication 

    def create(self, request, *args, **kwargs):
        # register a new user - validate and save user data 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # method: handles creation of new user. Validates and saves user data and returns new user data with 201 http status("The HTTP 201 Created success status response code indicates that the request has succeeded and has led to the creation of a resource." https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/201)

    @action(detail=False, methods=['get', 'put'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            if not serializer.is_valid():
                # Log the errors for debugging
                print(f"Profile update errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=['get', 'put'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        # manage user profile - retrieve or update user data
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        # action: a custom action to retrieve or update the authenticated user's profile. Responds based on the HTTP method (GET & PUT). 

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

class MyTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)
# both of these classes are custom classes that come from the rest_framework_simplejwt package.Setting AllowAny lets unauthenticated users get or refresh their tokens 


# https://dev.to/ki3ani/implementing-jwt-authentication-and-user-profile-with-django-rest-api-part-3-3dh9