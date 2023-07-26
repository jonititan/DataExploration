import geopandas
import folium

df = geopandas.read_file("EWR Alignment Ox2CamSouth ln.shp")
print(df)
df.set_crs(epsg=1936, inplace=True)
df = df.explode(index_parts=True)
print(df)

m = folium.Map(control_scale=True)
feature_dict={a:folium.FeatureGroup(name=a) for a in list(df['name'].unique())}
for r in df.iterrows():
	location_tmp = list([(lat, lon) for lon, lat, alt in r[1]['geometry'].coords])
	folium.features.PolyLine(locations=location_tmp).add_to(feature_dict[r[1]['name']])
for fgs in feature_dict.values():
         fgs.add_to(m)
#folium.GeoJson(df.to_json(to_wgs84=True)).add_to(m)
folium.LayerControl().add_to(m)
m.fit_bounds(m.get_bounds())
m.save('index.html')

import code
code.interact(local=locals())