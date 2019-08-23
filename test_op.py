import bpy
import torch

class TEST_OT_OPERATOR(bpy.types.Operator):
    bl_idname = "view3d.cursor_center"
    bl_label = "Simple Operator"
    bl_description = "Center 3D cursos"

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_center()
        return {'FINISHED'}