from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def index(request):
    '''
    Returns the index view of the jobs app
    '''

    return Response({"message": "Welcome to the index route for jobs"})
