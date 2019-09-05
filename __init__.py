# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# TODOs 
# 1) Create basic (custom) node
# 2) Correctly load pytorch models 
# 3) Integrate a NN into node

bl_info = {
    "name" : "DeepBlend",
    "author" : "Rage",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy
from . test_op import TEST_OT_OPERATOR
from . test_panel import TEST_PT_PANEL
from . DeepDream import *
from . StyleTransfer import *
from nodeitems_utils import NodeItem, register_node_categories, unregister_node_categories
from nodeitems_builtins import CompositorNodeCategory

classes = (TEST_OT_OPERATOR, TEST_PT_PANEL)

register, unregister = bpy.utils.register_classes_factory(classes)

# Only DeepDream is being registered right now

def register():
    bpy.utils.register_class(DeepDream)
    newcatlist = [CompositorNodeCategory("SH_NEW_CUSTOM", "Custom Nodes", items=[NodeItem("DeepDream"),]),]
    register_node_categories("CUSTOM_NODES", newcatlist)

def unregister():
    unregister_node_categories("CUSTOM_NODES")
    bpy.utils.unregister_class(DeepDream)
