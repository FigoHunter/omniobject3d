import bpy
from bpy.props import ( BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty, StringProperty )
from bpy.types import ( PropertyGroup )
import pickle
import codecs


objList=[("None", "None","")]

def getObjFileList(scene, context):
    global objList
    if str(context.scene.omniobject_props.objListJson):
        objList=pickle.loads(codecs.decode(context.scene.omniobject_props.objListJson.encode(), "base64"))
    return objList

def setObjFileList(list, context):
    global objList
    objList = list
    context.scene.omniobject_props.objListJson=codecs.encode(pickle.dumps(objList), "base64").decode()


class OmniObjectProperties(PropertyGroup):

    objFile : EnumProperty(
        name = "",
        description = "Obj File",
        items = getObjFileList
    )

    dataPath : StringProperty(
        name = "",
        description = "Dataset Path",
        default = "",
        subtype = 'DIR_PATH'
        )
    
    objListJson:StringProperty(
        name = "",
        description = "Obj List",
        default = "",
    )
