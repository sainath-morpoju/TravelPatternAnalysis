import csv
import numpy as np
import pandas as pd
import os
from test.kmeansCluster import kmeansCluster as km
class Map(object):
    def __init__(self):
        self._points = []

    def add_all(self,data):
        self._points = data

    def add_point(self, coordinates):
        self._points.append(coordinates)

    def __str__(self):
        if len(self._points) > 0:
            mean = np.mean(self._points,axis=0)
            centerLat = mean[0]
            centerLon = mean[1]

            #centerLat = sum(( x[0] for x in self._points )) / len(self._points)
            #centerLon = sum(( x[1] for x in self._points )) / len(self._points)
            # centerLon = 0.0
            # centerLat = 0.0
            markersCode = "\n".join(
                [ """new google.maps.Marker({{
                    position: new google.maps.LatLng({lat}, {lon}),
                    map: map
                    }});""".format(lat=x[0], lon=x[1]) for x in self._points
                ])
        else:
            centerLon = 0.0
            centerLat = 0.0
            markersCode = "\n"
        return """
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&key=AIzaSyArLRvWuf-D_xRBhSk3VtnerwABnvfJjLc"></script>
            <div id="map-canvas" style="height: 100%; width: 100%"></div>
            <script type="text/javascript">
                var map;
                function show_map() {{
                    map = new google.maps.Map(document.getElementById("map-canvas"), {{
                        zoom: 6,
                        center: new google.maps.LatLng({centerLat}, {centerLon})
                    }});
                    {markersCode}
                }}
                google.maps.event.addDomListener(window, 'load', show_map);
            </script>
        """.format(centerLat=centerLat, centerLon=centerLon,
                   markersCode=markersCode)


def create_gps_map(data=None,day=None):
    # Create a google map instance
    map = Map()
    if data is not None:
        map.add_all(data.tolist())
        #for point in data:
            #map.add_point(point)
    if day is not None:
        if not os.path.isdir('C:/Users/saina/Documents/sample/test/data/participantId2/'):
            os.mkdir('C:/Users/saina/Documents/sample/test/data/participantId2/')
        with open("C:/Users/saina/Documents/sample/test/data/participantId2/testout_{day}.html".format(day=day), "w+") as out:
            print(map, file=out)
    else:
        if not os.path.isdir('C:/Users/saina/Documents/sample/test/data/participantId2/'):
            os.mkdir('C:/Users/saina/Documents/sample/test/data/participantId2/')
        with open("C:/Users/saina/Documents/sample/test/data/participantId2/testout.html", "w+") as out:
            print(map, file=out)


if __name__ == "__main__":

    # file = np.genfromtxt("C:/Users/saina/Documents/sample/test/data/sample_data.csv",delimiter=',')

    #with open("C:/Users/saina/Documents/sample/test/data/sample_data.csv", newline='') as file:
    #buffer = csv.reader(file, delimiter=',', quotechar='|', quoting = csv.QUOTE_NONNUMERIC)

    #create_gps_map(file)

    dataframe = pd.read_excel("C:/Users/saina/Documents/sample/test/data/sensorDataSelf.xlsx", header=0).filter(items=['locLat', 'locLon', 'collectedTimeStamp'])
   # print(dataframe)

    days = dataframe["collectedTimeStamp"].map(lambda t: t.date()).unique()
    print(days)
    for day in days:
        #self.distanceMap[day] = []
        filtered_df = dataframe.loc[dataframe["collectedTimeStamp"].map(lambda t: t.date()) == day]
        filtered_df = filtered_df[filtered_df['locLat'] != "None"]
        data = filtered_df[['locLat', 'locLon']].values

        print(data)
        create_gps_map(data,day)

    create_gps_map(dataframe[['locLat','locLon']].values)
