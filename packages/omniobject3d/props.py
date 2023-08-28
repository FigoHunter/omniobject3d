from bpy.props import ( BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty, StringProperty )
from bpy.types import ( PropertyGroup )

objList=[("None", "None","")]

def getObjFileList(scene, context):
    return objList


class OmniObjectProperties(PropertyGroup):

    objFile : EnumProperty(
        name = "",
        description = "Obj File",
        items = getObjFileList
    )
