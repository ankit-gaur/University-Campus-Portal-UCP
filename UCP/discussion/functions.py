"""
Functions file for discussion app

consists of common functions used by both api.py and views.py file
"""
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render
from django.template import Context
from django.utils import timezone
from django.views.generic import View

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from login.models import UserProfile
import login.serializers as Serializers
from discussion.models import DiscussionThread
from discussion.serializers import DiscussionThreadSerializer
from UCP.constants import result, message
from UCP.settings import EMAIL_HOST_USER, BASE_URL


def add_discussion_thread(request):
    
    response = {}
    serializer = DiscussionThreadSerializer(data=request.POST)

    if serializer.is_valid():
        user_profile = UserProfile.objects.get(user = request.user)
        serializer.save(
            posted_by = user_profile,
            posted_at = timezone.now()
        )
        response["error"] = []
    else:
        response["error"] = serializer.errors
        
    return response
    
def get_discussion_list(request):
    
    response = {}
    
    threads = DiscussionThread.objects.all()
    serializer = DiscussionThreadSerializer(threads, many=True)

    response["data"] = serializer.data
    
    return response