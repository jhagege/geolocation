#import kdtree We don't use the kdtree anymore.

# Std library imports
import distance

# Third party imports
import numpy as np
from scipy import spatial

# Local application imports
from gpspoint import GPSPoint

class GeoLocation:
    '''
    self.gps_points will hold all the GPSPoint objects.
    self.tree will hold the KD-Tree
    '''
    def __init__(self):
        # An array that holds GPSPoint objects.
        self.gps_points = []
        # A cKDTree object.
        self.tree = None
    
    # Receives the list of tuples: [['Miriam Haheshmonait 8', lat, lon], ...]
    def load_points(self, gps_tuples):
        # If there are existing points, we need to be careful about concurrency.
        # So first: create a temporary array with the new points.
        if (len(self.gps_points) != 0):
            temp_array = []
            for point_tuple in gps_tuples:
                self.add_gps_point(*point_tuple, destination_array=temp_array)
            # Once it's done, update the pointer of the gps_points to the temp array.
            
            temp_tree = None
            self.tree = self.create_kd_tree(temp_tree)
            
            # Update the new pointers once the tree is constructed.
            #self.tree = temp_tree

            self.gps_points = temp_array
            
        # This is the first time we load points, no need to take care of the temp array and tree.
        else:
            for point_tuple in gps_tuples:
                self.add_gps_point(*point_tuple, destination_array=self.gps_points)
            # We have to reassign because of the way python passes objects.
            # When passing self.tree, we pass None, which is immutable.
            self.tree = self.create_kd_tree(self.tree)
        
    def number_of_points(self):
        return len(self.gps_points)
        
    def add_gps_point(self, address, lat=None, lon=None, destination_array=None):
        point = GPSPoint(address, lat, lon)
        destination_array.append(point)
    
    def create_kd_tree(self, destination_tree):
        # Creates a KDTree using the Scipy cKDTree class.
        # It takes as argument an array of points: [[1,2,3], [-12, 234, 123], ...]
        destination_tree = spatial.cKDTree([point.data for point in self.gps_points])
        #self.tree = kdtree.create(self.points_array)
        return destination_tree
    
    # K Nearest neighbors to point.
    # Return [(gps_point, distance from point), ...]
    def kNN(self, point, k):
        # Error checking: if k > n, do k=n
        number_of_points = self.number_of_points()
        if k > number_of_points:
            k = number_of_points
        
        # The distance function is cartesian distance (we converted the points with this).
        # The query function is KNN - returns [distances, neighbors_index]
        distances, neighbors_index = self.tree.query(point.data, k=k)
        
        # neighbors_index = [1242, 434, 244555, 23213, 1234123]
        kNN = []
        
        for neighbor_index in np.nditer(neighbors_index):
            distance = self.gps_points[neighbor_index].distance(point)
            kNN.append([self.gps_points[neighbor_index], distance])
        return kNN
            
    def print_points(self):
        for point in self.gps_points:
            print point