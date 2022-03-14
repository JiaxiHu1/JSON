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

#map 1 
from cgitb import text
import json
import plotly 
import csv
from plotly import offline
from plotly.graph_objs import Scattergeo, Layout



infile = open('univ.json', 'r')
list_of_schools = json.load(infile) 

readfile = open('ValueLabels.csv','r')
csv_readfile = csv.reader(readfile,delimiter = ',')

divisions = ["Atlantic Coast Conference", "Big Twelve Conference", "Big Ten Conference", "Pacific-12 Conference", "Southeastern Conference"]
d_dict = {}

for line in csv_readfile:
    if line[2] in divisions:
        d_dict[line[2]] = line[1]



grad_women,enroll, schoolname, lons,lats,text = [],[], [], [],[],[]



for i in list_of_schools:
    if str(i["NCAA"]["NAIA conference number football (IC2020)"]) in d_dict.values() and i["Graduation rate  women (DRVGR2020)"] > 50: 
       
        grad_rate_women = i["Graduation rate  women (DRVGR2020)"]
        grad_women.append(grad_rate_women)

        enroll = i["Total  enrollment (DRVEF2020)"]
        #enroll.append(enroll)

        school=i["instnm"]
        schoolname.append(school)
        
        lon = i["Longitude location of institution (HD2020)"]
        lons.append(lon)

        lat = i["Latitude location of institution (HD2020)"]
        lats.append(lat)

        text.append(schoolname+','+str(grad_women)+'%')

#top 10 
print(grad_women[:10])
print(schoolname[:10])
print(lons[:10])
print(lats[:10])



data = [Scattergeo(lon=lons,lat=lats)]

data = [
    {'type':'scattergeo',
    'lon':lons,
    'lat':lats,
    'text':text,
    'grad_rate_for_women':grad_women,
    'institution':schoolname,
    'marker':{
        'size':[2*a for a in enroll], 
        'color':enroll,
        'colorscale':'Viridis',
        'reversescale':True,
        'colorbar':{'title':'Total Enrollment'}
    },
    }]


my_layout = Layout(title='Universities - Graduation Rate for Women over 50%')
fig = {'data':data, 'layout':my_layout}
offline.plot(fig,filename='graduation_rate_for_women.html')

