# # =============================================
# # IMPORT OF THE DATA
# # =============================================
# import requests
# import urllib.parse

# endpointUrl = "https://query.wikidata.org/sparql?query=";
# query = """
# SELECT ?item ?itemLabel ?elev ?coord
# WHERE
# {
#   ?item wdt:P31/wdt:P279* wd:Q486972;
#   wdt:P17 wd:Q183;
#   rdfs:label ?itemLabel;
#   wdt:P2044 ?elev;
#   wdt:P625 ?coord;
#   FILTER (lang(?itemLabel) = "de") .
#   FILTER regex (?itemLabel, "(ow|itz)$").
# }
# """
# encoded_query = urllib.parse.quote(query)
# url = f"{endpointUrl}{encoded_query}&format=json"

# r=requests.get(url)
# data = r.json()
#print(data)
# #=============================================



#=============================================
#CLEANUP AND CODE PREPERATION
#=============================================

from pyqgis_scripting_ext.core import *

countriesName = "ne_50m_admin_0_countries"
citiesName = "owitz"
HMap.remove_layers_by_name(["OpenStreetMap", citiesName, countriesName])

folder = "C:/github/examocking/"


# load open street map
osm = HMap.get_osm_layer()
HMap.add_layer(osm)
#=============================================


# #=============================================
# #CREATION OF THE GEOPACKAGE
# #=============================================
# fields = {
#     "name": "String",
#     "elevation": "Integer",
#     "lat": "Float",
#     "lon": "Float"
# }

# villageLayer = HVectorLayer.new(citiesName, "Point", "EPSG:4326", fields)

# for result in data['results']['bindings']:

#     city_name = result['itemLabel']['value']
#     elevation = result['elev']['value']
#     coordinates = result['coord']['value']
#     coord_parts = coordinates.split('(')[1].split(')')[0].split()
    
#     lat = float(coord_parts[1])
#     lon = float(coord_parts[0])
    
#     villageLayer.add_feature(HPoint(lon, lat), [city_name, elevation, lat, lon])
    

# path = folder + "villages.gpkg"
# HopeNotError = villageLayer.dump_to_gpkg(path, overwrite = True)
# if HopeNotError:
#     print(HopeNotError)
# #=============================================


#=============================================
#LOADING THE BOUNDARIES OF GERMANY
#=============================================

geopackagePath = folder + "natural_earth_vector.gpkg"


germanyLayer = HVectorLayer.open(geopackagePath, countriesName)
germanyLayer.subset_filter("ADMIN = 'Germany'")
HMap.add_layer(germanyLayer)
#=============================================


#=============================================
#LOADING TOF THE OWITZ LAYER
#=============================================
owitzLayer = HVectorLayer.open(folder + "villages.gpkg", citiesName)
HMap.add_layer(owitzLayer)
#=============================================