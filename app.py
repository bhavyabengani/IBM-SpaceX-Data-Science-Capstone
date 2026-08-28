import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df=pd.read_csv("data/spacex_launch_dash.csv")
app=Dash(__name__)
app.layout=html.Div([
    html.H1("SpaceX Falcon 9 Launch Dashboard"),
    html.Label("Launch site"),
    dcc.Dropdown(sorted(df.LaunchSite.unique()), sorted(df.LaunchSite.unique()), id="site", multi=True),
    dcc.Graph(id="success-pie"),
    dcc.Graph(id="outcome-scatter")
])

@app.callback(Output("success-pie","figure"), Output("outcome-scatter","figure"), Input("site","value"))
def update(site):
    d=df[df.LaunchSite.isin(site)] if site else df
    counts=d.groupby("LaunchSite",as_index=False)["Class"].sum().rename(columns={"Class":"SuccessfulLandings"})
    pie=px.pie(counts,names="LaunchSite",values="SuccessfulLandings",title="Successful landings by site")
    scatter=px.scatter(d,x="FlightNumber",y="Class",color="LaunchSite",title="Launch outcome (1=success, 0=failure)")
    return pie,scatter

if __name__=="__main__":
    app.run(debug=True)
