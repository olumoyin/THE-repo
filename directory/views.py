from django.shortcuts import render

from rest_framework.viewsets import generics
from common import permissions as custom_permissions

from directory.models import ServiceLocation
from directory.serializers import ServiceLocationCreateSerializer, ServiceLocationSerializer
from rest_framework import permissions
from directory.utils import haversine_distance





class ServiceLocationList(generics.ListAPIView):
    queryset = ServiceLocation.objects.all()
    serializer_class = ServiceLocationSerializer
    permission_classes = []

    def get_queryset(self):
        '''
            Looks for query parameters(lat, lng) in the URL and filters the queryset 
            with SL in close proximity[default = 10km] to the passed in location coordinates.
            Returns the whole dataset if query parameters are invalid or absent 
        '''
        try:
            q_lat = float(self.request.GET.get('lat'))
            q_lng = float(self.request.GET.get('lng'))
            query_coordinates = (q_lat, q_lng)    
        except:
            query_coordinates = None
        
        if query_coordinates:
            max_distance_km = 5
            close_results = []

            for location in ServiceLocation.objects.all():
                location_coordinate = (float(location.latitude), float(location.longitude))
                # Calculate a maximum distance (e.g., 10 kilometers)
                distance = haversine_distance(query_coordinates, location_coordinate)
            
                if distance <= max_distance_km:
                    # If the location is within the specified distance, add it to close_results
                    # TODO location.distance = distance  # Store distance in the object for reference('This service location is {distance} kilometers away')
                    close_results.append(location)
            
            print("Result size: ", len(close_results))
            return close_results
        
        return super().get_queryset()
    

    
class ServiceLocationCreateView(generics.CreateAPIView):
    queryset = ServiceLocation.objects.all()
    serializer_class = ServiceLocationCreateSerializer
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsWispOperator]
    

    
