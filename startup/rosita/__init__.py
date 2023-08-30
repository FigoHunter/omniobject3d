import bpy
from bpy.props import PointerProperty,CollectionProperty
import omniobject3d.ops
import omniobject3d.props
import omniobject3d.panels
from omniobject3d import utils

bpy.utils.register_class(omniobject3d.props.OmniObjectProperties)
bpy.types.Scene.omniobject_props = PointerProperty(type=omniobject3d.props.OmniObjectProperties)

bpy.utils.register_class(omniobject3d.panels.OmniObject_PT_LoadObjects)

bpy.utils.register_class(omniobject3d.ops.LoadObjs)
bpy.utils.register_class(omniobject3d.ops.AddObj)
bpy.utils.register_class(omniobject3d.ops.SelectObj)

def collhack(scene):
    bpy.app.handlers.depsgraph_update_pre.remove(collhack)
    if not str(scene.omniobject_props.dataPath):
        print("SetPath")
        scene.omniobject_props.dataPath = utils.DATASET_PATH
    print(str(scene.omniobject_props.dataPath))

bpy.app.handlers.depsgraph_update_pre.append(collhack)
