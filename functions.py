import bpy
from bpy import context
import math

def BoxSelect(size = (1,1,1)):
    """
    Input
    -------
    size = tuple of size (x,y,z)
    
    Output
    -------
    select all vertices in range
    """
    box_size = [abs(size[0]),abs(size[1]),abs(size[2])]
    cursor3d = bpy.context.scene.cursor.location
        
    #list in dictionary all indexes and positions af all vertices
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = context.active_object
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="VERT")
    v = obj.data.vertices[0]
    co_final = obj.matrix_world @ v.co
    vertices = {}
    counter = 0
    for x in obj.data.vertices:
        v = obj.data.vertices[counter]
        counter += 1
        co_final = obj.matrix_world @ v.co
        vertices[x] = co_final
    
    
    #list all near vertices
    nv = []
    counter = 0
    for x in vertices:
        if abs(vertices[x][0] - cursor3d[0]) <= abs(box_size[0] / 2) and abs(vertices[x][1] - cursor3d[1]) <= abs(box_size[1] / 2) and abs(vertices[x][2] - cursor3d[2]) <= abs(box_size[2] / 2):
            nv.append(counter)
        counter += 1
    
    #select the vertices
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    for x in nv:
        obj.data.vertices[x].select = True
    bpy.ops.object.mode_set(mode = 'EDIT') 
    
     
def SphereSelect(radius = 1):
    """
    Input
    -------
    radius = radius of sphere
    
    Output
    -------
    select all vertices in range
    """
    box_size = [abs(radius*2),abs(radius*2),abs(radius*2)]
    cursor3d = bpy.context.scene.cursor.location
    #list in dictionary all indexes and positions af all vertices
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = context.active_object
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="VERT")
    v = obj.data.vertices[0]
    co_final = obj.matrix_world @ v.co
    vertices = {}
    counter = 0
    for x in obj.data.vertices:
        v = obj.data.vertices[counter]
        counter += 1
        co_final = obj.matrix_world @ v.co
        vertices[x] = co_final
    
    
    nv = []
    counter = 0
    for x in vertices:
        if (cursor3d - vertices[x]).length <= radius:
            nv.append(counter)
        counter += 1
    #select the vertices
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    for x in nv:
        obj.data.vertices[x].select = True
    bpy.ops.object.mode_set(mode = 'EDIT') 
    
    
    
#BoxSelect((2,2,2))
SphereSelect(1)