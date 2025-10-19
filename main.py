import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d



def epsilon(max_kx, max_ky, a, t, figsize, dpi, elev, azim, filename):
    """Compute and save the epsilon surface.

    Args:
        max_kx, max_ky: axis limits for kx and ky
        a, t: parameters for the dispersion
        figsize: tuple for figure size in inches
        dpi: image dots-per-inch when saving
        elev: elevation angle for 3D view
        azim: azimuth angle for 3D view
    """
    kx = np.linspace(-max_kx, max_kx, 200)
    ky = np.linspace(-max_ky, max_ky, 200)
    KX, KY = np.meshgrid(kx, ky)
    epsilon_p = t * np.sqrt(
        1 + 
        4 * (np.cos(3 * KX * a / 2)) * np.cos(np.sqrt(3) * KY * a / 2) + 
        np.cos(np.sqrt(3) * KY * a / 2)**2
    )
    epsilon_n = -epsilon_p
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


if __name__ == "__main__":
    # Example: larger figure and different camera angle
    epsilon(max_kx=2, max_ky=2, t=1, a=1, figsize=(9, 7), dpi=100, elev=0, azim=45, filename="small_kval_side_plot.png")
    epsilon(max_kx=1000, max_ky=1000, t=1, a=1, figsize=(9, 7), dpi=100, elev=0, azim=45, filename="large_kval_side_plot.png")
    epsilon(max_kx=2, max_ky=2, t=1, a=1, figsize=(9, 7), dpi=100, elev=25, azim=45, filename="small_kval_top_plot.png")
    epsilon(max_kx=1000, max_ky=1000, t=1, a=1, figsize=(9, 7), dpi=100, elev=25, azim=45, filename="large_kval_top_plot.png")