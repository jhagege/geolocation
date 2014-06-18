from math import radians, cos, sin

from geopy import geocoders

import distance

class GPSPoint:    
    g = geocoders.GoogleV3()
    '''
    If there is latitude and longitude, we won't have to ask geocode for it.
    '''
    def __init__(self, addressString=None, lat=None, lon=None):
        if lat != None and lon != None:
            self.address = addressString
            self.deg_lat = lat
            self.deg_lon = lon
        else:
            self.address, (self.deg_lat, self.deg_lon) = self.g.geocode(addressString);
        
        self.convert_to_cartesian()
        self.data = [self.x, self.y, self.z]
        #self.data = (self.deg_lat, self.deg_lon)
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __len__(self):
        return len(self.data)
        
    def distance(self, otherPoint):
        # Haversine does the conversion to radians.
        return distance.haversine([self.deg_lat, self.deg_lon], [otherPoint.deg_lat, otherPoint.deg_lon])
    
    def __str__(self):
        #return str(self.address[0:8]) + " " + str(self.x) + " " + str(self.y) + " " + str(self.z)
        return str(self.address) + " " + str(self.deg_lat)[0:5] + " " + str(self.deg_lon)[0:5]
    
    def to_point(self):
        return [self.x, self.y, self.z]
    
    def convert_to_cartesian(self):
        R = 6371
        self.rad_lat = radians(self.deg_lat)
        self.rad_lon = radians(self.deg_lon)
        self.x = R * cos(self.rad_lat) * cos(self.rad_lon)
        self.y = R * cos(self.rad_lat) * sin(self.rad_lon)
        self.z = R * sin(self.rad_lat)
        
    def __repr__(self):
        return self.address