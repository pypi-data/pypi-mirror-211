'''
This submodule contains utility functions
'''

import numpy as np
import numpy.typing as npt
from .objects import Ray
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_zcw_rays(density: int) -> list[Ray]:
    '''
    Generate a set of rays emanating from a single point using the ZCW
    algorithm

    See Appendix I in
    Eden, M.; Levitt, M. H. J. Magn. Res., 1998, 132, 220-239.

    Parameters
    ----------
    density : int
        Density number for ZCW algorithm

    Returns
    -------
    list[Ray]
        List of ray objects
    '''

    g = [recursive_g(m) for m in range(density + 3)]
    N = g[density + 2]

    c = [1, 2, 1]

    rays = [
        Ray(
            np.arccos(c[0] * (c[1] * np.fmod(j / N, 1) - 1)),
            2 * np.pi / c[2] * np.fmod(j * g[density] / N, 1)
        ) for j in range(N)
    ]

    return rays


def recursive_g(m: int) -> int:
    '''
    Recursively calculates numbers g_m required by ZCW integration scheme

    Parameters
    ----------
    m : int
        m index

    Returns
    -------
    int
        g_m value for given m

    '''

    if m == 0:
        g = 8
    elif m == 1:
        g = 13
    else:
        g = recursive_g(m - 2) + recursive_g(m - 1)

    return g


def plot_rays(vecs: npt.NDArray, clusters: npt.NDArray, n_clust: int,
              show: bool = True, fig: go.Figure = None,
              colours: list[str] = None) -> None:
    '''
    Create a plot of unblocked rays for web browser using plotly

    Parameters
    ----------
    vecs : np.ndarray[float]
        (3,n_unblocked_rays) array containing xyz vectors of unblocked rays
    clusters : np.ndarray[int]
        Integers specifying which cluster each ray belongs to
    n_clust : int
        Number of clusters
    show : bool
        If true, displays figure in browser
    fig : go.Figure
        If provided, rays are added to this figure
    colours : list[str]
        List of colours, one per cluster formatted as\n
        [\n
            'rgb(VAL, VAL, VAL)',\n
            'rgb(VAL, VAL, VAL)',\n
            ...\n
        ]\n
        where VAL is Red, Green, Blue in range(0, 255)

    Returns
    -------
    go.Figure
        Figure of unblocked rays as points
    '''

    if not colours:
        colours = [
            'rgb(51 , 34 , 136)',
            'rgb(17 , 119, 51)',
            'rgb(68 , 170, 153)',
            'rgb(136, 204, 238)',
            'rgb(221, 204, 119)',
            'rgb(204, 102, 119)',
            'rgb(170, 68 , 153)',
            'rgb(136, 34 , 85)',
            'rgb(0  , 0  , 0)',
            'rgb(230, 159, 0)',
            'rgb(86 , 180, 233)',
            'rgb(0  , 158, 115)',
            'rgb(240, 228, 66)',
            'rgb(0  , 114, 178)',
            'rgb(213, 94 , 0)',
            'rgb(204, 121, 167)',
        ]

    if fig is None:
        fig = make_subplots()
    for cl in range(n_clust):
        # Unblocked rays
        fig.add_trace(
            go.Scatter3d(
                x=vecs[clusters == cl, 0],
                y=vecs[clusters == cl, 1],
                z=vecs[clusters == cl, 2],
                mode='markers',
                marker={'color': colours[cl]},
                showlegend=False
            )
        )

    # Turn off plotly gubbins
    layout = go.Layout(
        hovermode=False,
        dragmode='orbit',
        scene_aspectmode='cube',
        scene=dict(
            xaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=False,
                showgrid=False,
                zeroline=False,
                title='',
                showline=False,
                ticks='',
                showticklabels=False,
                backgroundcolor='rgb(255, 255,255)',
            ),
            yaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showgrid=False,
                zeroline=False,
                title='',
                showline=False,
                ticks='',
                showticklabels=False,
                backgroundcolor='rgb(255, 255,255)',
            ),
            zaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showgrid=False,
                title='',
                zeroline=False,
                showline=False,
                ticks='',
                showticklabels=False,
                backgroundcolor='rgb(255, 255,255)',
            ),
            aspectratio=dict(
                x=1,
                y=1,
                z=1
            ),
        ),
        margin={
            'l': 20,
            'r': 30,
            't': 30,
            'b': 20
        }
    )

    fig.update_layout(layout)

    if show:
        fig.show()

    return fig
