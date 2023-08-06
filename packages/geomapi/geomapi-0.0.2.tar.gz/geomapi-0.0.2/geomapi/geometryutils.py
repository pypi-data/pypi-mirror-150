"""
Geometrytools - a Python library for processing mesh and point cloud data.
"""

#trimesh
#PyMesh
#pygalmesh => builds upon eigen and cgal
#Plyable

#IMPORT PACKAGES
# import trimesh

from ast import Try
from lib2to3.pytree import Node
from turtle import shape
from xmlrpc.client import Boolean
import numpy as np 
import cv2 
import open3d as o3d 
import json  
import os 
import re
import uuid    
import ntpath
import copy

import matplotlib.pyplot as plt #conda install -c conda-forge matplotlib
#import torch #conda install -c pytorch pytorch
import pye57 #conda install xerces-c  =>  pip install pye57
import xml.etree.ElementTree as ET 
import math
from datetime import datetime
from typing import List

# import APIs
import rdflib
from rdflib import Graph, plugin
from rdflib.serializer import Serializer #pip install rdflib-jsonld https://pypi.org/project/rdflib-jsonld/
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD
import ifcopenshell
import ifcopenshell.geom as geom
import ifcopenshell.util
from ifcopenshell.util.selector import Selector
import multiprocessing
from scipy.spatial.transform import Rotation as R

import trimesh

#IMPORT MODULES watch out for circular imports
import geomapi
# import geomapi.pointcloudnode
# import geomapi.meshnode
# import geomapi.imagenode
# import geomapi.bimnode
# import geomapi.linkeddatatools as ld

def mesh_to_pcd(mesh:o3d.geometry.TriangleMesh,voxelSize : float = 0.1) -> o3d.geometry.PointCloud:
    """Sample a point cloud on a triangle mesh (Open3D)

    Args:
        mesh (o3d.geometry.TriangleMesh) : source geometry
        voxel_size (float) : spatial resolution of the point cloud e.g. 0.1m

    Returns:
        An o3d.geometry.PointCloud() 
    """
    pcd = o3d.geometry.PointCloud()
    for submesh in mesh:
        k = round(submesh.get_surface_area() * 1000)
        submeshpcd = submesh.sample_points_uniformly(number_of_points = k, use_triangle_normal=True)
        pcd.__iadd__(submeshpcd)
    pcd = pcd.voxel_down_sample(voxelSize)    
    return pcd


def e57_to_pcd(e57Path, e57Index) ->o3d.geometry.PointCloud:
    """Convert pye57.E57scan to o3d.geometry.PointCloud

    Args:
        e57scan

    Returns:
        o3d.geometry.PointCloud
    """
    try:
        e57 = pye57.E57(e57Path)

        #get transformation
        header = e57.get_header(e57Index)
        quaternion=header.rotation
        translation=header.translation
        r = R.from_quat([quaternion[3],quaternion[0],quaternion[1],quaternion[2]])
        rotation_matrix=e57_fix_rotation_order(r.as_matrix())
        transform=rotation_and_translation_to_transformation_matrix(rotation_matrix,translation)

        #get raw geometry (no transformation)
        raw_data = e57.read_scan_raw(e57Index)        
        x_ndarray=raw_data.get('cartesianX')
        y_ndarray=raw_data.get('cartesianY')
        z_ndarray=raw_data.get('cartesianZ')
        array= np.vstack(( x_ndarray,y_ndarray,z_ndarray)).T
        points = o3d.utility.Vector3dVector(array)
        pcd=o3d.geometry.PointCloud(points)
        pcd.transform(transform)

        #get color or intensity
        colors=e57_get_colors(raw_data)
        if colors is not None:
            pcd.colors=colors

        #return transformed data
        return pcd
    except:
        print("Conversion from e57 to o3d.geometry.PointCloud failed!")
        return None    

def e57_get_colors(raw_data):
    """
    Extract color of intensity information from e57 raw data (3D data) and output Open3D o3d.utility.Vector3dVector(colors) 
    """   
    try:
        colorRed=raw_data.get('colorRed')
        colorGreen=raw_data.get('colorGreen')
        colorBlue=raw_data.get('colorBlue')
        intensity=raw_data.get('intensity')

        if colorRed is not None and colorGreen is not None and colorBlue is not None:
            if np.amax(colorRed)<=1:
                colors=np.c_[colorRed , colorGreen,colorBlue ]  
            elif np.amax(colorRed) <=255:
                colors=np.c_[colorRed/255 , colorGreen/255,colorBlue/255 ]  
            else:
                colorRed=(colorRed - np.min(colorRed))/np.ptp(colorRed)
                colorGreen=(colorGreen - np.min(colorGreen))/np.ptp(colorGreen)
                colorBlue=(colorBlue - np.min(colorBlue))/np.ptp(colorBlue)
                colors=np.c_[colorRed , colorGreen,colorBlue ]  
            return o3d.utility.Vector3dVector(colors) 

        elif intensity is not None:
            if np.amax(intensity) <=1:
                colors=np.c_[intensity , intensity,intensity ]  
            else:
                intensity=(intensity - np.min(intensity))/np.ptp(intensity)
                colors=np.c_[intensity , intensity,intensity ]  
            return o3d.utility.Vector3dVector(colors) 
    except:
        return None
    return None


def e57_fix_rotation_order(rotation_matrix:np.array) -> np.array:
    """
    thix switches the rotation from clockwise to counter-clockwise
    https://robotics.stackexchange.com/questions/10702/rotation-matrix-sign-convention-confusion
    Currently only changes the signs of elements [0,1,5,8]
    """
    r=rotation_matrix
    return [[-r[0,0],-r[0,1],r[0,2]],
            [r[1,0],r[1,1],-r[1,2]],
            [r[2,0],r[2,1],-r[2,2]]]

def mesh_intersection(mesh: o3d.geometry.TriangleMesh, cuttingMeshes: List[o3d.geometry.TriangleMesh] ) -> List[o3d.geometry.TriangleMesh]:
    """
    Compute the mesh intersection between 2 o3d.geometry.TriangleMeshes or pygalmesh.mesh elements
    NOT IMPLEMENTED
    """
    
    # # if Mesh
    # # find vertices
    # mesh=o3d.geometry.TriangleMesh()
    # mesh.vertices 


    # mesh.remove_vertices_by_index()
    # mesh.remove_triangles_by_index()
    # points=mesh.vertices
    # faces=mesh.triangles
    # mesh.merge_close_vertices(0.01)
    # mesh.remove_duplicated_vertices()
    # triangle_mask=False*len(mesh.triangles)
    # cleanedMesh=mesh.remove_triangles_by_mask(triangle_mask)
    # mesh.remove_unreferenced_vertices()

    # CleanedMesh=mesh.select_by_index(indices,cleanup=True)
    # smoothMesh=mesh.subdivide_midpoint(1)
    
    return False

def crop_geometry(geometry:o3d.geometry, box:o3d.geometry.OrientedBoundingBox, subdivide:int = 0) ->o3d.geometry.TriangleMesh:
    """"Crop portion of a mesh/pointcloud that lies within an OrientedBoundingBox 

    Args:
        geometry (o3d.geometry.TriangleMesh or o3d.geometry.PointCloud)
        box (o3d.geometry.OrientedBoundingBox )
        subdivide (int): number of interations to increase the density of the mesh (1=x4, 2=x16, etc.)
        
    Returns:
        mesh:       o3d.geometry.TriangleMesh 
        None:       if no data was retained
    """
    # transform box to axis aligned box 
    r=box.R
    t=box.center
    transformedbox=copy.deepcopy(box)
    transformedbox=transformedbox.translate(-t)
    transformedbox=transformedbox.rotate(r.transpose(),center=(0, 0, 0))
    
    # transform geometry to coordinate system of the box
    transformedGeometry=copy.deepcopy(geometry)
    transformedGeometry=transformedGeometry.translate(-t)
    transformedGeometry=transformedGeometry.rotate(r.transpose(),center=(0, 0, 0))

    # convert to pcd if geometry is a mesh (crop fails with mesh geometry)
    if type(geometry) is o3d.geometry.PointCloud:
        croppedGeometry=geometry.crop(transformedbox)             
    elif type(geometry) is o3d.geometry.TriangleMesh:
        if subdivide!=0:
            transformedGeometry=transformedGeometry.subdivide_midpoint(subdivide)
        indices=transformedbox.get_point_indices_within_bounding_box(transformedGeometry.vertices) # this is empty
        if len(indices) !=0:
            croppedGeometry=transformedGeometry.select_by_index(indices,cleanup=True)
        else:
            return None

    # return croppedGeometry to original position
    if croppedGeometry is not None:
        croppedGeometry=croppedGeometry.rotate(r,center=(0, 0, 0))
        croppedGeometry=croppedGeometry.translate(t)
        return croppedGeometry
    else:
        return None

def expand_box (box: o3d.geometry.OrientedBoundingBox, u=5.0,v=5.0,z=5.0) -> o3d.geometry.OrientedBoundingBox:
    """
    expand an o3d.geometry.OrientedBoundingBox in u, v and z direction with a certain offset
    """
    center = box.get_center()
    orientation = box.R 
    extent = box.extent + [u, z, v] #check this order
    return o3d.geometry.OrientedBoundingBox(center,orientation,extent) 


# def crop_mesh2(mesh:o3d.geometry.TriangleMesh, geometry:o3d.geometry) ->o3d.geometry.TriangleMesh:
#     """"
#     NOT IMPLEMENTED
#     """
#     # test which indices are within box
#     hull=geometry.compute_convex_hull()

#     box.get_box_points()


def join_geometries(geometries):
    if type(geometries) is o3d.geometry.TriangleMesh:
        joined=o3d.geometry.TriangleMesh()
        for geometry in geometries:
            if geometry is not None and len(geometry.vertices) != 0:
                joined +=geometry
        return joined
    elif type(geometries) is o3d.geometry.PointCloud:
        joined=o3d.geometry.PointCloud()
        for geometry in geometries:
            if geometry is not None and len(geometry.points) != 0:
                joined +=geometry
        return joined
    else:
        print('submit point clouds or meshes')
        return None

def pointcloud_filter_by_distance(source: o3d.geometry.PointCloud, cutters, threshold : float =0.10) -> o3d.geometry.PointCloud:
    """"Select the portion of a pointcloud that lies within a range of another mesh/point cloud 
    
    Args:
        source (o3d.geometry.PointCloud) : point cloud to filter
        cutters (o3d.geometry.TriangleMesh or o3d.geometry.PointCloud): list of reference data
        threshold (float): threshold Euclidean distance for the filtering
        invert (bool): 'True' to retain point closer by than a threshold

    Returns:
        outputmesh(o3d.geometry.PointCloud)
    """
    #if no list, list
    cutters=item_to_list(cutters)
    joined=join_geometries(cutters)

    #if cutters are mesh, sample mesh
    if type(cutters) is o3d.geometry.TriangleMesh:
        reference=joined.sample_points_uniformly(number_of_points=1000000) 
    elif type(cutters) is o3d.geometry.PointCloud:
        reference=joined
    else:
        print('submit point cloud or  mesh as cutters')
        return None

    distances=source.compute_point_cloud_distance(reference) #10s to calculate
    indices=[ idx for idx,distance in enumerate(distances) if distance <threshold] #this takes 30s
    if len(indices) !=0:
        return source.select_by_index(indices)
    else:
        return None 

def mesh_intersection_raycasting(source:o3d.geometry.TriangleMesh, cutter: o3d.geometry.TriangleMesh, inside : Boolean = True,strict : Boolean = True ) -> o3d.geometry.TriangleMesh:
    """"Select portion of a mesh that lies within a mesh shape (if not closed, convexhull is called)
    
    Args:
        source (o3d.geometry.TriangleMesh) : mesh to cut
        cutter (o3d.geometry.TriangleMesh) : mesh that cuts
        inside (bool): 'True' to retain inside
        strict (bool): 'True' if no face vertex is allowed outside the bounds, 'False' allows 1 vertex to lie outside

    Returns:
        outputmesh(o3d.geometry.TriangleMesh)
    """
    #check if cutter is closed 
    if not cutter.is_watertight():
        cutter=cutter.compute_convex_hull()

    #check if mesh has normals? not needed

    #raycast the scene to determine which points are inside
    query_points=o3d.core.Tensor(np.asarray(source.vertices),dtype=o3d.core.Dtype.Float32 )
    cpuMesh = o3d.t.geometry.TriangleMesh.from_legacy(cutter)
    scene = o3d.t.geometry.RaycastingScene()
    geometry = scene.add_triangles(cpuMesh)
    ans=scene.compute_occupancy(query_points)
    
    if inside:
        occupancyList=ans==0
    else:
        occupancyList=ans>0

    outputmesh=copy.deepcopy(source)
    if strict:
        outputmesh.remove_vertices_by_mask(occupancyList)
        outputmesh.remove_degenerate_triangles()
        outputmesh.remove_unreferenced_vertices
    else:
        triangles=copy.deepcopy(np.asarray(outputmesh.triangles)) #can we remove this one?
        indices= [i for i, x in enumerate(occupancyList) if x == True]
        #mark all unwanted points as -1
        triangles[~np.isin(triangles,indices)] = -1
        # if 2/3 vertices are outside, flag the face
        occupancyList=np.ones ((triangles.shape[0],1), dtype=bool)

        for idx,row in enumerate(triangles):
            if (row[0] ==-1 and row[1]==-1) or (row[0] ==-1 and row[2]==-1) or (row[1] ==-1 and row[2]==-1):
                occupancyList[idx]=False
        outputmesh.remove_triangles_by_mask(occupancyList)
        outputmesh.remove_unreferenced_vertices()
    return outputmesh

def mesh_intersection_convex_hull(source:trimesh.Trimesh, cutter: trimesh.Trimesh, inside : Boolean = True ) -> trimesh.Trimesh:
    """"Cut a portion of a mesh that lies within/outside the convex hull of another mesh
    
    Args:
        source (trimesh.Trimesh):   mesh that will be cut
        cutter (trimesh.Trimesh):   mesh of which the faces are used for the cuts. Face normals should point outwards (positive side)
        inside (Boolean):           True if retain the inside of the intersection
    Returns:
        mesh:       trimesh.Trimesh 
        None:       if no data was retained
    """
    #compute faces and centers
    convexhull=cutter.convex_hull
    plane_normals=convexhull.face_normals
    plane_origins=convexhull.triangles_center

    if inside: # retain inside
        return(source.slice_plane(plane_origins, -1*plane_normals))
    else:# retain outside
        #cut source mesh for every slicing plane on the box
        meshes=[]
        for n, o in zip(plane_normals, plane_origins):
            tempMesh= source.slice_plane(o, n)
            if not tempMesh.is_empty:
                meshes.append(tempMesh)
        if len(meshes) !=0: # gather pieces
            combined = trimesh.util.concatenate( [ meshes ] )
            combined.merge_vertices(merge_tex =True,merge_norm =True )
            combined.remove_duplicate_faces()
            return combined
        else:
            return None

def cap_mesh(test):
      # the plane we're using
    normal = trimesh.unitize([1,1,1])
    origin = m.center_mass

    # get a section as a Path3D object
    s = m.section(plane_origin=origin,
                  plane_normal=normal)

    # transform the Path3D onto the XY plane so we can triangulate
    on_plane, to_3D = s.to_planar()

    # triangulate each closed region of the 2D cap
    v, f = [], []
    for polygon in on_plane.polygons_full:
        tri = trimesh.creation.triangulate_polygon(polygon)
        v.append(tri[0])
        f.append(tri[1])
        
    # append the regions and re- index
    vf, ff = trimesh.util.append_faces(v, f)
    # three dimensionalize polygon vertices
    vf = np.column_stack((vf, np.zeros(len(vf))))
    # transform points back to original mesh frame
    vf = trimesh.transform_points(vf, to_3D)
    # flip winding of faces for cap
    ff = np.fliplr(ff)

    # the mesh for the planar cap
    cap = trimesh.Trimesh(vf, ff)

    # get the uncapped slice
    sliced = m.slice_plane(plane_origin=origin,
                           plane_normal=normal)

    # append the cap to the sliced mesh
    capped = sliced + cap

def open3d_box_to_mesh(box:o3d.geometry) ->o3d.geometry.TriangleMesh:
    if type(box) is o3d.geometry.OrientedBoundingBox or type(box) is o3d.geometry.AxisAlignedBoundingBox:
        mesh=o3d.geometry.TriangleMesh()
        mesh.vertices=box.get_box_points()
        #triangles rotate counterclockwise
        mesh.triangles= o3d.cpu.pybind.utility.Vector3iVector(np.array([[0,2,1],
                            [0,1,3],
                            [0,3,2],
                            [1,6,3],
                            [1,7,6],
                            [1,2,7],
                            [2,3,5],
                            [2,5,4],
                            [2,4,7],
                            [3,4,5],
                            [3,6,4],
                            [4,6,7]])) 
        return mesh                  
    else:
        print('Incorrect geometry input. Only input o3d.geometry.AxisAlignedBoundingBox or o3d.geometry.OrientedBoundingBox or type(geometry)  ')
        return None 

def get_box_inliers(sourceBox:o3d.geometry.OrientedBoundingBox, testBoxes: List[o3d.geometry.OrientedBoundingBox])->List[int]:
    """"
    Return the indices of the testBoxes of which the bounding points lie within the sourceBox

    Args:
        sourceBox (o3d.geometry.OrientedBoundingBox):   box to test
        testBoxes (o3d.geometry.OrientedBoundingBox):   boxes to test
    Returns:
        list (List[int]):       indices of testBoxes

    """
    #Convert to list
    testBoxes=item_to_list(testBoxes)

    array= [False] * len(testBoxes)
    for idx,testbox in enumerate(testBoxes):
        if testbox is not None:
            points=ld.get_oriented_bounds(testbox)
            indices=[]
            indices=sourceBox.get_point_indices_within_bounding_box(o3d.utility.Vector3dVector(points))
            if len(indices) !=0:
                array[idx]= True
    list = [ i for i in range(len(array)) if array[i]]
    return list

def item_to_list(item):
    if type (item) is list:
        return item
    else:
        return [item]

def get_box_intersections(sourceBox:o3d.geometry.OrientedBoundingBox, testBoxes: List[o3d.geometry.OrientedBoundingBox])->List[int]:
    """"
    return indices of testBoxes of which the geometry intersects with the sourceBox

    Args:
        sourceBox (o3d.geometry.OrientedBoundingBox):   box to test
        testBoxes (o3d.geometry.OrientedBoundingBox):   boxes to test
    Returns:
        list (List[int]):       indices of testBoxes

    """
    # 2 oriented bounding boxes (A,B) overlap if the projection from B in the coordinate system of A on all the axes overlap. 
    # The projection of B on the oriented axes of A is simply the coordinate range for that axis.
    
    #convert to list
    testBoxes=item_to_list(testBoxes)

    array= [False] * len(testBoxes)

    for idx,testbox in enumerate(testBoxes):
    # compute axes of box A
        if testbox is not None:
            #transform box to aligned coordinate system
            transformedboxA=copy.deepcopy(sourceBox)
            transformedboxA=transformedboxA.translate(-sourceBox.center)
            transformedboxA=transformedboxA.rotate(sourceBox.R.transpose(),center=(0, 0, 0))
            
            #transform testbox to aligned coordinate system
            transformedboxB=copy.deepcopy(testbox)
            transformedboxB=transformedboxB.translate(-sourceBox.center)
            transformedboxB=transformedboxB.rotate(sourceBox.R.transpose(),center=(0, 0, 0))

            # compute coordinates of bounding points of B in coordinate system of A
            minA=transformedboxA.get_min_bound()
            minB=transformedboxB.get_min_bound()
            maxA=transformedboxA.get_max_bound()
            maxB=transformedboxB.get_max_bound()

            if (maxB[0]>=minA[0] and minB[0]<=maxA[0]):
                if (maxB[1]>=minA[1] and minB[1]<=maxA[1]):
                    if (maxB[2]>=minA[2] and minB[2]<=maxA[2]):
                        array[idx]= True  
    # return index if B overlaps with A in all three axes u,v,w 
    list = [ i for i in range(len(array)) if array[i]]
    return list

def open3d_to_trimesh(geometry: o3d.geometry) -> trimesh.Trimesh:
    """
    Convert open3D.geometry.TriangleMesh to trimesh.Trimesh
    """
    if type(geometry) is o3d.geometry.OrientedBoundingBox or type(geometry) is o3d.geometry.AxisAlignedBoundingBox:
        geometry=open3d_box_to_mesh(geometry)
    
    if type(geometry) is o3d.geometry.TriangleMesh and len(geometry.vertices) !=0:
        vertices= geometry.vertices
        faces= geometry.triangles
        face_normals=None
        vertex_normals=None
        face_colors=None
        vertex_colors=None

        if geometry.has_triangle_normals():
            face_normals=geometry.triangle_normals
        if geometry.has_vertex_normals():
            vertex_normals=geometry.vertex_normals
        if geometry.has_triangle_uvs(): # this is probably not correct
            face_colors=geometry.triangle_uvs
        if geometry.has_vertex_colors():
            vertex_colors=geometry.vertex_colors

        try:
            triMesh= trimesh.Trimesh(vertices, faces, face_normals=face_normals, vertex_normals=vertex_normals, face_colors=face_colors, vertex_colors=vertex_colors)
            return triMesh
        except:
            print('Open3D to Trimesh failed')
            return None
    else:
        print('Incorrect geometry input. Only input o3d.geometry.TriangleMesh,o3d.geometry.AxisAlignedBoundingBox or o3d.geometry.OrientedBoundingBox or type(geometry)  ')
        return None

def get_center(mesh:o3d.geometry.TriangleMesh,triangle:np.array) -> np.array:
    """
    Compute center of an Open3D mesh face
    """
    points=np.array([mesh.vertices[triangle[0]],
                    mesh.vertices[triangle[1]],
                    mesh.vertices[triangle[2]]])
    # point4=mesh.vertices[triangle[3]] # check if Open3D supports quads
    if points.shape[1] ==3:        
        return np.mean(points,axis=0)
    else:
        return None

def get_triangle_centers(mesh:o3d.geometry.TriangleMesh) -> np.array:
    """
    Compute centers of all Open3D mesh faces
    """
    centers=np.empty((len(mesh.triangles),3))
    for idx,row in enumerate(mesh.triangles):
        points=np.array([mesh.vertices[row[0]],
                    mesh.vertices[row[1]],
                    mesh.vertices[row[2]]])
        centers[idx]=np.mean(points,axis=0)
    return centers

def visualize_geometry(geometry)->None:
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(geometry)
    vis.run()
    vis.destroy_window()


def rotation_and_translation_to_transformation_matrix(rotation: np.array, translation: np.array)->np.array:
    """
    rotation [3,3]
    translation [3,1]
    """
    r=np.asarray(rotation)
    if r.size==9 and len(translation) ==3:    
        return np.array([[ r[0,0],r[0,1],r[0,2], translation[0]],
                        [ r[1,0],r[1,1],r[1,2], translation[1]],
                        [ r[2,0],r[2,1],r[2,2], translation[2]],
                        [ 0,0,0,1]])
    else:
        return None

def cartesian_bounds_to_cartesian_transform(cartesianBounds:np.array) ->np.array:
    if len(cartesianBounds) !=6:
        return None
    else:
        matrix=np.zeros([4,4])
        np.fill_diagonal(matrix,1)
        matrix[3]=(cartesianBounds[1]-cartesianBounds[0])/2
        matrix[7]=(cartesianBounds[3]-cartesianBounds[2])/2
        matrix[11]=(cartesianBounds[5]-cartesianBounds[4])/2
        return matrix


def ifc_to_mesh(ifcElement:ifcopenshell.entity_instance)-> o3d.geometry.TriangleMesh: 
    """Convert an ifcOpenShell geometry to an Open3D TriangleMesh

    Args:
        ifcElement (ifcopenshell.entity_instance): IfcOpenShell Element parsed from and .ifc file. See BIMNode for more documentation.

    Returns:
        o3d.geometry.TriangleMesh: Open3D Mesh Geometry of the ifcElment boundary surface
    """    
    try:
        if ifcElement.get_info().get("Representation"): 
            # Set geometry settings and global coordinates as true
            settings = geom.settings() 
            settings.set(settings.USE_WORLD_COORDS, True) 
        
            # Extract vertices/faces of the IFC geometry
            shape = geom.create_shape(settings, ifcElement) 
            ifcVertices = shape.geometry.verts 
            ifcFaces = shape.geometry.faces 

            #Group the vertices and faces in a way they can be read by Open3D
            vertices = [[ifcVertices[i], ifcVertices[i + 1], ifcVertices[i + 2]] for i in range(0, len(ifcVertices), 3)]
            faces = [[ifcFaces[i], ifcFaces[i + 1], ifcFaces[i + 2]] for i in range(0, len(ifcFaces), 3)]

            #Convert grouped vertices/faces to Open3D objects 
            o3dVertices = o3d.utility.Vector3dVector(np.asarray(vertices))
            o3dTriangles = o3d.utility.Vector3iVector(np.asarray(faces))

            # Create the Open3D mesh object
            return o3d.geometry.TriangleMesh(o3dVertices,o3dTriangles) 
    except:
        print('ifcopenshell.entity_instance error')
        return None
  

def get_cartesian_bounds(geometry : o3d.geometry) ->np.array:
    """Get cartesian bounds from Open3D geometry

    Args:
        geometry (o3d.geometry): Open3D geometry supertype (PointCloud, TriangleMesh, OrientedBoundingBox, etc.)

    Returns:
        np.array: [xMin,xMax,yMin,yMax,zMin,zMax]
    """
    max=geometry.get_max_bound()
    min=geometry.get_min_bound()
    return np.array([min[0],max[0],min[1],max[1],min[2],max[2]])

def get_oriented_bounds(geometry : o3d.geometry ) -> np.array:
    """Get the 8 corner points of the oriented bounding box

    Args:
        geometry (o3d.geometry): Open3D geometry supertype (PointCloud, TriangleMesh, OrientedBoundingBox, etc.)

    Returns:
        np.array: [8x3]
    """
    orientedBoundingBox = geometry.get_oriented_bounding_box()
    return np.asarray(orientedBoundingBox.get_box_points())


def cartesian_bounds_to_open3d_axis_aligned_bounding_box(cartesianBounds:np.array) ->o3d.geometry.OrientedBoundingBox:
    """ NOT IMPLEMENTED    
    """
    pass

def oriented_bounds_to_open3d_oriented_bounding_box(orientedBounds : np.array) -> o3d.geometry.OrientedBoundingBox:
    """Convert 8 bounding points to Open3D Geometry

    Args:
        orientedBounds (np.array): [8x3] bounding points

    Returns:
        o3d.geometry.OrientedBoundingBox: Open3D Geometry
    """
    boxPointsVector = o3d.utility.Vector3dVector(orientedBounds)
    open3dOrientedBoundingBox = o3d.geometry.OrientedBoundingBox.create_from_points(boxPointsVector)
    return open3dOrientedBoundingBox

def get_center_of_oriented_bounds(orientedBounds: np.array) -> np.array:
    boxPointsVector = o3d.utility.Vector3dVector(orientedBounds)
    open3dOrientedBoundingBox = o3d.geometry.OrientedBoundingBox.create_from_points(boxPointsVector)
    return np.asarray(open3dOrientedBoundingBox.get_center())

def get_rotation_of_oriented_bounds(orientedBounds: np.array) -> np.array:
    boxPointsVector = o3d.utility.Vector3dVector(orientedBounds)
    open3dOrientedBoundingBox = o3d.geometry.OrientedBoundingBox.create_from_points(boxPointsVector)
    return np.asarray(open3dOrientedBoundingBox.R)

def get_center_of_cartesian_bounds(cartesianBounds:np.array)-> np.array:
    if cartesianBounds.size ==6:
        x=(cartesianBounds[1]-cartesianBounds[0])/2
        y=(cartesianBounds[3]-cartesianBounds[2])/2
        z=(cartesianBounds[5]-cartesianBounds[4])/2
        return np.array([x,y,z])
    else:
        return None

def get_center_of_points(points:np.array)-> np.array: 
    if points.shape[1] ==3:        
        return np.mean(points,axis=0)
    else:
        return None

def get_bounding_points(cartesianBounds:np.array) -> List[o3d.utility.Vector3dVector]:
    array=np.empty((8,3))
    xMin=cartesianBounds[0]
    xMax=cartesianBounds[1]
    yMin=cartesianBounds[2]
    yMax=cartesianBounds[3]
    zMin=cartesianBounds[4]
    zMax=cartesianBounds[5]

    #maybe these should be ordered a bit more 
    array[0]=np.array([xMin,yMin,zMin])
    array[1]=np.array([xMin,yMin,zMax])
    array[2]=np.array([xMin,yMax,zMin])
    array[3]=np.array([xMin,yMax,zMax])
    array[4]=np.array([xMax,yMin,zMin])
    array[5]=np.array([xMax,yMin,zMax])
    array[6]=np.array([xMax,yMax,zMin])
    array[7]=np.array([xMax,yMax,zMax])

    return o3d.utility.Vector3dVector(array)

def get_translation(cartesianTransform:np.array) -> np.array:
    if cartesianTransform.size ==16:
        return np.array([cartesianTransform[0,3],cartesianTransform[1,3],cartesianTransform[2,3]])
    else:
        return None

def lambert72_to_spherical_coordinates(x :float ,y:float) -> tuple: 
    """"
    Belgian Lambert 1972---> Spherical coordinates
    Input parameters : X, Y = Belgian coordinates in meters
    Output : latitude and longitude in Belgium Datum!
    source: http://zoologie.umons.ac.be/tc/algorithms.aspx
    """
    LongRef = 0.076042943  #      '=4°21'24"983
    nLamb  = 0.7716421928 #
    aCarre = 6378388 ^ 2 #
    bLamb = 6378388 * (1 - (1 / 297)) #
    eCarre = (aCarre - bLamb ^ 2) / aCarre #
    KLamb = 11565915.812935 #
    
    eLamb = math.Sqrt(eCarre)
    eSur2 = eLamb / 2
    
    Tan1  = (x - 150000.01256) / (5400088.4378 - y)
    Lambda = LongRef + (1 / nLamb) * (0.000142043 + math.Atan(Tan1))
    RLamb = math.Sqrt((x - 150000.01256) ^ 2 + (5400088.4378 - y) ^ 2)
    
    TanZDemi = (RLamb / KLamb) ^ (1 / nLamb)
    Lati1 = 2 * math.Atan(TanZDemi)
    
    eSin=0.0
    Mult1=0.0
    Mult2=0.0
    Mult=0.0
    LatiN=0.0
    Diff=1     

    while math.Abs(Diff) > 0.0000000277777:
        eSin = eLamb * math.Sin(Lati1)
        Mult1 = 1 - eSin
        Mult2 = 1 + eSin
        Mult = (Mult1 / Mult2) ^ (eLamb / 2)
        LatiN = (math.PI / 2) - (2 * (math.Atan(TanZDemi * Mult)))
        Diff = LatiN - Lati1
        Lati1 = LatiN
    
    latBel = (LatiN * 180) / math.PI
    lngBel = (Lambda * 180) / math.PI
    return latBel,lngBel

def spherical_coordinates_to_lambert72(latBel :float,lngBel:float) -> tuple:
    """
    Conversion from spherical coordinates to Lambert 72
    Input parameters : lat, lng (spherical coordinates)
    Spherical coordinates are in decimal degrees converted to Belgium datum!
    source: http://zoologie.umons.ac.be/tc/algorithms.aspx
    """
 
    LongRef  = 0.076042943  #      '=4°21'24"983
    bLamb  = 6378388 * (1 - (1 / 297))
    aCarre  = 6378388 ^ 2
    eCarre = (aCarre - bLamb ^ 2) / aCarre
    KLamb = 11565915.812935
    nLamb = 0.7716421928
    
    eLamb  = math.Sqrt(eCarre)
    eSur2  = eLamb / 2
    
    #conversion to radians
    lat = (math.PI / 180) * latBel
    lng = (math.PI / 180) * lngBel
    
    eSinLatitude = eLamb * math.Sin(lat)
    TanZDemi = (math.Tan((math.PI / 4) - (lat / 2))) *  (((1 + (eSinLatitude)) / (1 - (eSinLatitude))) ^ (eSur2))
    
    RLamb= KLamb * ((TanZDemi) ^ nLamb)
    
    Teta  = nLamb * (lng - LongRef)
        
    x = 150000 + 0.01256 + RLamb * math.Sin(Teta - 0.000142043)
    y = 5400000 + 88.4378 - RLamb * math.Cos(Teta - 0.000142043)
    return x,y

def belgian_datum_to_wgs84(latBel:float,lngBel:float) -> tuple:
    """
    Input parameters : Lat, Lng : latitude / longitude in decimal degrees and in Belgian 1972 datum
    Output parameters : LatWGS84, LngWGS84 : latitude / longitude in decimal degrees and in WGS84 datum
    source: http://zoologie.umons.ac.be/tc/algorithms.aspx
    """
    Haut = 0.0   
        
    #conversion to radians
    Lat = (math.PI / 180) * latBel
    Lng = (math.PI / 180) * lngBel
    
    SinLat = math.Sin(Lat)
    SinLng = math.Sin(Lng)
    CoSinLat = math.Cos(Lat)
    CoSinLng = math.Cos(Lng)
    
    dx = -125.8
    dy = 79.9
    dz = -100.5
    da = -251.0
    df = -0.000014192702
    
    LWf = 1 / 297
    LWa = 6378388
    LWb = (1 - LWf) * LWa
    LWe2 = (2 * LWf) - (LWf * LWf)
    Adb = 1 / (1 - LWf)
    
    Rn = LWa / math.Sqrt(1 - LWe2 * SinLat * SinLat)
    Rm = LWa * (1 - LWe2) / (1 - LWe2 * Lat * Lat) ^ 1.5
    
    DLat = -dx * SinLat * CoSinLng - dy * SinLat * SinLng + dz * CoSinLat
    DLat = DLat + da * (Rn * LWe2 * SinLat * CoSinLat) / LWa
    DLat = DLat + df * (Rm * Adb + Rn / Adb) * SinLat * CoSinLat
    DLat = DLat / (Rm + Haut)
    
    DLng = (-dx * SinLng + dy * CoSinLng) / ((Rn + Haut) * CoSinLat)
    Dh = dx * CoSinLat * CoSinLng + dy * CoSinLat * SinLng + dz * SinLat
    Dh = Dh - da * LWa / Rn + df * Rn * Lat * Lat / Adb
    
    LatWGS84 = ((Lat + DLat) * 180) / math.PI
    LngWGS84 = ((Lng + DLng) * 180) / math.PI
    return LatWGS84,LngWGS84

def wgs84_to_belgian_datum(LatWGS84: float,LngWGS84:float) -> tuple:
    """
    Input parameters : Lat, Lng : latitude / longitude in decimal degrees and in WGS84 datum
    Output parameters : LatBel, LngBel : latitude / longitude in decimal degrees and in Belgian datum
    source: http://zoologie.umons.ac.be/tc/algorithms.aspx
    """
    Haut = 0    
    
    #conversion to radians
    Lat = (math.PI / 180) * LatWGS84
    Lng = (math.PI / 180) * LngWGS84
    
    SinLat = math.Sin(Lat)
    SinLng = math.Sin(Lng)
    CoSinLat = math.Cos(Lat)
    CoSinLng = math.Cos(Lng)
    
    dx = 125.8
    dy = -79.9
    dz = 100.5
    da = 251.0
    df = 0.000014192702
    
    LWf = 1 / 297
    LWa = 6378388
    LWb = (1 - LWf) * LWa
    LWe2 = (2 * LWf) - (LWf * LWf)
    Adb = 1 / (1 - LWf)
    
    Rn = LWa / math.Sqrt(1 - LWe2 * SinLat * SinLat)
    Rm = LWa * (1 - LWe2) / (1 - LWe2 * Lat * Lat) ^ 1.5
    
    DLat = -dx * SinLat * CoSinLng - dy * SinLat * SinLng + dz * CoSinLat
    DLat = DLat + da * (Rn * LWe2 * SinLat * CoSinLat) / LWa
    DLat = DLat + df * (Rm * Adb + Rn / Adb) * SinLat * CoSinLat
    DLat = DLat / (Rm + Haut)
    
    DLng = (-dx * SinLng + dy * CoSinLng) / ((Rn + Haut) * CoSinLat)
    Dh = dx * CoSinLat * CoSinLng + dy * CoSinLat * SinLng + dz * SinLat
    Dh = Dh - da * LWa / Rn + df * Rn * Lat * Lat / Adb
    
    LatBel = ((Lat + DLat) * 180) / math.PI
    LngBel = ((Lng + DLng) * 180) / math.PI
    return  LatBel,LngBel
