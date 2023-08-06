"""
linkeddatatools - a Python library for RDF graph structuring and exchange.
"""
#IMPORT PACKAGES
from lib2to3.pytree import Node
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

#IMPORT MODULES watch out for circular imports
import geomapi
from geomapi.pointcloudnode import PointCloudNode
from geomapi.node import Node
from geomapi.meshnode import MeshNode
from geomapi.imagenode import ImageNode
from geomapi.bimnode import BIMNode
from geomapi.sessionnode import SessionNode

import geomapi.utils as ut
import geomapi.geometryutils as gt

def e57xml_to_nodes(e57XmlPath :str, **kwargs) -> List[PointCloudNode]:
    """Parse XML file that is created with E57lib e57xmldump.exe

    Args:
        path (string):  e57 xml file path e.g. "D:\\Data\\2018-06 Werfopvolging Academiestraat Gent\\week 22\\PCD\\week 22 lidar_CC.xml"
            
    Returns:
        A list of pointcloudnodes with the xml metadata 
    """
    try:
        #E57 XML file structure
        #e57Root
        #   >data3D
        #       >vectorChild
        #           >pose
        #               >rotation
        #               >translation
        #           >cartesianBounds
        #           >guid
        #           >name
        #           >points recordCount
        #   >images2D
        mytree = ET.parse(e57XmlPath)
        root = mytree.getroot()  
        nodelist=[]   
        e57Path=e57XmlPath.replace('.xml','.e57')       

        for idx,e57node in enumerate(root.iter('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}vectorChild')):
            nodelist.append(PointCloudNode(e57XmlPath=e57XmlPath,e57Index=idx,e57Path=e57Path,**kwargs))
        return nodelist
    except:
        print('xmlPath not recognized. Please run .\e57xmldump on target e57 files and store output xml files somewhere in session folder. If formatting error occurs, manually remove <?xml version="1.0" encoding="UTF-8"?> from xml file.')
        return None


def img_xml_to_nodes(xmlPath :str, **kwargs) -> List[ImageNode]:
    """Parse XML file that is created with https://www.agisoft.com/

    Args:
        path (string):  e57 xml file path e.g. "D:\\Data\\2018-06 Werfopvolging Academiestraat Gent\\week 22\\PCD\\week 22 lidar_CC.xml"
            
    Returns:
        A list of pointcloudnodes with the xml metadata 
    """
    try:
        mytree = ET.parse(xmlPath)
        root = mytree.getroot()  
        nodelist=[]   
        for idx,item in enumerate(root.iter('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}vectorChild')):
            nodelist.append(ImageNode(xmlPath=xmlPath,xmlIndex=idx,**kwargs))
        return nodelist
    except:
        print('xml parsing error')
        return None

def e57header_to_nodes(e57Path:str, **kwargs) -> List[PointCloudNode]:
    """
    Parse e57 file header that is created with E57lib e57xmldump.exe

    Args:
        path (string):  e57 xml file path e.g. "D:\\Data\\2018-06 Werfopvolging Academiestraat Gent\\week 22\\PCD\\week 22 lidar_CC.xml"
            
    Returns:
        A list of pointcloudnodes with the xml metadata 
    """
    try:
        nodelist=[]   
        e57 = pye57.E57(e57Path)   
        for idx in range(e57.scan_count):
            nodelist.append(PointCloudNode(e57Path=e57Path,e57Index=idx, **kwargs))
        return nodelist
    except:
        print('e57header error')
        return None

# def mesh_to_node(path:str, sessionPath=None, sensor=None, accuracy=0.05) -> MeshNode:
#     """
#     Import mesh and extract all metadata parameters to create a MeshNode
#     Args:
#         path(str): path to the mesh    
#     Returns:
#         node (geomapi.meshnode.MeshNode)
#         None if mesh is empty
#     """
#     mesh=o3d.io.read_triangle_mesh(path)  
#     if len(mesh.vertices) != 0:
#         node=geomapi.meshnode.MeshNode()
#         node.sessionPath=sessionPath
#         node.timestamp=ut.get_timestamp(path) 
#         node.name=ut.get_filename(path)
#         node.path=path
#         node.sensor = sensor
#         node.accuracy=accuracy
#         node.mesh=mesh
#         node.set_metadata_from_mesh()
#         node.guid= '{'+str(uuid.uuid1())+'}'  
#         return node             
#     else: 
#         return None

def nodes_to_graph(nodelist : List[Node]) -> Graph:
    """ Convert list of nodes to a graph"""
    g=Graph()
    g=ut.bind_ontologies(g)
    for idx,node in enumerate(nodelist):
        try:
            node.to_graph()
            g+=node.graph
        except:
            print('Node '+str(idx)+' could not be serialized.')
            continue
    return g   

def subject_to_node_type(graph: Graph , subject:URIRef, **kwargs)-> Node:
    nodeType=ut.literal_to_string(graph.value(subject=subject,predicate=RDF.type))
    g = Graph()
    g += graph.triples((subject, None, None))
    if 'BIMNode' in nodeType:
        node=BIMNode(graph=g,**kwargs)
    elif 'MeshNode' in nodeType:
        node=MeshNode(graph=g,**kwargs)
    elif 'PointCloudNode' in nodeType:
        node=PointCloudNode(graph=g,**kwargs)
    elif 'ImageNode' in nodeType:
        node=ImageNode(graph=g,**kwargs)
    elif 'SessionNode' in nodeType:
        node=SessionNode(graph=g,**kwargs)  
    else:
        node=Node(graph=g,**kwargs) 
    return node

def get_linked_nodes(node: Node ,graph:Graph, getGeometry=False, **kwargs) -> List[Node]:
    """Get related nodes based on linkedNodes variable

    Returns:
        List[Node]: List of linked Nodes
    """
    nodelist=[]
    if getattr(node,'linkedNodes',None) is not None:  
        for subject in node.linkedNodes:
            if graph.value(subject=subject,predicate=RDF.type) is not None:
                nodelist.append(subject_to_node_type(graph=graph,subject=subject, getGeometry=getGeometry, **kwargs)) 
    return nodelist

def graph_to_nodes(graph : Graph,**kwargs) -> List[Node]:
    """Convert a graph to a set of Nodes

    Args:
        graph (RDFlib.Graph):  Graph to parse
        sessionPath (str): folder path of the graph 

    Returns:
        A list of pointcloudnodes, imagenodes, meshnodes, bimnodes, orthonodes with metadata 
    """
    nodelist=[]
    for subject in graph.subjects(RDF.type): #iterate over subjects
        #create correct nodeType
        node=subject_to_node_type(graph,subject,**kwargs)
        node.name = str(subject).replace('http://','') 
        node.graph = Graph()
        node.graph += graph.triples((subject, None, None))

        for predicate,object in graph.predicate_objects(subject):# iterate over all predicates of a subject
            attr=ut.predicate_to_attribute(predicate)
            
            #GEOMETRY
            if attr == 'cartesianBounds':
                node.cartesianBounds=ut.literal_to_cartesianBounds(graph.value(subject=subject,predicate=predicate)) 
            elif attr == 'orientedBounds':
                node.orientedBounds=ut.literal_to_orientedBounds(graph.value(subject=subject,predicate=predicate)) 
            elif attr == 'cartesianTransform':
                node.cartesianTransform=ut.literal_to_cartesianTransform(graph.value(subject=subject,predicate=predicate))
            elif attr == 'geospatialTransform':
                node.geospatialTransform=ut.literal_to_geospatialTransform(graph.value(subject=subject,predicate=predicate))
            #PATHS
            elif re.search('path', attr, re.IGNORECASE):
                path=ut.literal_to_string(graph.value(subject=subject,predicate=predicate))
                if path is not None:
                    if getattr(node,'sessionPath',None) is not None:
                        setattr(node,attr,(node.sessionPath+'\\'+path)) 
                    elif getattr(node,'graphPath',None) is not None:
                        setattr(node,attr,(node.graphPath+'\\'+path)) 
                    else:
                        setattr(node,attr,(os.getcwd()+'\\'+path)) 
            #INT    
            elif attr in ['recordCount','faceCount','label','e57Index']:
                setattr(node,attr,ut.literal_to_int(object)) 
            #FLOAT
            elif attr in ['xResolution','yResolution','imageWidth','imageHeight','focalLength35mm','principalPointU','principalPointV','accuracy']:
                setattr(node,attr,ut.literal_to_float(object)) 
            #ARRAYS
            elif attr in ['hasBIM','hasCAD','hasPcd','hasMesh','hasImg','hasOrtho','hasChild','hasParent','distortionCoeficients']:
                setattr(node,attr,ut.literal_to_list(object)) 
            #LISTS   
            elif attr in ['linkedNodes']:
                setattr(node,attr,ut.literal_to_uriref(object)) 
            #STRINGS
            else:
                setattr(node,attr,object.toPython()) # this solely covers string
        nodelist.append(node)
    return nodelist


def ifc_to_nodes(ifcPath:str, classes:str='ifcElement',**kwargs)-> List[BIMNode]:
    """
    Parse ifc file to a list of BIMNodes, one for each ifcElement

    Args:
        path (string):  ifc file path e.g. "D:\\Data\\2018-06 Werfopvolging Academiestraat Gent\\week 22\\PCD\\week 22 lidar_CC.xml"
        classes (string): ifcClasses seperated by | e.g. '.IfcWall | .IfcSlab'    
    Returns:
        A list of BIMNodes  
    """   
    try:
        nodelist=[]   
        ifc = ifcopenshell.open(ifcPath)   
        selector = Selector()
        for ifcElement in selector.parse(ifc, classes): 
            try:   
                node=BIMNode(ifcElement=ifcElement,ifcPath=ifcPath, **kwargs)
                if getattr(node,'mesh',None) is not None and len(node.mesh.triangles) !=0:
                    node.get_metadata_from_mesh()
            except:
                print('Node creation error')
                continue
            # if node.set_metadata_from_ifc_element(ifcElement):
            nodelist.append(node)
        return nodelist
    except:
        print('IfcOpenShell import error')
        return None
