import pickle
from math import radians, cos, sin, asin, sqrt
import textdistance
from shapely.geometry import Point
import geopandas
import os
import time

FILENAME = "suburbs.dat"
FILENAME2 = "suburbgeo.dat"


class subfinder:
    def __init__(self):
        path = self.rel_path(FILENAME)
        f = open(path, 'rb')
        lst = pickle.load(f)
        self.sub_info = lst[0]
        self.sub_same = lst[1]
        f.close()
        path = self.rel_path(FILENAME2)
        f = open(path, 'rb')
        lst = pickle.load(f)
        self.geo_name = lst[0]
        self.geo_obj = lst[1]
        self.ids = lst[2]

    def rel_path(self, filename):
        return os.path.join(os.getcwd(), os.path.dirname(__file__), filename)

    def get_key(self, value):
        return [k for k, v in self.sub_info.items() if v == value]

    def CalSimilarity(self, suburb, lng, lat):
        pending_lst = []
        for key in self.sub_same:
            sim = textdistance.jaro_winkler.similarity(key, suburb)
            if sim > 0.7:
                pending_lst.append(key)
        nearest = float('inf')
        nearest_city = None
        for area in pending_lst:
            dlon = self.sub_info[area]["lng"] - lng
            dlat = self.sub_info[area]["lat"] - lat
            dis = ((dlon**2) + (dlat**2))**0.5
            if dis < nearest:
                nearest = dis
                nearest_city = area
        return nearest_city

    def GetPlace(self, lat, lng):
        coordinates = Point(lng, lat)
        st = time.time()
        decide = self.geo_obj.intersects(coordinates)
        index = decide[decide].index.values[0]
        suburb = self.geo_name[str(self.ids[index])].title()
        print("Get Suburb time: ", time.time() - st)
        state = "Victoria"
        if suburb in self.sub_same:
            if len(self.sub_same[suburb]) == 1:
                result = dict()
                result["suburb"] = suburb
                result["state"] = state
                result["city"] = self.sub_info[suburb]["statistic_area"]
                return result
            else:
                st = time.time()
                nearest = float('inf')
                nearest_city = None
                for name in self.sub_same[suburb]:
                    dlon = self.sub_info[name]["lng"] - lng
                    dlat = self.sub_info[name]["lat"] - lat
                    dis = ((dlon**2) + (dlat**2))**0.5
                    if dis < nearest:
                        nearest = dis
                        nearest_city = name
                print("nearest city time: ", time.time() - st)
                result = dict()
                result["suburb"] = suburb
                result["state"] = state
                result["city"] = self.sub_info[nearest_city]["statistic_area"]
                return result
        else:
            st = time.time()
            best_match = self.CalSimilarity(suburb, lng, lat)
            print("best match time: ", time.time() - st)
            if best_match:
                result = dict()
                result["suburb"] = best_match
                result["state"] = state
                result["city"] = self.sub_info[best_match]["statistic_area"]
                return result
            else:
                return None
