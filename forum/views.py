from rest_framework.response import Response
from rest_framework.decorators import api_view 


@api_view(["GET"])
def topics_view(request):
    '''
    Returns the topics view of the forum app
    '''

    return Response({"message": "Welcome to the topics route of wisp forum"})
