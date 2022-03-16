"""
Process the JSON file named univ.json. Create 3 maps per instructions below.
The size of the point on the map should be based on the size of total enrollment. Display only those schools 
that are part of the ACC, Big 12, Big Ten, Pac-12 and SEC divisons (refer to valueLabels.csv file)

The school name and the specific map criteria should be displayed when you hover over it.

(For example for Map 1, when you hover over Baylor, it should display "Baylor University, 81%")
Choose appropriate tiles for each map.


Map 1) Graduation rate for Women is over 50%
Map 2) Percent of total enrollment that are Black or African American over 10%
Map 3) Total price for in-state students living off campus over $50,000

"""


import json
import csv
from plotly import offline
from plotly.graph_objs import Scattergeo, Layout



infile = open('univ.json', 'r')
list_of_schools = json.load(infile) 

readfile = open('ValueLabels.csv','r')
csv_readfile = csv.reader(readfile,delimiter = ',')
next(csv_readfile)

division_names = ["Atlantic Coast Conference", "Big Twelve Conference", "Big Ten Conference", "Pacific-12 Conference", "Southeastern Conference"]
d_dict = {}

for x in csv_readfile:
    if x[2] in division_names:
        d_dict[x[2]] = x[1]


prices,enroll, lons,lats,text = [],[], [], [],[]


for i in list_of_schools:
    if str(i["NCAA"]["NAIA conference number football (IC2020)"]) in d_dict.values():
        try:
            if i["Total price for in-state students living off campus (not with family)  2020-21 (DRVIC2020)"] > 50000: 
       
                price = i["Total price for in-state students living off campus (not with family)  2020-21 (DRVIC2020)"]
                prices.append(price)

                e = i["Total  enrollment (DRVEF2020)"]
                enroll.append(e)

                school=i["instnm"]
        
                lon = i["Longitude location of institution (HD2020)"]
                lons.append(lon)

                lat = i["Latitude location of institution (HD2020)"]
                lats.append(lat)

                text.append(school+","+ "$"+str(price))
        except:
            print(school,"has no data about the housing prices")




data = [Scattergeo(lon=lons,lat=lats)]

data = [
    {'type':'scattergeo',
    'lon':lons,
    'lat':lats,
    'text':text,
    'marker':{
        'size':[e/1000 for e in enroll], 
        'color':enroll,
        'colorscale':'Viridis',
        'reversescale':True,
        'colorbar':{'title':'Total Enrollment'}
    },
    }]


my_layout = Layout(title='Map 3) Total price for in-state students living off campus over $50,000')
fig = {'data':data, 'layout':my_layout}
offline.plot(fig,filename='total_price_for_in-state_students.html')

