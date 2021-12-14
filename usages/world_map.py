import pandas as pd
from graph import *
from consts import *
from ColoringAlgos import ColoringAlgos

# visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.subplots as ps
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.io as pio
from operator import truediv
import json

def load_us():
    vertices = VerticesList()
    edges = EdgesSet()
    dfBorders = pd.read_csv("us-state-borders.csv")
    for idx, row in dfBorders.iterrows():
        st1, st2 = row["ST1ST2"].split("-")
        if st1 not in vertices:
            vertices.add(Vertex(st1))
        if st2 not in vertices:
            vertices.add(Vertex(st2))

        edges.add((vertices[st1], vertices[st2]))

    graph = Graph(vertices,edges)
    
    dfBound = pd.read_csv("us-state-boundaries.csv", delimiter=";")
    geo = None
    with open("us-geo.json", "r") as f:
        geo = json.load(f)

    dfColor = pd.DataFrame(columns=["stusab", "color"])

    ColoringAlgos.sat(graph)
    for vertex in graph.vertices:
        dfColor = dfColor.append(pd.Series([vertex.id, vertex.color], index = dfColor.columns), ignore_index=True)

    dfBound = dfBound.merge(dfColor, how="inner", left_on="stusab", right_on="stusab")
    
    return dfBound, geo

def load_fr():
    vertices = VerticesList()
    edges = EdgesSet()
    with open("departements_fr_boundaries.txt", "r") as f:
        for line in f.readlines():
            row = line.strip().split(",")
            dept = row[0]
            if dept not in vertices:
                vertices.add(Vertex(dept))


            for vois in row[1:]:
                if vois not in vertices:
                    vertices.add(Vertex(vois))
                edges.add((vertices[dept], vertices[vois]))

    graph = Graph(vertices,edges)
    print(graph)
    
    geo = None
    with open("fr-geo.json", "r") as f:
        geo = json.load(f)

    dfColor = pd.DataFrame(columns=["stusab", "color"])

    ColoringAlgos.sat(graph)
    for vertex in graph.vertices:
        dfColor = dfColor.append(pd.Series([vertex.name, vertex.color], index = dfColor.columns), ignore_index=True)

    return dfColor, geo

"""
fig = px.choropleth_mapbox(dfBound, geojson=geo, color="color",
                        locations="name", featureidkey="properties.name",
                        center={"lat": 42.5517, "lon": -97.7073},
                        mapbox_style="carto-positron", zoom=2.5, color_discrete_sequence=COLORS_ORDER)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.write_image("fig1.png")
"""
    