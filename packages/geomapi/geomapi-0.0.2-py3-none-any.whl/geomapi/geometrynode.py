"""
GeometryNode - a Python Class to govern the data and metadata of geometric data (Mesh, BIM, PCD)
"""

#IMPORT MODULES
from geomapi.node import Node
import geomapi.utils as ut
import geomapi.geometryutils as gt
import open3d as o3d 

class GeometryNode (Node):
    # class attributes

    def __init__(self): 
        #instance attributes        
        super().__init__()
        self.cartesianBounds=None     # (nparray [6x1]) [xMin,xMax,yMin,yMax,zMin,zMax]
        self.orientedBounds=None     # (nparray [6x1]) [xMin,xMax,yMin,yMax,zMin,zMax]
        self.oriendtedBoundingBox=None # (open3d.geometry.OrientedBoundingBox) 
        # self.features3d= None #o3d.registration.Feature() # http://www.open3d.org/docs/0.9.0/python_api/open3d.registration.Feature.html
    
    def get_bounding_box(self)->o3d.geometry.OrientedBoundingBox:
        """Gets the Open3D geometry from cartesianBounds or orientedBounds

        Returns:
            o3d.geometry.OrientedBoundingBox: Open3D Geometry
        """
        if getattr(self,'cartesianBounds',None) is not None:
            box=gt.cartesian_bounds_to_open3d_axis_aligned_bounding_box(self.cartesianBounds)
        elif getattr(self,'orientedBounds',None) is not None:
            box=gt.oriented_bounds_to_open3d_oriented_bounding_box(self.orientedBounds)
        else:
             return None
        return box

    def visualize(self):
        vis = o3d.visualization.Visualizer()
        vis.create_window()

        if getattr(self,'mesh',None) is not None:
            vis.add_geometry(self.mesh)
        elif getattr(self,'pcd',None) is not None:
            vis.add_geometry(self.pcd)
        else:
            return None
        vis.run()
        vis.destroy_window()