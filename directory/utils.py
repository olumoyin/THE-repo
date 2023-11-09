import json
import uuid
import random
import math

from users.models import CompanyProfile
from .models import ServiceLocation

# Import GeoJSON files as dict
# from SL_Data.current_received_data.geo_data import *


class ParseGeoJSON():
    '''
    Contains functions for parsing the geo_json data acquired from different
    wisp operator. 
    Functions named after an operator are tailored to retrieve the appropriate 
    data from the geo_json file gotten from them
    '''

    def get_address(self, feature: dict) -> str:
        '''
        This gets the whole address in the MTN P2P GeoJSON data file
        '''
        # Get a dict
        feature = feature
        # Get its properties field
        props = feature['properties']
        # Get its 1st name, Address1, Address2, Town and state values
        name, address1, address2, town, state = props['1st_Name'], props['Address_1'], props['Address_2'], props['Town'], props['State']
        # Put these values in a list
        address_values = [name, address1, address2, town, state]
        # Remove Nones from the list
        while None in address_values:
            address_values.remove(None)
        while "None" in address_values:
            address_values.remove("None")
        
        # Create an address variable
        address =""
        
        # Return addres if list is empty
        if len(address_values) == 0:
            return address
        
        # List not empty
        for item_index in range(len(address_values)):
            # Try concatenating address values
            item = address_values[item_index]
            # Check if item isn't the last on the list
            if item_index != (len(address_values)-1):
                # Get next item
                next_item = address_values[item_index+1].lower().strip()
            else:
                next_item = ""
            # If the current value.lower().strip() is the same with the next.lower().strip() skip
            if item.lower().strip() == next_item:
                continue
            else:
                # else concatenate it to address
                address += f", {item}"

        return address[2:]

    def fiam(file: dict, upto: int=None) -> None:
        '''
        Reads the provided dict(in geojson format) and write a list of service locations 
        dictionaries with its data into JSON a file named <OperatorName_Service_data.txt>
        '''
        sl = {
            'id' : None,
            'description' : None,
            'operator' : None,
            'address' : None,
            'latitude' : None,
            'longitude' : None,
            'service' : None,
            'speed' : None,
        }
        filepath = "SL_Data/" + file["name"]+"_data.json"
        op_name = file["name"].split('_')[0].upper()

        print(f"filepath: {filepath}")
        print(f"Operator name: {op_name}")

        if type(upto) == int and upto <= len(file['features']):
            upto = upto
        else:
            upto = len(file['features'])

        service_locations = []

        for feature in file['features'][:upto]:
            sl['id'] = str(uuid.uuid4())
            sl['description'] = "Nigerian wireless ISP offering fast, reliable and affordable data to high-density, low income areas and rural communities."
            sl['operator'] = op_name
            sl['address'] = f"{feature['properties']['name ']}, {feature['properties']['state']}"
            sl['latitude'] = float(f"{feature['geometry']['coordinates'][1]}")
            sl['longitude'] = float(f"{feature['geometry']['coordinates'][0]}")
            sl['service'] = f"{feature['properties']['type'].lower()}"
            sl['speed'] = random.randint(35, 105)
            service_locations.append(sl.copy())
        
        with open(filepath, 'w') as json_file:  
            json.dump(service_locations, json_file, indent=4)
        print("Done")

    def legend(file: dict, upto: int=None) -> None:
        '''
        Reads the provided dict(in geojson format) and write a list of service locations 
        dictionaries with its data into JSON a file named <OperatorName_Service_data.txt>
        '''
        sl = {
            'id' : None,
            'description' : None,
            'operator' : None,
            'address' : None,
            'latitude' : None,
            'longitude' : None,
            'service' : None,
            'speed' : None,
        }
        filepath = "SL_Data/" + file["name"]+"_data.json"
        op_name = file["name"].split('_')[0].upper()

        print(f"filepath: {filepath}")
        print(f"Operator name: {op_name}")

        if type(upto) == int and upto <= len(file['features']):
            upto = upto
        else:
            upto = len(file['features'])

        service_locations = []

        for feature in file['features'][:upto]:
            sl['id'] = str(uuid.uuid4())
            sl['description'] = "Nigerian ISP offering fast, reliable and affordable network speeds to high-density cities through our vast network of fiber landings."
            sl['operator'] = op_name
            sl['address'] = f"{feature['properties']['Name']}, {feature['properties']['town']}, {feature['properties']['state']}"
            sl['latitude'] = float(f"{feature['geometry']['coordinates'][1]}")
            sl['longitude'] = float(f"{feature['geometry']['coordinates'][0]}")
            sl['service'] = f"{feature['properties']['type'].lower()}"
            sl['speed'] = random.randint(40, 135)
            service_locations.append(sl.copy())
        
        with open(filepath, 'w') as json_file:  
            json.dump(service_locations, json_file, indent=4)
        print("Done")

    def voda(file: dict, upto: int=None) -> None:
        '''
        Reads the provided dict(in geojson format) and write a list of service locations 
        dictionaries with its data into JSON a file named <OperatorName_Service_data.txt>
        '''
        sl = {
            'id' : None,
            'description' : None,
            'operator' : None,
            'address' : None,
            'latitude' : None,
            'longitude' : None,
            'service' : None,
            'speed' : None,
        }
        filepath = "SL_Data/" + file["name"]+"_data.json"
        op_name = file["name"].split('_')[0].upper()

        print(f"filepath: {filepath}")
        print(f"Operator name: {op_name}")

        if type(upto) == int and upto <= len(file['features']):
            upto = upto
        else:
            upto = len(file['features'])

        service_locations = []

        for feature in file['features'][:upto]:
            sl['id'] = str(uuid.uuid4())
            sl['description'] = "We are an enterprise focus ICT subsidiary of the Vodacom Group and Africa's preferred Pan-African service provider"
            sl['operator'] = op_name
            sl['address'] = f"({feature['properties']['Name']}), {feature['properties']['address']}"
            sl['latitude'] = float(f"{feature['geometry']['coordinates'][1]}")
            sl['longitude'] = float(f"{feature['geometry']['coordinates'][0]}")
            sl['service'] = "p2p"
            sl['speed'] = random.randint(35, 105)
            service_locations.append(sl.copy())
        
        with open(filepath, 'w') as json_file:  
            json.dump(service_locations, json_file, indent=4)
        print("Done")

    def mtn(self, file: dict, upto: int=None) -> None:
        '''
        Reads the provided dict(in geojson format) and write a list of service locations 
        dictionaries with its data into a JSON file named <OperatorName_Service_data.json>
        '''
        sl = {
            'id' : None,
            'description' : None,
            'operator' : None,
            'address' : None,
            'latitude' : None,
            'longitude' : None,
            'service' : None,
            'speed' : None,
        }
        filepath = "SL_Data/" + file["name"] + "_data.json"
        op_name = file["name"].split('_')[0].upper()

        print(f"filepath: {filepath}")
        print(f"Operator name: {op_name}")

        if type(upto) == int and upto <= len(file['features']):
            upto = upto
        else:
            upto = len(file['features'])

        service_locations = []  
        
        for feature in file['features'][:upto]:
            sl["id"] = str(uuid.uuid4())
            sl["description"] = "Mtn is a well known telecommunications company that provides mobile network services in Nigeria"
            sl["operator"] = op_name
            sl["address"] = self.get_address(feature)
            sl["latitude"] = float(f"{feature['geometry']['coordinates'][1]}")
            sl["longitude"] = float(f"{feature['geometry']['coordinates'][0]}")
            sl["service"] = "p2p"
            sl["speed"] = random.randint(35, 105)
            service_locations.append(sl.copy()) 
        
        with open(filepath, 'w') as json_file: 
            json.dump(service_locations, json_file, indent=4) 

        print("Done")



def SaveServiceLocations(file_path, company_profile_pk):
    '''
    This function read a json file containing a list of service locations, loops
    through its content and saves each service location to the database.
    
    :param str file_path: The path to the JSON file with service locations.
    :param str company_profile_pk: The pk(UUID) of a company profile already in the db to make 
        a relation to the WISP Operator
    :return: None
    :rtype: None

    [
        {
            "id": "0b524487-f551-4f57-dlsa-e0c17324j2bf",
            "description": "Descriptionsss.",
            "operator": "FIAM",
            "address": "Asokoro, Abuja",
            "latitude": 6.45353635635531,
            "longitude": 5.3454252424247,
            "service": "wifi",
            "speed": 62
        },
        {
            "id": "7324k4b1-afeb-431e0-8310-177a7d19a0c0",
            "description": "descriptions",
            "operator": "MTN",
            "address": "Bimbo Cafe, Lagos",
            "latitude": 6.434435852633,
            "longitude": 3.54634885,
            "service": "wifi",
            "speed": 76
        }
    ]
    '''

    data = []
    invalids = []
    with open(file_path, 'r') as file:
        data =  json.load(file)

    try:
        op = CompanyProfile.objects.get(pk=company_profile_pk)
        print(f"Seeding with {op.name.upper()} data")
    except:
        report = f"Company profile not found. File skipped. "
        return report
     
    for item in data:
        try:
            object = ServiceLocation(
                                    id= str(uuid.uuid4()),
                                    description= item['description'],
                                    operator= op,
                                    address= item['address'],
                                    latitude= item['latitude'],
                                    longitude= item['longitude'], 
                                    service= item['service'],
                                    speed= item['speed']
                                    )
            try:
                object.save()
            except:
                print(f"Couldn't save data at index {data.index(item)}")
                # Append invalid data to invalids
                invalids.append(item)
        except:
            # Append invalid data to invalids
            print(f"Invalid data at index {data.index(item)}")
            invalids.append(item)

    report = f"Saved {len(data) - len(invalids)} items and had {len(invalids)} invalids"

    return report
        
        
# ---------  PARSE DATA    ---------

# ParseGeoJSON.fiam(fiam_wifi)
# ParseGeoJSON.legend(legend_fibre)
# ParseGeoJSON.voda(voda_p2p)

# geo_parser = ParseGeoJSON()
# geo_parser.mtn(mtn_p2p)


def haversine_distance(coord1, coord2):
    '''
    Calcluates the distance between two point on a sphere using the 
    haversine function 
    :return: int [distance] km
    '''
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Radius of the Earth in kilometers
    earth_radius = 6371

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    km = earth_radius * c
    m = km * 1000.0



    print(f"Distance: {m} m")
    print(f"Distance: {km} km")
    return km