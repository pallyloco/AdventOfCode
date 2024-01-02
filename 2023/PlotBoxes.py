import plotly.graph_objects as go
import numpy as np
from plotly.graph_objects import Mesh3d


def plot_box(data: list[tuple[int, int, int, int, int, int]]):
    meshes: list[Mesh3d] = list()
    for box in data:
        x1, y1, z1, x2, y2, z2 = box

        # vertices
        x = [x1, x1, x2+1, x2+1, x2+1, x2+1, x1, x1]
        y = [y1, y1, y1, y1, y2+1, y2+1, y2+1, y2+1]
        z = [z1, z2+1, z1, z2+1, z2+1, z1, z2+1, z1]

        meshes.append(
            go.Mesh3d(
                # 8 vertices of a cube
                x = x, y = y, z = z,
                colorscale=[[0, 'gold'],
                            [0.5, 'mediumturquoise'],
                            [1, 'magenta']],
                # Intensity of each vertex, which will be interpolated and color-coded
                intensity=np.linspace(0, 1, 8, endpoint=True),
                # i, j and k give the vertices of triangles
                i=[0,1,2,4,1,1,1,0,4,5,2,0],
                j=[1,2,3,5,3,4,6,1,5,6,5,2],
                k=[2,3,4,2,4,6,7,7,6,7,7,7],
                # i=[0,1,2,4,],
                # j=[1,2,3,5,],
                # k=[2,3,4,2,],

            )
        )

    fig = go.Figure(data=meshes)

    fig.show()
