bl_info = {
    "name": "3d selection",
    "author": "JBlock",
    "version": (1, 0),
    "blender": (2, 83, 0),
    "location": "",
    "description": "Lets the user make a selection by choosing a shape around the 3d cursor and selecting within it",
    "warning": "this is in development so there may be bugs or cases where it might crash blender",
    "doc_url": "",
    "category": "3D View",
}

import bpy


class SphereSelect(bpy.types.Operator):
    """Sphere select"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.sphere_select"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Sphere select"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    
    radius: bpy.props.FloatProperty(name="radius", default=1,min = 1,max = 2)
    
    addToSelect: bpy.props.BoolProperty(name="add to selection", default=True)
    
    def execute(self, context):        # execute() is called when running the operator.
        radius = self.radius
        if self.addToSelect == False:
            bpy.ops.mesh.select_all(action='DESELECT')
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

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.
    

class BoxSelect(bpy.types.Operator):
    """Box select"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.box_select"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Box select"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    
    sizeX: bpy.props.FloatProperty(name="Scale x", default=2)
    sizeY: bpy.props.FloatProperty(name="Scale y", default=2)
    sizeZ: bpy.props.FloatProperty(name="Scale z", default=2)
    
    addToSelect: bpy.props.BoolProperty(name="add to selection", default=True)
    
    def execute(self, context):        # execute() is called when running the operator.
        size = (self.sizeX,self.sizeY,self.sizeZ)
        if self.addToSelect == False:
            bpy.ops.mesh.select_all(action='DESELECT')
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
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.


def BoxSelectMenu(self, context):
    self.layout.operator(BoxSelect.bl_idname)

def SphereSelectMenu(self, context):
    self.layout.operator(SphereSelect.bl_idname)

def register():
    bpy.utils.register_class(BoxSelect)
    bpy.utils.register_class(SphereSelect)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.prepend(BoxSelectMenu)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.prepend(SphereSelectMenu)
    

def unregister():
    bpy.utils.unregister_class(BoxSelect)
    bpy.utils.unregister_class(SphereSelect)
    
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(BoxSelectMenu)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(SphereSelectMenu)
    


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
