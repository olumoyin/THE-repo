from rest_framework.response import Response
from rest_framework.decorators import api_view 


@api_view(["GET"])
def ticketing_view(request):
    '''
    Returns the ticketing view of the support 
    '''

    return Response({"message": "Welcome to the ticket route wisp support"})
