import bpy

class TEST_PT_PANEL(bpy.types.Panel):
    bl_idname = "TEST_PT_PANEL"
    bl_label = "A panel"
    bl_category = "Test panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("view3d.cursor_center")
