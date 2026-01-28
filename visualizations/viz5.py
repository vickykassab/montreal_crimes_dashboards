import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from data_manager import data_manager


def get_season(m):
    return (
        "Winter" if m in [12, 1, 2] else
        "Spring" if m in [3, 4, 5] else
        "Summer" if m in [6, 7, 8] else
        "Fall"
    )

def get_processed_data():
    """Obtient et traite les données pour viz5 avec mise en cache"""
    df = data_manager.get_data_for_viz5()
    
    
    df = df.rename(columns={
        "CATEGORIE": "CrimeType",
        "LONGITUDE": "Longitude",
        "LATITUDE": "Latitude"
    })
    
   
    df = df.dropna(subset=["DATE"])
    df["Month"] = df["DATE"].dt.month
    df["Season"] = df["Month"].apply(get_season)
    df["CrimeType"] = df["CrimeType"].str.strip().str.lower().str.title()

  
    time_translation = {
        "Jour": "Day",
        "Soir": "Evening",
        "Nuit": "Night"
    }

    crime_translation = {
        "Vol De Véhicule À Moteur": "Motor Vehicle Theft",
        "Méfait": "Mischief",
        "Vol Dans / Sur Véhicule À Moteur": "Theft From/In Motor Vehicle",
        "Introduction": "Breaking And Entering",
        "Vols Qualifiés": "Robbery",
        "Infractions Entrainant La Mort": "Offences Causing Death"
    }

    df["QUART"] = df["QUART"].str.strip().str.capitalize().map(time_translation)
    df["CrimeType"] = df["CrimeType"].map(crime_translation).fillna(df["CrimeType"])
    
    return df

def get_heatmap_data():
    """Calcule les données pour les heatmaps avec mise en cache"""
    df = get_processed_data()
    
    heat_time = df.groupby(["CrimeType", "QUART"]).size().unstack(fill_value=0)
    heat_season = df.groupby(["CrimeType", "Season"]).size().unstack(fill_value=0)
    heat_year = df.groupby(["CrimeType", "YEAR"]).size().unstack(fill_value=0)
    
    return heat_time, heat_season, heat_year

def layout():
    heat_time, heat_season, heat_year = get_heatmap_data()
    
    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        z=heat_time.values,
        x=heat_time.columns,
        y=heat_time.index,
        colorscale="YlOrRd",
        colorbar_title="Number of Crimes",
        visible=True,
        name="Time of Day",
        hovertemplate="<b>Crime Type:</b> %{y}<br><b>Time:</b> %{x}<br><b>Count:</b> %{z}<extra></extra>"
    ))

    fig.add_trace(go.Heatmap(
        z=heat_season.values,
        x=heat_season.columns,
        y=heat_season.index,
        colorscale="YlOrRd",
        colorbar_title="Number of Crimes",
        visible=False,
        name="Season",
        hovertemplate="<b>Crime Type:</b> %{y}<br><b>Season:</b> %{x}<br><b>Count:</b> %{z}<extra></extra>"
    ))

    fig.add_trace(go.Heatmap(
        z=heat_year.values,
        x=heat_year.columns,
        y=heat_year.index,
        colorscale="YlOrRd",
        colorbar_title="Number of Crimes",
        visible=False,
        name="Year",
        hovertemplate="<b>Crime Type:</b> %{y}<br><b>Year:</b> %{x}<br><b>Count:</b> %{z}<extra></extra>"
    ))

    fig.update_layout(
    title="Crime Heatmap Analysis",
    xaxis_title="Time Period",
    yaxis_title="Crime Type",
    height=600,
    updatemenus=[
        dict(
            type="dropdown",
            direction="down",
            buttons=list([
                dict(
                    args=[{"visible": [True, False, False]}],
                    label="By Time of Day",
                    method="restyle"
                ),
                dict(
                    args=[{"visible": [False, True, False]}],
                    label="By Season",
                    method="restyle"
                ),
                dict(
                    args=[{"visible": [False, False, True]}],
                    label="By Year",
                    method="restyle"
                )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            x=1.0,         
            xanchor="right",
            y=1.15,        
            yanchor="top"
        ),
    ]
)

    return html.Div([
        html.H3("Crime Heatmap Analysis"),
        html.P("Interactive heatmaps showing crime patterns across different time dimensions. Use the buttons above the chart to switch between views."),
        dcc.Graph(figure=fig)
    ])

