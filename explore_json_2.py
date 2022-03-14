import json 

#changed to 30 day file 
infile = open('eq_data_30_day_m1.json','r')
outfile = open('readable_eq_data.json','w')

eq_data = json.load(infile)
json.dump(eq_data, outfile, indent = 4)

#call the key of the dictionary - and the return will be the value inside 
list_of_eqs = eq_data["features"]

mags,lons,lats, hover_texts = [],[],[],[]

#list of eqs is the whole things 
#and eq in list of eqs is the features 
for eq in list_of_eqs:
    mag = eq['properties']['mag']
    lon = eq['geometry']['coordinates'][0]
    lat = eq['geometry']['coordinates'][1]
    title = eq['properties']['title']
    mags.append(mag)
    lons.append(lon)
    lats.append(lat)
    hover_texts.append(title)

#top 10 of mags 
print(mags[:10])
print(lons[:10])
print(lats[:10])

from plotly.graph_objs import Scattergeo, Layout 
from plotly import offline 

data = [
    {'type':'scattergeo',
    'lon':lons,
    'lat':lats,
    'text':hover_texts,
    'marker':{
        #[expression iteration condition]
        'size':[5*mag for mag in mags],#to make the size of the dots 5 times bigger 
        'color':mags,
        'colorscale':'Viridis',
        'reversescale':True,
        'colorbar':{'title':'Magnitude'}
    },
    }]
    #Scattergeo(lon=lons, lat=lats)]

my_layout = Layout(title='Global Earthquakes')

#to produce the figure 
fig = {'data':data, 'layout':my_layout}

offline.plot(fig,filename = 'global_earthquakes.html')

