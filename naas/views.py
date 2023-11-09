from rest_framework.response import Response
from rest_framework.decorators import api_view 


@api_view(["GET"])
def service_requests_view(request):
    '''
    Returns the service-request view of the naas app
    '''

    return Response({"message": "Welcome to the service-request route of naas app"})
