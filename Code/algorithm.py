import alphashape
import json
from shapely.geometry import Point, Polygon,LinearRing
import random
import time


#Global Varialbles
alpha_shapes = []
property_name = []
stored_map = []


def geofencing_enabled(geo):
    """
    The primary use of the function is to enable geofencing on the vehicle
    :param geo: status of geofence on the vehicle
    :return: The function returns a boolean value representing if geofencing is enabled on the vehicle
    """

    if geo == False:
        print("Geofence is now being enabled")
        geo = True
        return geo
    else:
        print("Geofence is enabled")
        return geo

def geofence_repository():
    """
    The function imports a geofence database and forms a alpha shape for each property. It stores the alpha shapes
    into a list.
    :return: The list with stored alpha shapes
    """

    # read file
    with open('sample.json', 'r') as myfile:
        map = json.load(myfile)

    # localvariables
    features = map["features"]

    # listing the properties , notes : properties data type is dictionary
    for i in range(len(features)):
        properties = map["features"][i]["properties"]
        # forming polygon for each of the features / building
        coordinates = map["features"][i]["geometry"]["coordinates"][0]
        for j in coordinates:
            property_name.append(properties)
            #the accuracy of the alpha shape can be adjusted, but imapcts the execution time
            #alpha_shape = Polygon(j)
            alpha_shape = alphashape.alphashape(j, 0.)
            alpha_shapes.append(alpha_shape)
    #storing the results of the algorithm
    results = zip(property_name, alpha_shapes)
    zipped_list = list(results)
    return zipped_list

def geofence_violation(location,stored_map):
    """
    The function checks if a geofence violation has been made. It check if the point of interest is within the alpha shape and also the distance of the
    drone from the nearest alpha shape.
    :param location: current location of the drone
    :param stored_map: stored offline geofence database
    :return: returns False if a violation hasnt been made. If a violation has been made it recommends a new position for the drone.
    """

    print("Current location is ", location)
    max_value =[]
    max_name = []
    violation = False
    for key,value in stored_map:
        if location.within(value) or value.boundary.distance(location)<6000:
            print()
            print("Geofence violation by entering" , key['name'],", ID", key['osm_id'])
            print("Distance to exterior fence of geofenced area", key['name'], " is further ",
                  value.boundary.distance(location))
            violation = True
            return value.boundary.distance(location)
            break

        else:
            max_value.append(value.boundary.distance(location))
            max_name.append(key)
    if violation is False:

        max_results = zip(max_name, max_value)
        max = list(max_results)
        max.sort(key=lambda x:x[1])
        i = 0
        print("Nearby Geofence locations")
        for name,value in max:
            if i < 5:
                print(name['name'],value)
            i = i +1
        return violation

def geofence_check():
    """
    The main function used to check if a geofence violation has been made
    :return: none
    """
    #assigning geofence to false for testing purposes
    geo = False
    count = 0
    while True:
        # starting time
        start = time.time()
        #asssigns random location for testing purposes
        latitude = random.uniform(492840.0,499630.660384617280215)
        longitude = random.uniform(170585.0,190585.19162220077123)
        location = Point(latitude, longitude)

        #checking if geofence is enabled
        geofence_enable = geofencing_enabled(geo)

        # Global Varialbles
        alpha_shapes = []
        property_name = []
        stored_map = []

        def geofencing_enabled(geo):
            """
            The primary use of the function is to enable geofencing on the vehicle
            :param geo: status of geofence on the vehicle
            :return: The function returns a boolean value representing if geofencing is enabled on the vehicle
            """

            if geo == False:
                print("Geofence is now being enabled")
                geo = True
                return geo
            else:
                print("Geofence is enabled")
                return geo

        def geofence_repository():
            """
            The function imports a geofence database and forms a alpha shape for each property. It stores the alpha shapes
            into a list.
            :return: The list with stored alpha shapes
            """

            # read file
            with open('sample.json', 'r') as myfile:
                map = json.load(myfile)

            # localvariables
            features = map["features"]

            # listing the properties , notes : properties data type is dictionary
            for i in range(len(features)):
                properties = map["features"][i]["properties"]
                # forming polygon for each of the features / building
                coordinates = map["features"][i]["geometry"]["coordinates"][0]
                for j in coordinates:
                    property_name.append(properties)
                    # the accuracy of the alpha shape can be adjusted, but imapcts the execution time
                    # alpha_shape = Polygon(j)
                    alpha_shape = alphashape.alphashape(j, 0.)
                    alpha_shapes.append(alpha_shape)
            # storing the results of the algorithm
            results = zip(property_name, alpha_shapes)
            zipped_list = list(results)
            return zipped_list

        def geofence_violation(location, stored_map):
            """
            The function checks if a geofence violation has been made. It check if the point of interest is within the alpha shape and also the distance of the
            drone from the nearest alpha shape.
            :param location: current location of the drone
            :param stored_map: stored offline geofence database
            :return: returns False if a violation hasnt been made. If a violation has been made it recommends a new position for the drone.
            """

            print("Current location is ", location)
            max_value = []
            max_name = []
            violation = False
            for key, value in stored_map:
                if location.within(value) or value.boundary.distance(location) < 6000:
                    print()
                    print("Geofence violation by entering", key['name'], ", ID", key['osm_id'])
                    print("Distance to exterior fence of geofenced area", key['name'], " is further ",
                          value.boundary.distance(location))
                    violation = True
                    return value.boundary.distance(location)
                    break

                else:
                    max_value.append(value.boundary.distance(location))
                    max_name.append(key)
            if violation is False:

                max_results = zip(max_name, max_value)
                max = list(max_results)
                max.sort(key=lambda x: x[1])
                i = 0
                print("Nearby Geofence locations")
                for name, value in max:
                    if i < 5:
                        print(name['name'], value)
                    i = i + 1
                return violation

        def geofence_check():
            """
            The main function used to check if a geofence violation has been made
            :return: none
            """
            # assigning geofence to false for testing purposes
            geo = False
            count = 0
            while True:
                # starting time
                start = time.time()
                # asssigns random location for testing purposes
                latitude = random.uniform(492840.0, 499630.660384617280215)
                longitude = random.uniform(170585.0, 190585.19162220077123)
                location = Point(latitude, longitude)

                # checking if geofence is enabled
                geofence_enable = geofencing_enabled(geo)

                if geofence_enable is True:
                    geo = True
                    # checking if the function is being executed for the first time
                    if count == 0:
                        # it forms alpha shapes of all the location on the map only once for effeciency
                        stored_map = geofence_repository()
                        count = count + 1

                    # detects a geofence violation
                    violation = geofence_violation(location, stored_map)

                    if violation is not False:
                        print()
                        # modifies the path if the geofence violation is detected
                        print("Drone path modified due to geofence violation")
                        latitude = latitude - (violation * 4.2)
                        longitude = longitude - (violation * 4.2)
                        new_location = Point(latitude, longitude)

                        # check if location has been updated
                        if new_location == location:
                            break
                        else:
                            location = new_location
                    end = time.time()
                    print(f"Runtime of the program is {end - start} seconds")
                    while True:
                        try:
                            # confirms if user wants to keep flying
                            mission = int(input("Continue mission (1 to continue, 0 to Exit)"))
                            break
                        except:
                            print("Please try again")
                    if mission == 1:
                        continue
                    else:
                        break
                else:
                    break
            print()
            print("Hope you enjoyed flying the drone")

        # calling the same function
        geofence_check()

        if  geofence_enable is True:
            geo = True
            #checking if the function is being executed for the first time
            if count== 0 :
                #it forms alpha shapes of all the location on the map only once for effeciency
                stored_map = geofence_repository()
                count = count + 1

            #detects a geofence violation
            violation = geofence_violation(location,stored_map)

            if violation is not False:
                print()
                #modifies the path if the geofence violation is detected
                print("Drone path modified due to geofence violation")
                latitude = latitude-(violation*4.2)
                longitude = longitude-(violation*4.2)
                new_location = Point(latitude,longitude)

                #check if location has been updated
                if new_location == location:
                    break
                else:
                    location = new_location
            end = time.time()
            print("Runtime of the program is {end - start} seconds")
            while True :
                try:
                    #confirms if user wants to keep flying
                    mission = int(input("Continue mission (1 to continue, 0 to Exit)"))
                    break
                except:
                    print("Please try again")
            if mission == 1:
                continue
            else:
                break
        else:
            break
    print()
    print("Hope you enjoyed flying the drone")


#calling the same function
geofence_check()

