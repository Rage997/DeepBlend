import bpy
import torch
from PIL import Image as diocane
import numpy as np

# for blender2.80 we should derive the class from bpy.types.ShaderNodeCustomGroup
class StyleTransfer(bpy.types.CompositorNodeCustomGroup):

    bl_name='Style Transfer Neural Network'
    bl_label='StyleTransfer'

    # Setup the node - setup the node tree and add the group Input and Output nodes
    def init(self, context):
        self.node_tree=bpy.data.node_groups.new('.' + self.bl_name, 'ShaderNodeTree')
    
        self.node_tree.inputs.new("NodeSocketColor", "Image")
        self.node_tree.inputs.new("NodeSocketColor", "Image")
        self.node_tree.outputs.new("NodeSocketColor", "Image")
        self.node_tree.nodes.new('NodeGroupInput')
        self.node_tree.nodes.new('NodeGroupOutput') 
        print(self.node_tree.nodes['Group Input'].outputs[0])
        self.node_tree.links.new(self.node_tree.nodes['Group Input'].outputs[0],self.node_tree.nodes['Group Output'].inputs[0])
    
    def update(self):
        if self.inputs[0]:
            print("Input socket {} is linked".format(self.inputs[0].name))
            #The input node is given by going to the inputs then links and then get the socket
            tex_node = self.inputs[0].links[0].from_socket.node
            print(tex_node.type)
            img = tex_node.image
            print(img.channels)
            
            #Generate new img? 
            #bpy.data.images.new(name=img.name + "_deep_dream", width=100, height=100)
            pixels = list(img.pixels)
            print(pixels.shape)
        
    def copy(self, node):
        self.node_tree=node.node_tree.copy()

    def free(self):
        bpy.data.node_groups.remove(self.node_tree, do_unlink=True)
    