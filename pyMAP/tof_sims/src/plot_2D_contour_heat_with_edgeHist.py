import plotly.graph_objects as go

import numpy as np

#t = np.linspace(-1, 1.2, 2000)
x = clean_data_array[:,3].copy()
y = clean_data_array[:,11].copy()

fig = go.Figure()
fig.add_trace(go.Histogram2dContour(
        x = x,
        y = y,
        colorscale = 'Jet',
        contours = dict(
            showlabels = True,
            labelfont = dict(
                family = 'Raleway',
                color = 'white'
            )
        ),
        xaxis = 'x',
        yaxis = 'y', 
        contours_coloring="fill"
    ))
fig.add_trace(go.Histogram(
        y = y,
        xaxis = 'x2',
        marker = dict(
            color = 'rgba(0,0,0,1)'
        )
    ))
fig.add_trace(go.Histogram(
        x = x,
        yaxis = 'y2',
        marker = dict(
            color = 'rgba(0,0,0,1)'
        )
    ))

fig.update_layout(
    autosize = False,
    xaxis = dict(
        zeroline = False,
        domain = [0,0.85],
        showgrid = True
    ),
    yaxis = dict(
        zeroline = False,
        domain = [0,0.85],
        showgrid = True
    ),
    xaxis2 = dict(
        zeroline = False,
        domain = [0.85,1],
        showgrid = True
    ),
    yaxis2 = dict(
        zeroline = False,
        domain = [0.85,1],
        showgrid = True
    ),
    height = 600,
    width = 600,
    bargap = 0,
    hovermode = 'closest',
    showlegend = False
)

fig.show()

