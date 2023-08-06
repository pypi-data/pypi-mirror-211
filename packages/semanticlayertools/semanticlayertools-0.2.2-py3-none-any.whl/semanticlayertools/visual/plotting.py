import matplotlib.pyplot as plt
import igraph as ig
import pandas as pd
import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from datashader.bundling import hammer_bundle

colormap = cm.tab10.colors


class Multilayer3D():
    """Plot multiplex network.
    This solution is based on this StackOverflow answer:

    https://stackoverflow.com/questions/60392940/multi-layer-graph-in-networkx/60416989
    """
    def __init__(
        self, dataframes, graphLabels, comColors=colormap 
    ):
        self.dataframes: list = dataframes
        self.graphs = []
        self.graphLabels: list = graphLabels
        self.total_layers = len(dataframes)
        self.positions = {}
        self.node_to_community = {}
        self.community_to_color = {}
        self.nodeEdgePaths = []
        self.node_color = {}
        self.communityColors = comColors
  
    def createComposedGraphData(self):
        composedData = pd.concat(self.dataframes)
        composed = ig.Graph.TupleList([(x[0], x[2]) for x in composedData.itertuples(index=False)], directed=False)
        nodes = [x['name'] for x in composed.vs]
        nodeIndexDict = {idx: x['name'] for idx, x in enumerate(composed.vs)}
        layout = composed.layout_kamada_kawai()
        self.positions = {x: (y[0], y[1]) for x, y in zip(nodes, layout.coords)}
        nodePos = pd.DataFrame([(x, y[0], y[1]) for x, y in zip(nodes, layout.coords)], columns=['name', 'x', 'y'])
        edgesComposed = pd.DataFrame([(x.source_vertex['name'], x.target_vertex['name']) for x in composed.es], columns=["source", "target"])
        for idx, graph in enumerate(self.graphs):
            nodes = [x['name'] for x in graph.vs]
            edges = edgesComposed.query("source.isin(@nodes) and target.isin(@nodes)")
            nodepositions = nodePos.query('name.isin(@nodes)')
            nodepositions = nodepositions.set_index("name")
            hb = hammer_bundle(nodepositions, edges)
            hb.insert(2, 'z', idx)
            self.nodeEdgePaths.append(
                (nodepositions, edges, hb)
            )
        clustering = composed.community_multilevel(return_levels=False)
        mg = sorted(
            clustering,
            key=lambda x: len(x),
            reverse=True
        )
        for x, y in enumerate(mg):
            for elem in y:
                self.node_to_community.update({nodeIndexDict[elem]: x})
        self.community_to_color = {
            x: self.communityColors[x] for x in set(self.node_to_community.values()) if x < 10
        }

        for elem in set(self.node_to_community.values()):
            if elem >= 10:
                self.community_to_color.update({elem: (0.5, 0.5, 0.5)})

        self.node_color = {
            node: self.community_to_color[community_id] for node, community_id in self.node_to_community.items()
        }
        return

    def get_nodes(self):
        """Construct an internal representation of nodes with the format (node ID, layer)."""
        self.nodes = []
        for elem in self.dataframes:
            self.graphs.append(
                ig.Graph.TupleList([(x[0], x[2]) for x in elem.itertuples(index=False)], directed=False)
            )
        for z, g in enumerate(self.graphs):
            self.nodes.extend([(node['name'], z) for node in g.vs()])
        
    def get_edges_within_layers(self):
        """Remap edges in the individual layers to the internal representations of the node IDs."""
        self.edges_within_layers = []
        for z, g in enumerate(self.graphs):
            edgeList = [(e.source_vertex, e.target_vertex) for e in g.es()]
            self.edges_within_layers.extend([((source['name'], z), (target['name'], z)) for source, target in edgeList])

    def get_edges_between_layers(self):
        """Determine edges between layers. Nodes in subsequent layers are
        thought to be connected if they have the same ID."""
        self.edges_between_layers = []
        for z1, g in enumerate(self.graphs[:-1]):
            z2 = z1 + 1
            h = self.graphs[z2]
            vs1 = set([x['name'] for x in g.vs])
            vs2 = set([x['name'] for x in h.vs])
            shared_nodes = list(vs1.intersection(vs2))
            for node in shared_nodes:
                x = self.positions[node][0]
                y = self.positions[node][1]
                self.edges_between_layers.extend(
                    [((x, y, z1), (x, y, z2))]
                )

    def get_node_positions(self, *args, **kwargs):
        """Get the node positions in the layered layout."""
        self.node_positions = dict()
        for z, g in enumerate(self.graphs):
            self.node_positions.update({(node['name'], z): (*self.positions[node['name']], z) for node in g.vs()})
            
    def draw_nodes(self, nodes, *args, **kwargs):
        x, y, z = zip(*[self.node_positions[node] for node in nodes])
        colors = [self.community_to_color[self.node_to_community[x[0]]] for x in nodes] 
        self.ax.scatter(x, y, z, c=colors, *args, **kwargs)

    def draw_edges(self, edges, *args, **kwargs):
        line_collection = Line3DCollection(edges, *args, **kwargs)
        self.ax.add_collection3d(line_collection)

    def draw_edges_from_path(self, edgesData, *args, **kwargs):
        for layer in edgesData:
            hb = layer[2]
            hbnp = hb.to_numpy()
            splits = (np.isnan(hbnp[:, 0])).nonzero()[0]

            start = 0
            segments = []
            for stop in splits:
                seg = hbnp[start:stop, :]
                segments.append(seg[1:])
                start = stop
            for part in segments:
                newseg = []
                for idx, elem in enumerate(part):
                    if idx + 1 < len(part):
                        newseg.append((part[idx], part[idx + 1]))
                line_collection = Line3DCollection(newseg, *args, **kwargs)
                self.ax.add_collection3d(line_collection)
            
    def get_extent(self, pad=0.1):
        xyz = np.array(list(self.node_positions.values()))
        xmin, ymin, _ = np.min(xyz, axis=0)
        xmax, ymax, _ = np.max(xyz, axis=0)
        dx = xmax - xmin
        dy = ymax - ymin
        return (xmin - pad * dx, xmax + pad * dx), \
            (ymin - pad * dy, ymax + pad * dy)

    def draw_plane(self, z, *args, **kwargs):
        (xmin, xmax), (ymin, ymax) = self.get_extent(pad=0.1)
        u = np.linspace(xmin, xmax, 10)
        v = np.linspace(ymin, ymax, 10)
        U, V = np.meshgrid(u, v)
        W = z * np.ones_like(U)
        self.ax.plot_surface(U, V, W, *args, **kwargs)

    def prepareNetwork(self):
        self.get_nodes()
        self.createComposedGraphData()
        self.get_node_positions()
        self.get_edges_between_layers()

    def draw(self, textposition=(0.1, 1.1), ax=False):
        if ax:
            self.ax = ax
        else:
            fig = plt.figure()
            self.ax = fig.add_subplot(111, projection='3d')
        self.draw_edges_from_path(
            self.nodeEdgePaths,  color='k', alpha=0.05, linestyle='-', zorder=2
        )
        self.draw_edges(
            self.edges_between_layers, color='k', alpha=0.05, linestyle='dotted', zorder=2
        )

        for z in range(self.total_layers):
            self.draw_plane(z, alpha=0.1, zorder=1)
            self.draw_nodes([node for node in self.nodes if node[1] == z], s=100, zorder=3)
            self.ax.text(textposition[0], textposition[1], z, 'Layer ' + self.graphLabels[z])
