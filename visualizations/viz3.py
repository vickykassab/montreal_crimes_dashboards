from dash import html, dcc, callback, Input, Output, Patch
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import json
from shapely.geometry import Point
import numpy as np
import os
from data_manager import data_manager

_cached_figure = None
_cached_data = None
_cached_reduced_data = {}  
_cached_geojson_path = None

def crime_hover_template(crime_type):
    return (
        f"<b>{crime_type}</b><br>" +
        "District: %{customdata[1]}<br>" +
        "PDQ: %{customdata[0]}<br>" +
        "Crime Count: %{customdata[2]}<extra></extra>"
    )

def base_hover_template():
    return "District: %{location}<extra></extra>"

def _get_montreal_json_path():
    """Trouve le chemin correct vers le fichier montreal.json"""
    global _cached_geojson_path
    if _cached_geojson_path:
        return _cached_geojson_path
    
    primary_path = "src/data/montreal.json"
    if os.path.exists(primary_path):
        _cached_geojson_path = primary_path
        return primary_path
    
    possible_paths = [
        "data/montreal.json", 
        "../data/montreal.json",
        os.path.join(os.path.dirname(__file__), "data", "montreal.json"),
        os.path.join(os.path.dirname(__file__), "..", "data", "montreal.json")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            _cached_geojson_path = path
            return path
    
    _cached_geojson_path = primary_path
    return _cached_geojson_path

def load_and_process_data():
    """OPTIMIZATION 2: Load data once with minimal processing"""
    global _cached_data
    
    if _cached_data is not None:
        return _cached_data
    
    print("Loading and preprocessing data for optimal performance...")
    
    CRIME_TRANSLATION = {
        "Vol De Véhicule À Moteur": "Motor Vehicle Theft",
        "Méfait": "Mischief", 
        "Vol Dans / Sur Véhicule À Moteur": "Theft From/In Motor Vehicle",
        "Introduction": "Breaking And Entering",
        "Vols Qualifiés": "Robbery",
        "Infractions Entrainant La Mort": "Offences Causing Death"
    }
    
    montreal_json_path = _get_montreal_json_path()
    with open(montreal_json_path) as f:
        montreal_geo = json.load(f)

    gdf_districts = gpd.read_file(montreal_json_path)
    df = data_manager.get_data_for_viz3()
    df = df.rename(columns={
        "CATEGORIE": "CrimeType",
        "LONGITUDE": "Longitude", 
        "LATITUDE": "Latitude",
        "PDQ": "PDQ"
    }).dropna(subset=["Longitude", "Latitude"])
    
    df["CrimeType"] = df["CrimeType"].str.strip().str.lower().str.title()
    df["CrimeType"] = df["CrimeType"].map(CRIME_TRANSLATION).fillna(df["CrimeType"])
    df["PDQ"] = df["PDQ"].astype(str)

    df = df[
        (df["Latitude"].between(45.40, 45.70)) & 
        (df["Longitude"].between(-73.95, -73.45))
    ].copy()
    
    df["geometry"] = gpd.points_from_xy(df["Longitude"], df["Latitude"])
    gdf_crimes = gpd.GeoDataFrame(df, geometry="geometry", crs=gdf_districts.crs)
    gdf_joined = gpd.sjoin(gdf_crimes, gdf_districts, how="left", predicate="within")
    gdf_joined["District"] = gdf_joined["NOM"]
    
    _cached_data = {
        'montreal_geo': montreal_geo,
        'gdf_joined': gdf_joined,
        'districts': gdf_districts
    }
    
    print(f"Data optimized and cached: {len(gdf_joined)} crime records")
    return _cached_data

def precompute_reduced_data(gdf_joined, max_points_per_district):
    """OPTIMIZATION 6: Precompute and cache different reduction levels"""
    global _cached_reduced_data
    
    cache_key = f"reduced_{max_points_per_district}"
    if cache_key in _cached_reduced_data:
        return _cached_reduced_data[cache_key]
    
    print(f"Precomputing reduced dataset for {max_points_per_district} points per district...")
    

    district_groups = gdf_joined.dropna(subset=['District']).groupby('District')
    reduced_data = []
    
    for district, district_data in district_groups:
        crime_counts = district_data['CrimeType'].value_counts()
        top_crimes = crime_counts.head(max_points_per_district)
        
        for crime_type, count in top_crimes.items():
            crime_subset = district_data[district_data['CrimeType'] == crime_type]
            representative_idx = len(crime_subset) // 2
            representative = crime_subset.iloc[representative_idx].copy()
            representative['crime_count'] = count
            reduced_data.append(representative)
    
    result = pd.DataFrame(reduced_data)
    _cached_reduced_data[cache_key] = result
    print(f"Cached reduced dataset: {len(result)} points")
    return result

def create_initial_figure():
    """OPTIMIZATION 8: Create base figure once and reuse structure"""
    print("Creating optimized base figure...")
    
    data = load_and_process_data()
    montreal_geo = data['montreal_geo']
    
    fig = go.Figure()

    neighborhoods = [feature["properties"]["NOM"] for feature in montreal_geo["features"]]
    z_vals = [1] * len(neighborhoods)

    fig.add_choroplethmapbox(
        geojson=montreal_geo, 
        locations=neighborhoods,
        z=z_vals,
        featureidkey="properties.NOM",
        colorscale=[[0, "lightgrey"], [1, "lightgrey"]],
        showscale=False,
        marker_opacity=0.2,
        marker_line=dict(width=1.5, color="black"),
        hovertemplate=base_hover_template(),
        name="Districts"
    )

    
    fig.update_layout(
        mapbox_style="white-bg",
        mapbox_zoom=8.5,
        mapbox_center={"lat": 45.55, "lon": -73.6},
        mapbox_bounds={"west": -74.1, "east": -73.3, "south": 45.35, "north": 45.75},
        height=700,
        margin=dict(t=60, r=10, l=10, b=10),
        legend=dict(
            orientation="v",
            yanchor="top", 
            y=1,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="Black",
            borderwidth=1
        ),
        title=dict(
            text="Montreal Crime Map - Loading...",
            x=0.5,
            font=dict(size=18),
            pad=dict(t=20)
        )
    )
    
    return fig

def update_crime_traces(fig, max_points):
    """OPTIMIZATION 10: Update only crime traces, not entire figure"""
    data = load_and_process_data()
    gdf_joined = data['gdf_joined']
    reduced_gdf = precompute_reduced_data(gdf_joined, max_points)
    
    COLOR_MAP = {
        "Motor Vehicle Theft": "#626ff5",
        "Mischief": "#E74C3C", 
        "Theft From/In Motor Vehicle": "#1ABC9C",
        "Breaking And Entering": "#9B59B6",
        "Robbery": "#F39C12",
        "Offences Causing Death": "#00BCD4"
    }

 
    fig.data = fig.data[:1] 
    
    for crime_type, color in COLOR_MAP.items():
        crime_data = reduced_gdf[reduced_gdf["CrimeType"] == crime_type]
        
        if not crime_data.empty:
            base_size = 8
            sizes = np.minimum(20, base_size + (crime_data['crime_count'].fillna(0) / 10))

            fig.add_trace(go.Scattermapbox(
                lat=crime_data["Latitude"].values,
                lon=crime_data["Longitude"].values,
                mode="markers",
                marker=dict(
                    size=sizes.tolist(),
                    color=color,
                    opacity=0.8
                ),
                name=crime_type,
                customdata=crime_data[["PDQ", "District", "crime_count"]].values,
                hovertemplate=crime_hover_template(crime_type)
            ))

    fig.update_layout(
        title_text=f"Montreal Crime Map - Top {max_points} Crime Types per District"
    )
    
    return fig

def layout():
    """OPTIMIZATION 11: Simplified layout with faster initial load"""
    return html.Div([
        # Header
        html.Div([
            html.H2("Montreal Crime Data Explorer", 
                   style={'textAlign': 'center', 'marginBottom': '10px', 'color': '#2c3e50'}),
            html.P("Interactive map showing top crime types across Montreal districts",
                   style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#7f8c8d'})
        ]),
        
        # Controls
        html.Div([
            html.Div([
                html.Label("Maximum crime types per district:", 
                          style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Slider(
                    id='max-points-slider',
                    min=1, max=5, step=1, value=3,
                    marks={i: str(i) for i in range(1, 6)},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], style={'width': '100%', 'textAlign': 'center'})
        ], style={'margin': '20px 0', 'padding': '15px', 
                 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),
        
        # Map with loading
        html.Div([
            dcc.Loading(
                dcc.Graph(
                    id='crime-map', 
                    figure=create_initial_figure(),
                    style={'height': '700px'}
                ),
                type="circle"
            )
        ], style={'width': '100%', 'margin': '0'})
        
    ], style={
        'fontFamily': 'Arial, sans-serif',
        'maxWidth': '1400px',
        'margin': '0 auto', 
        'padding': '20px'
    })

def clear_cache():
    """Enhanced cache clearing"""
    global _cached_figure, _cached_data, _cached_reduced_data, _cached_geojson_path
    _cached_figure = None
    _cached_data = None
    _cached_reduced_data = {}
    _cached_geojson_path = None
    data_manager.clear_cache()
    print("All caches cleared")


@callback(
    Output('crime-map', 'figure'),
    [Input('max-points-slider', 'value')]
)
def update_map(max_points):
    """Fast update using optimized trace management"""

    if max_points == 3:  
        return update_crime_traces(create_initial_figure(), max_points)

    try:
        current_fig = create_initial_figure()
        return update_crime_traces(current_fig, max_points)
    except Exception as e:
        print(f"Update error: {e}")
        return update_crime_traces(create_initial_figure(), max_points)

