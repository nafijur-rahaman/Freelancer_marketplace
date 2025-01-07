# rest framework modules
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# registration and login modules
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

# modules of project
from .models import UserModel, UserRole, JobPost
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from django_filters.rest_framework import DjangoFilterBackend

# for sending email modules
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your views here.

# User list api
from .permissions import IsAdmin, IsClient


from rest_framework.permissions import IsAuthenticated

class UserApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]  # Use OR condition
    queryset=UserModel.objects.all()
    serializer_class = UserSerializer





# user registration view
class UserRegistrationApiView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)  # user details store in serializer

        if serializer.is_valid():
            user = serializer.save()  # save serializer in database
            token = default_token_generator.make_token(user)  # generate token of user
            uid = urlsafe_base64_encode(force_bytes(user.pk))  # more specified the confirmation link

            confirm_link = f"https://freelancer-marketplace-5lqt.vercel.app/api/active/{uid}/{token}"  # link send for confirm
            email_subject = "Confirm Registration"

            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()

            return Response("Check email for confirmation")
        return Response(serializer.errors)


# activate view when user click the link
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)

    except (User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # account active
        user.save()
        return redirect('login')
    else:
        return redirect('register')


# user login view
class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=self.request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user:
                try:
                    user_data = UserModel.objects.get(user=user)
                    refresh = RefreshToken.for_user(user)  # Generate JWT tokens
                    login(request, user)  # Log in the user

                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user_id': user_data.id,
                    })
                except UserModel.DoesNotExist:
                    return Response({'error': "User data not found"})
            else:
                return Response({'error': "Invalid credentials"})
        return Response(serializer.errors)


# user logout view
class UserLogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
                logout(request)
                return Response({'message': 'Logout successful'})
            except Exception as e:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)



class JobPostViewSet(viewsets.ModelViewSet):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author']
    permission_classes = [IsClient]  # Ensure the user is authenticated

    def perform_create(self, serializer):
        # Get the logged-in user from the request
        user = self.request.user

        # Ensure the user exists in the UserModel table
        try:
            user_model_instance = UserModel.objects.get(user=user)  # Get the UserModel instance
            # Save the JobPost with the UserModel instance as the author
            serializer.save(author=user_model_instance)
        except UserModel.DoesNotExist:
            raise ValueError("The logged-in user does not exist in the UserModel table.")
    