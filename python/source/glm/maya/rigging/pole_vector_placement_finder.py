import maya.cmds as cmds
import maya.api.OpenMaya as om2

def create_pv_control(pos, name):
        #make an actual control in a group 
        loc = cmds.spaceLocator(name= name)
        #mVectors let you just do .x .y and .z instead of xform or a list where you have to do [0]
        cmds.move(pos.x, pos.y, pos.z, loc)
        
        return loc

def get_pole_vector_position(top_name, mid_name, end_name, top_joint_position, middle_joint_position, end_joint_position):
        
        #getting the position of each joint 
        top_joint_position = cmds.xform(top_name, query=True, translation=True, worldSpace=True)
        middle_joint_position = cmds.xform(mid_name, query=True, translation=True, worldSpace=True)
        end_joint_position = cmds.xform(end_name, query=True, translation=True, worldSpace=True)
        
        #create end MVector getting the x 0 y 1 and z 2 positions
        #creating a vector starts at origin and ends at the point of the joint, kinda like when you make an 
        #arrow and point constrain it.
        top_joint_vector = om2.MVector(top_joint_position[0],top_joint_position[1],top_joint_position[2])
        middle_joint_vector = om2.MVector(middle_joint_position[0],middle_joint_position[1],middle_joint_position[2])
        end_joint_vector = om2.MVector(end_joint_position[0],end_joint_position[1],end_joint_position[2])
        
        #revising the code to have a more appropriate placement
        line = (end_joint_vector - top_joint_vector)
        #this is a line from the top joint to the mid joint 
        point = (middle_joint_vector - top_joint_vector)
        
        
        #if using mVector if you multiply two vectors together itll do the .product automatically 
        #when getting the dot product you are getting the right angle of two angles https://www.mathsisfun.com/algebra/vectors-dot-product.html
        scale_value = (line * point) / (line * line)
        
        projected_vector = line * scale_value + top_joint_vector
        
        #getting length of arm to push the vector back far enough not to flip 
        root_to_mid_length = (middle_joint_vector - top_joint_vector).length()
        mid_to_end_length = (end_joint_vector - middle_joint_vector).length()
        
        total_length = root_to_mid_length + mid_to_end_length
        
        #normalizing the vector makes length equal one and multiplying by the length of the arm
        pole_vector_position = (middle_joint_vector - projected_vector).normal() * total_length + middle_joint_vector
        
     
        
        pv_control = create_pv_control(pole_vector_position, name= top_name + "_pv")
        
        return pv_control
        
def find_pole_vector_placement():
        ik_joint_chain = cmds.ls(sl=True)
        get_pole_vector_position(ik_joint_chain[0], ik_joint_chain[1], ik_joint_chain[2], ik_joint_chain[0],
                                 ik_joint_chain[1], ik_joint_chain[2])