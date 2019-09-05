import bpy
import torch
from PIL import Image
import numpy as np
from . modelDeepDream import DeepDreamNN

# for blender2.80 we should derive the class from bpy.types.ShaderNodeCustomGroup
class DeepDream(bpy.types.CompositorNodeCustomGroup):

    bl_name='Deep Dream Neural Network'
    bl_label='DeepDream'
    # Setup the node - setup the node tree and add the group Input and Output nodes
    def init(self, context):
        self.node_tree=bpy.data.node_groups.new('.' + self.bl_name, 'ShaderNodeTree')
    
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
            img = tex_node.image
            img_path = img.filepath_from_user()
            #Generate new img? 
            #bpy.data.images.new(name=img.name + "_deep_dream", width=100, height=100)
            
            NN = DeepDreamNN(img_path)
            result_img = NN.dreamed_image
            # TODO how to load the resulting image into blender? SHould go pixel to pixel
            
            # Image.fromarray(np.array(pixels[:]))
            # img = diocane.fromarray(np.asarray(array),'RGB')
            # img.pixels[:] = pixels
            # img.update()
            # print('ok')
            
        
    def copy(self, node):
        self.node_tree=node.node_tree.copy()

    def free(self):
        bpy.data.node_groups.remove(self.node_tree, do_unlink=True)
        