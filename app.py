import streamlit as st
import geopandas as gpd
import pandas as pd
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Visualisation MRC avec carte", layout="wide")

@st.cache_data
def load_mrc_geojson():
    return gpd.read_file("mrc.geojson")

@st.cache_data
def load_data():
    return pd.read_csv("data_mrc.csv")

mrc_map = load_mrc_geojson()
df = load_data()

st.title("Visualisation interactive des données par MRC")

m = folium.Map(location=[47.5, -71.5], zoom_start=6, tiles="cartodbpositron")

def style_function(feature):
    return {
        'fillColor': '#6baed6',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.5,
    }

def highlight_function(feature):
    return {
        'fillColor': '#2171b5',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.7,
    }

geojson = folium.GeoJson(
    mrc_map,
    name="MRC",
    style_function=style_function,
    highlight_function=highlight_function,
    tooltip=folium.GeoJsonTooltip(fields=["NOM_MRC"], labels=True),
)

geojson.add_to(m)

map_data = st_folium(m, width=700, height=500)

selected_mrc = st.selectbox("Ou sélectionnez une MRC ici :", sorted(df["NOM_MRC"].unique()))

clicked_mrc = None
if map_data and "last_active_drawing" in map_data and map_data["last_active_drawing"]:
    clicked_mrc = map_data["last_active_drawing"]["properties"].get("NOM_MRC", None)

mrc_to_show = clicked_mrc if clicked_mrc else selected_mrc

st.markdown(f"### Données pour la MRC : **{mrc_to_show}**")

data_filtered = df[df["NOM_MRC"] == mrc_to_show]
st.dataframe(data_filtered)