import bpy
from bpy.props import PointerProperty,CollectionProperty
import omniobject3d.ops
import omniobject3d.props
import omniobject3d.panels

bpy.utils.register_class(omniobject3d.props.OmniObjectProperties)
bpy.types.WindowManager.omniobject_props = PointerProperty(type=omniobject3d.props.OmniObjectProperties)
bpy.types.WindowManager.dropdown_collection = CollectionProperty(type=omniobject3d.props.OmniObjectProperties)


bpy.utils.register_class(omniobject3d.panels.OmniObject_PT_LoadObjects)

bpy.utils.register_class(omniobject3d.ops.LoadObjs)
bpy.utils.register_class(omniobject3d.ops.AddObj)
bpy.utils.register_class(omniobject3d.ops.SelectObj)
