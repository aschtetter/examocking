
#=============================================
#CLEANUP AND CODE PREPERATION
#=============================================

from pyqgis_scripting_ext.core import *

countriesName = "ne_50m_admin_0_countries"
citiesName = "owitz"
HMap.remove_layers_by_name(["OpenStreetMap", citiesName, countriesName])

#folder = "C:/github/examocking/" #Anna
folder = "C:/Users/Lorenz/Documents/GitHub/exam/examocking/" #Lorenz
outputFolder = f"{folder}/output/"

#CRS helper
crsHelper = HCrs()
crsHelper.from_srid(4326)
crsHelper.to_srid(32632)

# load open street map
osm = HMap.get_osm_layer()
HMap.add_layer(osm)
#=============================================



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
# #print(data)
# #=============================================



# #=============================================
# #CREATION OF THE GEOPACKAGE
# #=============================================
# fields = {
#     "name": "String",
#     "elevation": "Integer",
#     "lat": "Float",
#     "lon": "Float"
# }

# villageLayer = HVectorLayer.new(citiesName, "Point", "EPSG:32632", fields)

# for result in data['results']['bindings']:

#     city_name = result['itemLabel']['value']
#     elevation = result['elev']['value']
#     coordinates = result['coord']['value']
#     coord_parts = coordinates.split('(')[1].split(')')[0].split() # Point(42.21 25.64)
    
#     lat = float(coord_parts[1])
#     lon = float(coord_parts[0])
    
#     point = HPoint(lon, lat)
#     point = crsHelper.transform(point)
    
#     villageLayer.add_feature(point, [city_name, elevation, lat, lon])


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


#GerGeo definition needed later for bbox in the map layout
germany = germanyLayer.features()
GerGeo = germany[0].geometry
GerGeo = crsHelper.transform(GerGeo)
GerGeo = GerGeo.buffer(10000) #map units = 1 m -> Buffer = 10 km

#=============================================


#=============================================
#LOADING OF THE OWITZ LAYER
#=============================================
owitzLayer = HVectorLayer.open(folder + "villages.gpkg", citiesName)
HMap.add_layer(owitzLayer)
#=============================================

#=============================================
#STYLING
#=============================================
ranges = [
    [0, 50],
    [51, 100],
    [101, 500],
    [501, 1000],
    [1001, 2000],
    [2001, 3000],
    [3001, float('inf')]
]



styles = [
    HFill('#edf8fb') + HMarker("round", 2) + HStroke("black", 0.3),
    HFill('#bfd3e6') + HMarker("round", 2) + HStroke("black", 0.3),
    HFill('#9ebcda') + HMarker("round", 2) + HStroke("black", 0.3),
    HFill('#8c96c6') + HMarker("round", 2) + HStroke("black", 0.3),
    HFill('#8c6bb1') + HMarker("round", 2) + HStroke("black", 0.3),
    HFill('#88419d') + HMarker("round", 2) + HStroke("black", 0.3),
    HFill('#6e016b') + HMarker("round", 2) + HStroke("black", 0.3),
]

CitylabelProperties = {
    "font": "Arial",
    "color": "black",
    "size": 6,
    "field": "concat(name ,': ',elevation, ' m')",
    "xoffset": 0,
    "yoffset": -10
}

labelStyle = HLabel(**CitylabelProperties) +HHalo("white",1)
owitzLayer.set_graduated_style("elevation", ranges, styles, labelStyle)


germanyLayer.set_style(HStroke("black", 1) + HFill("0,0,0,35"))
#=============================================



#=============================================
#CREATING THE LAYOUT
#=============================================

printer = HPrinter(iface)
mapProperties = {
    "x": 5,
    "y": 25,
    "width": 285,
    "height": 180,
    "frame": True,
    "extent": GerGeo.bbox() # germayLayer seems not to work after the transformation
}
printer.add_map(**mapProperties)

legendProperties = {
        "x": 10,
        "y": 120,
        "width": 75,
        "height": 45,
        "frame": True
    }
printer.add_legend(**legendProperties)
    
labelProperties = {
        "x": 75,
        "y": 10,
        "text": "Distribution of German Cities ending in '-ow/-itz'",
        "font_size": 20,
        "bold": True
    }
printer.add_label(**labelProperties)

labelPropertiesSubtitle = {
    "x": 130,
    "y": 18,
    "text": "Based on elevation",
    "font_size": 14,
    "italic": True
}
printer.add_label(**labelPropertiesSubtitle)

scalebarProperties = {
    "x": 220,
    "y": 185,
    "units": "km",
    "style": "Single Box", # or 'Line Ticks Up'
    "font_size": 14
}
printer.add_scalebar(**scalebarProperties)

printer.dump_to_pdf(outputFolder+"OWITZ.pdf")
#=============================================