import folium
import pandas as pd

listings = pd.read_csv('listings_dec18.csv', header=0)

lat = listings['latitude']
lon = listings['longitude']

locations = list(zip(lat, lon))

map_base = folium.Map(location=[-33.8688, 151.2093],tiles='OpenStreetMap',zoom_start=8)
for index, row in listings.iterrows():
    if row['H_mark'] == 'H1':
        marker_color = 'darkred'
        fill_color = 'darkred'
    else:
        marker_color = 'orange'
        fill_color = 'lightggrey'

    folium.Circle(location=[row['latitude'], row['longitude']], color = marker_color, fill = True, fill_color = fill_color).add_to(map_base)
map_base