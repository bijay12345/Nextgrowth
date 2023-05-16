from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import RegisterSerializer
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    def get(self,request,format=None):
        return Response(template_name = 'users/register.html')
    
    def post(self, request):
        data = dict(request.POST.items())
        print(data)
        reg_serializer = RegisterSerializer(data=dict(request.POST.items()))
        if reg_serializer.is_valid():
            reg_serializer.save()
            return redirect("user-login")
        else:
            return Response({"error":reg_serializer.errors},template_name = 'users/register.html')


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    def get(self,request,format=None):
        return Response(template_name = "users/login.html")

    def post(self,request,format=None):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid Email or password.')
            return redirect('user-login')

def logout_view(request):
    logout(request)
    return redirect('user-login')
