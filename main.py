import os
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, callback



def epsilon(max_kx, max_ky, a, t):
    """Compute and save the epsilon surface.

    Args:
        max_kx, max_ky: axis limits for kx and ky
        a, t: parameters for the dispersion
        figsize: tuple for figure size in inches
        dpi: image dots-per-inch when saving
        elev: elevation angle for 3D view
        azim: azimuth angle for 3D view
    """
    kx = np.linspace(-max_kx, max_kx, 100)
    ky = np.linspace(-max_ky, max_ky, 100)
    KX, KY = np.meshgrid(kx, ky)
    epsilon_p = t * np.sqrt(
        1 + 
        4 * (np.cos(3 * KX * a / 2)) * np.cos(np.sqrt(3) * KY * a / 2) + 
        np.cos(np.sqrt(3) * KY * a / 2)**2
    )
    epsilon_n = -epsilon_p
    return epsilon_p, epsilon_n, KX, KY, kx, ky


def plot_epsilon(epsilon_p, epsilon_n, KX, KY,figsize, dpi, elev, azim, filename):
    # Ensure output directory exists
    os.makedirs('images', exist_ok=True)

    # Creating a 3D plot with configurable size
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')

    # Plotting the basic 3D surface
    ax.plot_surface(KX, KY, epsilon_p, color='#0c89fa', linewidth=10, antialiased=True, alpha=0.9)
    ax.plot_surface(KX, KY, epsilon_n, color='#ed619f', linewidth=10, antialiased=True, alpha=0.9)

    # Customizing the plot
    ax.set_xlabel(r'$k_x$')
    ax.set_ylabel(r'$k_y$')
    ax.set_zlabel(r'$\varepsilon(k_x,k_y)$')
    ax.set_title('Basic 3D Surface Plot')

    # Set the viewing angle (camera)
    ax.view_init(elev=elev, azim=azim)

    # Tight layout and save
    plt.tight_layout()
    plt.savefig("images/" + filename, dpi=dpi)
    plt.close(fig)
    
    
def plotly_epsilon(large_epsilon_p, large_epsilon_n,epsilon_p, epsilon_n, kx, ky, large_kx, large_ky):
    #using plotly
    fig = go.Figure(data=[
        go.Surface(z=epsilon_p, x=kx, y=ky, name='εₚ',
                   colorscale=[[0, 'red'], [1, 'orange']], showscale=False, opacity=0.9, showlegend=True),
        go.Surface(z=epsilon_n, x=kx, y=ky, name='εₙ',
                   colorscale=[[0, 'blue'], [1, 'cyan']], showscale=False, opacity=0.9, showlegend=True)
    ])
    fig.update_layout(title='', autosize=True,
                  width=1000, height=700,
                  margin=dict(l=0, r=0, b=0, t=0))
    app = Dash()
    app.layout = html.Div([
        html.H1(children="2D Dispersion Relation For Graphene", 
                style={
            'textAlign': 'center'
            #,'color': colors['text']
        }),
        
        dcc.RadioItems(
            ['Small k values', 'Large k values'],
            'Small k values',
            id='k-vals',
            inline=True
        ),
        
        dcc.Graph(figure=fig, id='fig')
    ])
    
    @callback(
        Output("fig", "figure"),
        Input("k-vals", "value")
    )
    def update_graph(k_vals):
        if k_vals == "Small k values":
            fig = go.Figure(data=[
                go.Surface(z=epsilon_p, x=kx, y=ky, name='εₚ',
                           colorscale=[[0, 'red'], [1, 'orange']], showscale=False, opacity=0.9, showlegend=True),
                go.Surface(z=epsilon_n, x=kx, y=ky, name='εₙ',
                           colorscale=[[0, 'blue'], [1, 'cyan']], showscale=False, opacity=0.9, showlegend=True)
            ])
        else:
            fig = go.Figure(data=[
                go.Surface(z=large_epsilon_p, x=large_kx, y=large_ky, name='εₚ',
                           colorscale=[[0, 'red'], [1, 'orange']], showscale=False, opacity=0.9, showlegend=True),
                go.Surface(z=large_epsilon_n, x=large_kx, y=large_ky, name='εₙ',
                           colorscale=[[0, 'blue'], [1, 'cyan']], showscale=False, opacity=0.9, showlegend=True)
            ])
        fig.update_layout(title='', autosize=True,
                         width=1000, height=700,
                         margin=dict(l=0, r=0, b=0, t=0))
        return fig
    
    return app
        

    
    
    

if __name__ == "__main__":
    # Example: larger figure and different camera angle
    small_epsilon_p, small_epsilon_n, small_KX, small_KY, small_kx, small_ky = epsilon(max_kx=2, max_ky=2, t=1, a=1)
    plot_epsilon(epsilon_p=small_epsilon_p, epsilon_n=small_epsilon_n, KX=small_KX, KY=small_KY, figsize=(9, 7), dpi=100, elev=0, azim=45, filename="small_kval_side_plot.jpeg")
    plot_epsilon(epsilon_p=small_epsilon_p, epsilon_n=small_epsilon_n, KX=small_KX, KY=small_KY, figsize=(9, 7), dpi=100, elev=25, azim=45, filename="small_kval_top_plot.jpeg")
    
    large_epsilon_p, large_epsilon_n, large_KX, large_KY, large_kx, large_ky = epsilon(max_kx=50, max_ky=50, t=1, a=1)
    plot_epsilon(epsilon_p=large_epsilon_p, epsilon_n=large_epsilon_n, KX=large_KX, KY=large_KY, figsize=(9, 7), dpi=100, elev=0, azim=45, filename="large_kval_side_plot.jpeg")
    plot_epsilon(epsilon_p=large_epsilon_p, epsilon_n=large_epsilon_n, KX=large_KX, KY=large_KY, figsize=(9, 7), dpi=100, elev=25, azim=45, filename="large_kval_top_plot.jpeg")
    
    
    app = plotly_epsilon(large_epsilon_p=large_epsilon_p, large_epsilon_n= large_epsilon_n, epsilon_p=small_epsilon_p, epsilon_n=small_epsilon_n, kx=small_kx, ky=small_ky, large_kx=large_kx, large_ky=large_ky)
    app.run(debug=True, use_reloader=False)