import bpy
from . import props

class OmniObject_PT_LoadObjects(bpy.types.Panel):
    bl_label = "Load Obj Models"
    bl_category = "OmniObject"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"



    def draw(self, context):

        layout = self.layout

        layout.operator("omniobject.loadobjs", text="Reload Objects")
        layout.separator()
        layout.label(text="Select Objects:")

        row = layout.row(align=True)
        layout.operator("omniobject.selectobj",text=context.window_manager.omniobject_props.objFile)

        layout.operator("omniobject.addobj", text="Add")

