import time
import random
import resource

from geolocation import GeoLocation
from gpspoint import GPSPoint

def generate_test_points():
    gps_tuples = []

    gps_tuples.append(["Miriam Haheshmonait 14 Tel Aviv"])
    gps_tuples.append(["San Francisco"])
    gps_tuples.append(["Rabin Square Tel Aviv"])
    gps_tuples.append(["New York"])
    gps_tuples.append(["Caracas"])
    gps_tuples.append(["Argentina"])
    gps_tuples.append(["Cuzco Peru"])
    gps_tuples.append(["Shangai China"])
    gps_tuples.append(["Seoul Korea"])
    gps_tuples.append(["Afghanistan"])
    gps_tuples.append(["Kfar Yona Israel"])
    gps_tuples.append(["Netanya Israel"])
    gps_tuples.append(["Gaash Israel"])
    gps_tuples.append(["Eilat Israel"])
    gps_tuples.append(["Strasbourg France"])
    gps_tuples.append(["Montpellier France"])
    gps_tuples.append(["Berlin Germany"])
    gps_tuples.append(["Stuttgart Germany"])
    
    return gps_tuples

def generate_random_points():
    gps_tuples = []
    start_time = time.time()
    number_of_points = 100000
    for i in xrange(1,number_of_points):
        gps_tuples.append(["Test", random.uniform(-90, 90), random.uniform(-180, 180)])
    end_time = time.time()
    print "Time for generating " + str(number_of_points) +" points: " + str(end_time - start_time)
    return gps_tuples
    
def printKnn(kNN):
    for result in kNN:
        print str(result[0]) + ", distance: " + str(result[1])
    print ""
    
if __name__ == "__main__":
    #gps_tuples = generate_test_points()
    gps_tuples = generate_random_points()
    geolocation = GeoLocation()
    
    start_time = time.time()
    geolocation.load_points(gps_tuples)
    end_time = time.time()
    print "Time for creating the kd-Tree: " + str(end_time - start_time)
    #geolocation.load_points(gps_tuples)
    test_point = GPSPoint("Maze 9 Tel Aviv", 12.3234, -12.234)
    
    
    #test_point = Point("Bastille paris", 48.862592, 2.347260)
    #lat = raw_input("Test point - Latitude: ")
    #lon = raw_input("Test point - Longitude: ")
    
    for k in xrange(1,2):
        #print testPoint.distance(ny);
        #k = int(raw_input("How many nearest neighbors? (K): "))
        start_time = time.time()
        result = geolocation.kNN(test_point, k)
        end_time = time.time()
        print "Time for kNN algorithm: " + str(end_time - start_time) + " with k=" + str(k)
        printKnn(result)
        
    print("Memory usage: " + str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576) + "MB")