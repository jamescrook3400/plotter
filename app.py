# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import os

from astrodbkit import astrodb

def getLocale(search):
    if (search == "ra") or (search =="dec"):
        return "sources","id"
    if search == "parallax":
        return "parallaxes","source_id"
    if search == 'magnitude':
        return "photometry","source_id"
    if (search == "proper_motion_ra") or (search == "proper_motion_dec") or (search == "V_tan"):
        return "proper_motions","source_id"
    if search == "radial_velocity":
        return "radial_velocities","source_id"

def genTheList(x,y):
    
    dbpath = '/Users/jamescrook/Desktop/plotterApp/bdnycdev_20160723_kc.db'

    db = astrodb.Database(dbpath)
    
    x_loc = getLocale(x)[0]
    x_id = getLocale(x)[1]

    
    y_loc = getLocale(y)[0]
    y_id = getLocale(y)[1]
    
    xDica = db.query('select {}, {} from {}'.format(x_id, x, x_loc), fmt='dict')
    yDica = db.query('select {}, {} from {}'.format(y_id, y, y_loc), fmt = 'dict')
    
    xDic = {}
    yDic = {}
    xList = []
    yList = []
    
    for a in xDica:
        xDic[a[x_id]] = a[x]
    for a in yDica:
        yDic[a[y_id]] = a[y]
        
    for v in xDic:
        try:
            if (yDic[v] is not None) and (xDic[v] is not None):
                xList.append(xDic[v])
                yList.append(yDic[v])
        except:
            pass
        
    return xList, yList

app = dash.Dash()

app.layout = html.Div([
    html.H1(children = 'Plotter'),
    
    html.Label('Y'),
    dcc.Dropdown(
        id = 'y-axis',
        options = [
            {'label' : 'ra', 'value':'ra'},
            {'label' : 'dec', 'value' : 'dec'},
            {'label' : 'Parallax', 'value' : 'parallax'},
            {'label' : 'Magnitude', 'value' : 'magnitude'},
            {'label' : 'Proper Motion in ra', 'value' : 'proper_motion_ra'},
            {'label' : 'Proper Motion in dec', 'value' : 'proper_motion_dec'},
            {'label' : 'Tangential Velocity', 'value' : 'V_tan'},
            {'label' : 'Radial Velocity', 'value' : 'radial_velocity'}
            ]
        ),
    html.Label('X'),
    dcc.Dropdown(
        id = 'x-axis',
        options = [
            {'label' : 'ra', 'value':'ra'},
            {'label' : 'dec', 'value' : 'dec'},
            {'label' : 'Parallax', 'value' : 'parallax'},
            {'label' : 'Magnitude', 'value' : 'magnitude'},
            {'label' : 'Proper Motion in ra', 'value' : 'proper_motion_ra'},
            {'label' : 'Proper Motion in dec', 'value' : 'proper_motion_dec'},
            {'label' : 'Tangential Velocity', 'value' : 'V_tan'},
            {'label' : 'Radial Velocity', 'value' : 'radial_velocity'}
            ]
        ),
    
    dcc.Graph(
        id = 'graph_with_dropdown')
]) 

@app.callback(
    dash.dependencies.Output('graph_with_dropdown', 'figure'),
    [dash.dependencies.Input('x-axis','value'),
    dash.dependencies.Input('y-axis', 'value')])

def update_figure(x,y):
       xList, yList = genTheList(x,y)
                  
       return{
       
            'data': [
               go.Scatter(
                    x = xList,
                    y = yList,
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    }
                )
            ],
            'layout': go.Layout(
                xaxis={
                    'title': x
                },
                yaxis={
                    'title': y
                },
                hovermode='closest'
            )
      }

if __name__ == '__main__':
    app.run_server(debug=True)
