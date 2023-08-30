import bpy
from . import utils
import os
from bpy.props import EnumProperty, CollectionProperty
from.import props

class LoadObjs(bpy.types.Operator):
    bl_idname = "omniobject.loadobjs"
    bl_label = "Load All Objects"
    bl_options = {'REGISTER'}

    def divide_chunks(self, l, n):
        # looping till length l
        for i in range(0, len(l), n): 
            yield l[i:i + n]

    def __walk(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:
                file = os.path.join(root, file)
                if file.endswith('.obj'):
                    yield file

    @classmethod
    def poll(cls, context):
        try:
            return os.path.exists(context.scene.omniobject_props.dataPath) and os.path.isdir(context.scene.omniobject_props.dataPath)
        except: return False

    def execute(self, context):
        items=[("None", "None","")]
        for f in self.__walk(context.scene.omniobject_props.dataPath):
            data = os.path.abspath(f)
            name=os.path.relpath(data, context.scene.omniobject_props.dataPath)
            items.append((name, name[2:],""))
        props.setObjFileList(items,context)
        context.scene.omniobject_props.objFile="None"
        return {'FINISHED'}


    @classmethod
    def menu_func(cls, menu, context):
        menu.layout.operator(cls.bl_idname)

class AddObj(bpy.types.Operator):
    bl_idname = "omniobject.addobj"
    bl_label = "Add Objects To Scene"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            # Enable button only if in Object Mode
            selected = context.scene.omniobject_props.objFile
            path = os.path.join(context.scene.omniobject_props.dataPath, selected)
            return os.path.exists(path)
        except: return False


    def execute(self, context):
        selected = context.scene.omniobject_props.objFile
        path = os.path.join(context.scene.omniobject_props.dataPath, selected)
        print(path)
        if os.path.exists(path):
            bpy.ops.import_scene.obj(filepath=path)
            for obj in bpy.context.selected_objects:
                name = path.replace('\\','/').split('/')[-3]
                obj.name = name
                obj.data.name = name
        return {'FINISHED'}
    
    @classmethod
    def menu_func(cls, menu, context):
        menu.layout.operator(cls.bl_idname)


class SelectObj(bpy.types.Operator):

    obj_list : bpy.props.EnumProperty(items=props.getObjFileList)

    """Tooltip"""
    bl_idname = "omniobject.selectobj"
    bl_label = "Select Obj"
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = "obj_list"


    def execute(self, context):
        context.scene.omniobject_props.objFile = self.obj_list
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}