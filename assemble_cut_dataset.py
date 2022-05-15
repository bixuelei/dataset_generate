import bpy 
import os 
import blensor
import math
import random
import csv
import numpy as np
#from sklearn.neighbors import NearestNeighbors


'''
new update in 18.01.2022:
    1. updata clamping sytem
    2. add random transformation to clympingsystem
    3. use square  randomly cover the scene
    4. randomly generate training data
'''


def Get_ObjectID(x) :    #get all kinds of ObjectID from numpy file

    dic = []
    for i in range(x.shape[0]):
        if x[i][8] not in dic:
            dic.append(x[i][8])

    return dic


def ChangeLabel(x):
    if x.shape[1] == 13 :
        for i in range(x.shape[0]):
            if x[i][8] == 808464432.0 :
                x[i][8] = int(0)
            elif x[i][8] == 825307441.0 :
                x[i][8] = int(1)
            elif x[i][8] == 842150450.0 :
                x[i][8] = int(2)
            elif x[i][8] == 875836468.0 :
                x[i][8] = int(3)
            elif x[i][8] == 892679477.0 :
                x[i][8] = int(4)
            elif x[i][8] == 909522486.0 :
                x[i][8] = int(5)
    else: 
        print("The cor of numpy is not right")
            
    return x



def Resort_IDX(x):     #reset the IDX Value in the filtered numpy
    
    for i in range(x.shape[0]) :
        x[i][-1] = i

    return x



def CutNumpy(x):     #drop the timestamp, yaw, pitch off and the point of (0,0,0)

    try :
        if x.shape[1] == 16 :
            x = x[:, 3:]
    except Exception as err :
        print(err)

    #Filter all points with a distance along the z coordinate small than 0
    y = x[x[:, 7] < 0]

    return y


def initial_clamp(Clamping_dir):
    add_plane()
    objects_name = []
    for obj in bpy.data.objects :
        objects_name.append(obj.name)
   
    if not '0000_Clamping' in objects_name :
        import_ClampingSystem_obj(Clamping_dir)

    if not '0000_SurPatch' in objects_name:
        add_tile()
        add_tile_another()
        

    



def import_MotorPart_obj(path, filters):

    need_file_items = []
    need_file_names = []

    filterDict = {}
    for item in filters:
        filterDict[item] = True

    file_lst = os.listdir(path)

    for item in file_lst: 
        fileName, fileExtension = os.path.splitext(item)
        if fileExtension == ".obj" and (not item in filterDict):
            need_file_items.append(item)

            need_file_names.append(fileName)

    n = len(need_file_items)
    for i in range(n):
        item = need_file_items[i]
        itemName = need_file_names[i]
        ufilename = path + "/" + item
        bpy.ops.import_scene.obj(filepath=ufilename, filter_glob="*.obj")
    
    rename_element('Motor')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = None
    resize_element('Motor')


def import_ClampingSystem_obj(path):     # for Blender 2.79-Version: need rename and conbination

    bpy.ops.import_scene.obj(filepath=path + '/clamp_counterpart.obj', filter_glob="*.obj")
    bpy.ops.import_scene.obj(filepath=path + '/foundation_slider.obj', filter_glob="*.obj")
    bpy.ops.import_scene.obj(filepath=path + '/operator_panel.obj', filter_glob="*.obj")
    bpy.ops.import_scene.obj(filepath=path + '/pillow.obj', filter_glob="*.obj")
    bpy.ops.import_scene.obj(filepath=path + '/plate.obj', filter_glob="*.obj")
    bpy.ops.import_scene.obj(filepath=path + '/plc_enclosure.obj', filter_glob="*.obj")
    bpy.ops.import_scene.obj(filepath=path + '/pneumatic.obj', filter_glob="*.obj")
    bpy.ops.import_scene.obj(filepath=path + '/slider.obj', filter_glob="*.obj")
    bpy.ops.import_scene.obj(filepath=path + '/Cylinder.obj', filter_glob="*.obj")
    rename_element('Clamping')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = None
    resize_element('Clamping')
    bpy.data.objects['0000_Clamping_Slider'].location=(0, 0.1, 0)

def rename_element(element_type ):      # element_type = ['Clamping', 'Motor']
    k = 0
    if element_type == 'Clamping' :
        for i in range(len(bpy.data.objects)):
            print(bpy.data.objects[i].name)
            if 'Cylinder' in bpy.data.objects[i].name:
                bpy.data.objects[i].name = '0000_Clamping_' + 'Cylinder'           
            if 'PLC' in bpy.data.objects[i].name:
                bpy.data.objects[i].name = '0000_Clamping_' + 'plc_enclosure'
            if 'Left_fixed' in bpy.data.objects[i].name:
                bpy.data.objects[i].name = '0000_Clamping_' + 'foundation_left_clamp'
            if 'Clamping_Right' in bpy.data.objects[i].name:
                bpy.data.objects[i].name = '0000_Clamping_' + 'countpart_right_clamp'
            if 'Slider_part' in bpy.data.objects[i].name:
                bpy.data.objects[i].name = '0000_Clamping_' + 'Slider'
            if 'Pneumatic_Assembly' in bpy.data.objects[i].name:
                bpy.data.objects[i].name = '0000_Clamping_' + 'Pneumatic'
            if 'Plate' in bpy.data.objects[i].name:
                bpy.data.objects[i].name = '0000_Clamping_' + 'plate'
            if 'operator_panel&duct' in bpy.data.objects[i].name:
                bpy.data.objects[i].name = '0000_Clamping_' + 'operator_panel'
            if 'MATRIX_Prototyp' in bpy.data.objects[i].name:
                bpy.data.objects[i].name = '0000_Clamping_' + 'pillar'

    

    elif element_type == 'Motor' :
        for i in range(len(bpy.data.objects)):
            if 'Bolt' in bpy.data.objects[i].name:
                bpy.data.objects[i].name = '6666_Bolt_' + str(k)
                k += 1
            elif 'Bottom' in  bpy.data.objects[i].name:
                bpy.data.objects[i].name = '5555_Bottom'
            elif 'Charge' in  bpy.data.objects[i].name:
                bpy.data.objects[i].name = '4444_Charge'
            elif 'Cover' in  bpy.data.objects[i].name:
                bpy.data.objects[i].name = '1111_Cover'
            elif 'Gear_Container' in  bpy.data.objects[i].name:
                bpy.data.objects[i].name = '2222_Gear_Container'



def intialize_lamp():

    bpy.ops.object.select_all(action='DESELECT')

    if bpy.data.objects['Point'] and bpy.data.objects['Point.001'] and bpy.data.objects['Point.002'] :
            
        bpy.data.objects['Point'].select = True
        bpy.context.scene.objects.active = bpy.data.objects['Point']
        bpy.context.object.data.energy = 0.8
        bpy.context.object.data.use_specular = False

        bpy.ops.object.select_all(action='DESELECT')

        bpy.data.objects['Point.001'].select = True
        bpy.context.scene.objects.active = bpy.data.objects['Point.001']
        bpy.context.object.data.energy = 0.8
        bpy.context.object.data.use_specular = False

        bpy.ops.object.select_all(action='DESELECT')

        bpy.data.objects['Point.002'].select = True
        bpy.context.scene.objects.active = bpy.data.objects['Point.002']
        bpy.context.object.data.energy = 0.8
        bpy.context.object.data.use_specular = False

        bpy.ops.object.select_all(action='DESELECT')

        
# Add a plane as the background
def add_plane():
    bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, location=(0, 0, 0), 
        layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.data.objects['Plane'].name = '0000_Plane'
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['0000_Plane'].select = True 
    bpy.context.scene.objects.active = bpy.data.objects['0000_Plane']
    bpy.ops.transform.resize(value=(3, 3, 3), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, 
            proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.transform.translate(value=(0, 0, 0), constraint_axis=(False, False, False),
            constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)   
    bpy.ops.object.select_all(action='DESELECT')



def create_csv(csv_path):
    if not os.path.exists(csv_path) :
        os.makedirs(csv_path)
    csv_path = csv_path + '/RandomInfor.csv'
    with open(csv_path, 'a+', newline = '') as f:
        csv_writer = csv.writer(f)
        head = ["x_camera", "y_camera", "z_camera", "euler1_camera", "euler2_camera", "euler3_camera"]
        csv_writer.writerow(head)


def read_bottomLength(csv_path):

    bottomLength = []
    with open(csv_path,"r+") as f:
        csv_read = csv.reader(f)
        for line in csv_read:
            if line[8] != 'mf_Bottom_Length':
                bottomLength.append(float(line[8])*0.05)
    return bottomLength

def read_subBottomLength(csv_path):

    subBottomLength = []
    with open(csv_path,"r+") as f:
        csv_read = csv.reader(f)
        for line in csv_read:
            if line[9] != 'mf_Sub_Bottom_Length':
                subBottomLength.append(float(line[9])*0.05)
    return subBottomLength


def random_CameraPosition(radius_camera, csv_path, save_RandomInfor):
    r = radius_camera
    theta = [0, 15.0*math.pi/180.0]           # 70`~90`
    phi = [0, 2*math.pi]

    phi_camera = random.uniform(phi[0], phi[1])
    theta_camera = random.uniform(theta[0], theta[1])
    x_camera = r*math.cos(phi_camera)*math.sin(theta_camera) 
    y_camera = r*math.sin(phi_camera)*math.sin(theta_camera) 
    z_camera = r*math.cos(theta_camera) 
    #bpy.data.objects['Camera'].location = (x_camera, y_camera, z_camera)

    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Camera'].select = True
    bpy.context.scene.objects.active = bpy.data.objects['Camera']

    beta_1 = math.atan2(abs(y_camera), abs(z_camera))
    beta_2 = math.asin(abs(x_camera) / (y_camera**2 + z_camera**2)**0.5)
    #beta_2 = math.asin(abs(x_camera) / (y_camera**2 + z_camera**2)**0.5)
    rotation_z = -1.57
    if 0 < phi_camera < math.pi/2.0 :
        rotation_x = -beta_2
        rotation_y = -beta_1
    if math.pi/2.0 < phi_camera < math.pi :
        rotation_x = beta_2
        rotation_y = -beta_1
    if math.pi < phi_camera < 3.0*math.pi/2.0 :
        rotation_x = beta_2
        rotation_y = beta_1
    if 3.0*math.pi/2.0 < phi_camera < 2.0*math.pi :  ###  ???
        rotation_x = -beta_2
        rotation_y = beta_1

    
    if phi_camera == 0.0 :
        rotation_x = theta_camera
        rotation_y = 0
    if phi_camera == math.pi/2.0 :
        rotation_x = 0
        rotation_y = theta_camera
    if phi_camera == math.pi :
        rotation_x = -theta_camera
        rotation_y = 0
    if phi_camera == 3.0*math.pi/2.0 :
        rotation_x = 0
        rotation_y = -theta_camera


    bpy.data.objects['Camera'].rotation_euler = (rotation_x, rotation_y, rotation_z)
    bpy.ops.object.select_all(action='DESELECT')
    #find a position above the motor
    x_camera +=(-0.915)
    y_camera +=0.3
    z_camera +=1.16
    bpy.data.objects['Camera'].location = (x_camera, y_camera, z_camera)
    cam_info = [str(x_camera), str(y_camera), str(z_camera), str(rotation_x), str(rotation_y), str(rotation_z)]
    return cam_info



def add_tile():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.surface.primitive_nurbs_surface_surface_add(radius=0.15, view_align=False, enter_editmode=False, 
            location=(0,0,0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.data.objects['SurfPatch'].name = '0000_SurfPatch'
    bpy.ops.object.select_all(action='DESELECT')

def add_tile_another():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.surface.primitive_nurbs_surface_surface_add(radius=0.08, view_align=False, enter_editmode=False, 
            location=(0,0,0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.data.objects['SurfPatch'].name = '0000_SurfPatch_another'
    bpy.ops.object.select_all(action='DESELECT')


def random_cover_position(Bottom_length,Motor_Type):
    if 'TypeA' in Motor_Type:
        tile_x = -0.8-Bottom_length+random.uniform(-0.2, 0.6)
        tile_y = 0.37+random.uniform(-0.2, 0.15)
        tile_x_2 = -0.8-Bottom_length+random.uniform(-0.2, 0.6)
        tile_y_2 = 0.37+random.uniform(-0.2, 0.15)
    else:
        tile_x = -0.60-Bottom_length+random.uniform(-0.2, 0.5)
        tile_x_2 = -0.60-Bottom_length+random.uniform(-0.2, 0.5)
        if tile_x>0.1:
            tile_y = 0.30+random.uniform(-0.2, 0.25)
        else:
            tile_y = 0.30+random.uniform(-0.45, 0.3)
        if tile_x_2>0.1:
            tile_y_2 = 0.30+random.uniform(-0.2, 0.25)
        else:
            tile_y_2 = 0.30+random.uniform(-0.45, 0.3)
    bpy.data.objects['0000_SurfPatch'].location = (tile_x, tile_y, 1.18)
    bpy.data.objects['0000_SurfPatch_another'].location = (tile_x_2, tile_y_2, 1.18)
    bpy.ops.object.select_all(action='DESELECT')
    return [str(tile_x), str(tile_y), '1.18']



def resize_element(element_type) :      # Resize ClampingSystem to 5 scale and Motor 0.05 scale

    factor_clamp=0.503
    factor_motor=0.05
    if element_type == 'Clamping' :
        for obj in bpy.data.objects:
            if '0000_Clamping_' in obj.name:
                bpy.ops.object.select_all(action='DESELECT')
                obj.select = True
                bpy.ops.transform.resize(value=(factor_clamp,factor_clamp,factor_clamp), constraint_axis=(False, False, False), 
            constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    elif element_type == 'Motor' :
        for obj in bpy.data.objects:
            if ('0000' not in obj.name) and ('Camera' not in obj.name) :
                bpy.ops.object.select_all(action='DESELECT')
                obj.select = True
                bpy.ops.transform.resize(value=(factor_motor,factor_motor,factor_motor), constraint_axis=(False, False, False), 
                    constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)




def Initial_motor_position(Motor_type,Bottom_length):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects :
        if ('0000' not in obj.name) and ('Camera' not in obj.name) :
            obj.select = True
            obj.location = (0, 0, 0)   
    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False),               # Ratotate all the Motor part 90` at Y axis
                    constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False),               # Ratotate all the Motor part 90` at x axis
                    constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.transform.rotate(value=3.14159, axis=(0, 0, 1), constraint_axis=(False, False, True), 
                    constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)                       
    
    if 'TypeB' in Motor_type:
        bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), 
                        constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.ops.transform.translate(value=(0,-0.03,-0.05), constraint_axis=(False, False, False),
                    constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    if 'TypeA2' in Motor_type:
        bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), 
                        constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.ops.transform.translate(value=(0,-0.03,-0.12), constraint_axis=(False, False, False),
                    constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    if 'TypeA1' in Motor_type:
        bpy.ops.transform.translate(value=(0,-0.03,-0.09), constraint_axis=(False, False, False),
                    constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    if 'TypeANone' in Motor_type:
        bpy.ops.transform.translate(value=(0,-0.03,-0.1), constraint_axis=(False, False, False),
                    constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.transform.translate(value=(-0.915+Bottom_length, 0.3, 1.16), constraint_axis=(False, False, False),
                    constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)


def random_Clymping_position():
    clySlider_location_x = random.uniform(-0.3, 0.3 )   
    clySlider_location_y =random.uniform(-0.2, 0.2)    
    clyfoundation_for_slider_y=clySlider_location_y+random.uniform(-0.1, 0.1 )
    clyfoundation_for_slider_z=random.uniform(-0.3, 0 )

    clycounter_for_slider_x = random.uniform(-0.2, 0.2)
    clycounter_for_slider_y = random.uniform(-0.05 ,0.3)
    clycounter_for_slider_z = random.uniform(-0.05,0)

    pillar_x=random.uniform(-0.2, 0 )
    pillar_y=random.uniform(-0.05, 0.15 )
    pillar_z=random.uniform(-0.1, 0.0 )

    cylinder_x = random.uniform(-0.05, 0.15)

    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['0000_Clamping_foundation_left_clamp'].location=(clySlider_location_x, clyfoundation_for_slider_y, clyfoundation_for_slider_z)
    bpy.data.objects['0000_Clamping_Slider'].location=(clySlider_location_x, clySlider_location_y, clyfoundation_for_slider_z)
    bpy.data.objects['0000_Clamping_countpart_right_clamp'].location=(clycounter_for_slider_x, clycounter_for_slider_y, clycounter_for_slider_z)
    bpy.data.objects['0000_Clamping_pillar'].location=(pillar_x, pillar_y, pillar_z)
    bpy.data.objects['0000_Clamping_Cylinder'].location = (cylinder_x, 0.06, 0)                      
    cly_info = [str(clySlider_location_x),str(clySlider_location_y),str(clyfoundation_for_slider_z) ]
    return cly_info


#############################cut the cuboids####################################
################################################################################
def get_Corordinate_inCam(cam_pos_x, cam_pos_y, cam_pos_z, alpha, beta, theta, cor):
    alpha = float(alpha)
    beta = float(beta)
    theta = float(theta)
    cor = np.array(cor).T
    cam_pos = np.array([float(cam_pos_x), float(cam_pos_y), float(cam_pos_z)]).T
    cor = cor - cam_pos

    c_mw = np.array([[math.cos(beta)*math.cos(theta), math.cos(beta)*math.sin(theta), -math.sin(beta)],
            [-math.cos(alpha)*math.sin(theta)+math.sin(alpha)*math.sin(beta)*math.cos(theta), math.cos(alpha)*math.cos(theta)+math.sin(alpha)*math.sin(beta)*math.sin(theta), math.sin(alpha)*math.cos(beta)],
            [math.sin(alpha)*math.sin(theta)+math.cos(alpha)*math.sin(beta)*math.cos(theta), -math.sin(alpha)*math.cos(theta)+math.cos(alpha)*math.sin(beta)*math.sin(theta), math.cos(alpha)*math.cos(beta)] ])
    
    cor_new = c_mw.dot(cor)
    return tuple(cor_new)


def get_panel(point_1, point_2, point_3):
    x1 = point_1[0]
    y1 = point_1[1]
    z1 = point_1[2]

    x2 = point_2[0]
    y2 = point_2[1]
    z2 = point_2[2] 

    x3 = point_3[0]
    y3 = point_3[1]
    z3 = point_3[2]
    
    a = (y2-y1)*(z3-z1) - (y3-y1)*(z2-z1)
    b = (z2-z1)*(x3-x1) - (z3-z1)*(x2-x1)
    c = (x2-x1)*(y3-y1) - (x3-x1)*(y2-y1)
    d = 0 - (a*x1 + b*y1 + c*z1)

    return (a, b, c, d)


def read_CameraPosition(csv_path):

    camera_position = []
    with open(csv_path,"r+") as f:
        csv_read = csv.reader(f)
        for line in csv_read:
            camera_position.append(line[:6])
   # camera_position = camera_position[1:]
    return camera_position



def set_Boundingbox(panel_list, point_cor):

    if panel_list['panel_up'][0]*point_cor[0] + panel_list['panel_up'][1]*point_cor[1] + panel_list['panel_up'][2]*point_cor[2] + panel_list['panel_up'][3] <= 0 :   # panel 1
        if panel_list['panel_bot'][0]*point_cor[0] + panel_list['panel_bot'][1]*point_cor[1] + panel_list['panel_bot'][2]*point_cor[2] + panel_list['panel_bot'][3] >= 0 : # panel 2
            if panel_list['panel_front'][0]*point_cor[0] + panel_list['panel_front'][1]*point_cor[1] + panel_list['panel_front'][2]*point_cor[2] + panel_list['panel_front'][3] <= 0 : # panel 3
                if panel_list['panel_behind'][0]*point_cor[0] + panel_list['panel_behind'][1]*point_cor[1] + panel_list['panel_behind'][2]*point_cor[2] + panel_list['panel_behind'][3] >= 0 : # panel 4
                    if panel_list['panel_right'][0]*point_cor[0] + panel_list['panel_right'][1]*point_cor[1] + panel_list['panel_right'][2]*point_cor[2] + panel_list['panel_right'][3] >= 0 : #panel 5
                        if panel_list['panel_left'][0]*point_cor[0] + panel_list['panel_left'][1]*point_cor[1] + panel_list['panel_left'][2]*point_cor[2] + panel_list['panel_left'][3] >= 0 : # panel 6

                            return True
    return False


def add_noise(patch_motor):
    ######### add uniform noise ############
    for point in patch_motor:
        noise_x = random.uniform(-0.001, 0.001)
        noise_y = random.uniform(-0.001, 0.001)
        noise_z = random.uniform(-0.005, 0.005)
        point[2] += noise_x
        point[3] += noise_y
        point[4] += noise_z
    
    ############ add downsample ############


    return patch_motor


def change_intoPointNet(wholescene,noise):
    if noise :
        cor = wholescene[:, 5:8]
    else:
        cor = wholescene[:, 2:5]
    color = wholescene[:, 9:12]
    lable = np.array([wholescene[:, 8]])
    new = np.concatenate((cor, color, lable.T), axis = 1)

    return new

 
def cut(data_to_cut,noise,camera_position_now):

    
 
    #cly_bottom = random.uniform(0.15,0.45)
    cly_bottom = 0.1
    Corners = [(-1.6, -0.2, 1.4),(-0.2, -0.2, 1.4),(-0.2, 0.65, 1.4),(-1.6, 0.65, 1.4),(-1.6, -0.2, cly_bottom),(-0.2, -0.2, cly_bottom),(-0.2, 0.65, cly_bottom),(-1.6, 0.65, cly_bottom)]


    cor_inCam = []
    for corner in Corners:
        cor_inCam_point = get_Corordinate_inCam(camera_position_now[0], camera_position_now[1], camera_position_now[2], camera_position_now[3], camera_position_now[4], camera_position_now[5], corner)
        cor_inCam.append(cor_inCam_point)
    panel_1 = get_panel(cor_inCam[0], cor_inCam[1], cor_inCam[2])
    panel_2 = get_panel(cor_inCam[5], cor_inCam[6], cor_inCam[4])
    panel_3 = get_panel(cor_inCam[0], cor_inCam[3], cor_inCam[4])
    panel_4 = get_panel(cor_inCam[1], cor_inCam[2], cor_inCam[5])
    panel_5 = get_panel(cor_inCam[0], cor_inCam[1], cor_inCam[4])
    panel_6 = get_panel(cor_inCam[2], cor_inCam[3], cor_inCam[6])
    panel_list = {'panel_up':panel_1, 'panel_bot':panel_2, 'panel_front':panel_3, 'panel_behind':panel_4, 'panel_right':panel_5, 'panel_left':panel_6}

    patch_motor = []
    for point in data_to_cut:
        if not noise:
            point_cor = (point[2], point[3], point[4])
        else:
            point_cor = (point[5], point[6], point[7])
        if set_Boundingbox(panel_list, point_cor):
            patch_motor.append(point)
    if(noise):
        patch_motor = add_noise(patch_motor)

    patch_motor = change_intoPointNet(np.array(patch_motor),noise=noise)  # resort the file information N*13 -> N*7
    
    return patch_motor
    #########################################################
    ##########################################################

def scan_cut(save_dir, Motor_type, scanner, sequence_Motor,cam_info):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.camera = bpy.data.objects['Camera']
    bpy.data.objects['Camera'].select = True
    bpy.context.scene.objects.active = bpy.data.objects['Camera']

    sigma = random.uniform(0.0, 0.005)

    saved_file_path = save_dir + '/' + 'Training_' + Motor_type + '_' + sequence_Motor + '.pcd'
    # blensor.tof.scan_advanced(scanner, tof_res_x=1280,tof_res_y=960,evd_file= saved_file_path,noise_sigma=sigma)
    # # the blensor API will generate 3 types of file,we need to remove unneeded ones and remame some of them named by API
    # os.remove(save_dir + '\\' + 'scan_' + Motor_type + '_' + sequence_Motor)
    # os.rename(save_dir + '\\' + 'scan_' + Motor_type + '_' + sequence_Motor + '00000' + '.pcd', save_dir + '\\' + 'scan_' + Motor_type + '_' + sequence_Motor + '.pcd')
    # os.rename(save_dir + '\\' + 'scan_' + Motor_type + '_' + sequence_Motor + '_noisy00000' + '.pcd', save_dir + '\\' + 'scan_' + Motor_type + '_' + sequence_Motor + '_noisy' + '.pcd')


    saved_numpy_path = save_dir + '/' + 'Training_' + Motor_type + '_' + sequence_Motor + '_noise.numpy'
    blensor.tof.scan_advanced(scanner,tof_res_x=1280,tof_res_y=960, evd_file= saved_numpy_path,noise_sigma=sigma)
    numpy_name = 'Training_' + Motor_type + '_' + sequence_Motor+'augmentation3' 
    motorNumpy_file = save_dir + '/' + 'Training_' + Motor_type + '_' + sequence_Motor + '_noise00000' + '.numpy'

    #########  transform the numpy file  #############
    motor_numpy = np.loadtxt(motorNumpy_file)
    filtered = CutNumpy(motor_numpy)
    filtered = ChangeLabel(filtered)
    filtered = Resort_IDX(filtered)
    filtered = cut(data_to_cut=filtered,noise=True,camera_position_now=cam_info)
    np.save(save_dir + '/' + numpy_name , filtered)
    os.remove(motorNumpy_file)

    bpy.ops.object.select_all(action='DESELECT')


def delete_allElement(): 
    '''
        Delete all elements except Camera, lamp and clympingsystem
    '''
    filter_keep = ['Camera','0000_Clamping_plc_enclosure','0000_Clamping_foundation_left_clamp','0000_Clamping_countpart_right_clamp' ,
                            '0000_Clamping_Slider','0000_Clamping_Pneumatic','0000_Clamping_plate',
                            '0000_Clamping_operator_panel','0000_Clamping_pillar','0000_Clamping_Cylinder' , '0000_Plane', '0000_SurfPatch','0000_SurfPatch_another']
    for obj in bpy.data.objects :
        if not obj.name in filter_keep :
            bpy.data.objects.remove(obj)

def random_list(num_motors):
    num_motors=num_motors
    num_noise=int(0.6*num_motors)
    num_original=int(0.2*num_motors)
    list=[]
    for i in range(num_motors):
        list.append(i+1)
    list_noise=random.sample(list,num_noise)
    list_rest=[]
    for m in list:
        if m not in list_noise:
            list_rest.append(m)
    list_original=random.sample(list_rest,num_original)
    list_nonoice=[]
    for m in list_rest:
        if m not in list_original:
            list_nonoice.append(m)
    validation_list=[]
    validation_list.append(random.sample(list_noise,math.floor(0.12*num_motors)))
    validation_list.append(random.sample(list_nonoice,math.floor(0.04*num_motors)))
    validation_list.append(random.sample(list_original,math.floor(0.04*num_motors)))
    return list_noise,list_original,list_nonoice,validation_list


def main():
    ###################################################
    ######           parameter to set        ##########
    ###################################################


    ##########      the obj not to load     ############
    filters = ["Motor.obj"]    


    ##########      the route to load motor     ###############################################################################                          
    file_path = "/Users/bixuelei/Master/Center_position/TypeA2"
    root, Motor_type = os.path.split(file_path)


    ##########      the route to load clamp     ###################################################################################
    Clamping_dir = "/Users/bixuelei/Master/Clamp_system_decorated"

    ########### route to save file#####################
    save_path = "/Users/bixuelei/Master/Result/Training/" + Motor_type

    ##############  directories to load motor##############
    List_motor = os.listdir(file_path)     # Path List for .obj file
    if 'data.csv' in List_motor :
        List_motor.remove('data.csv')
    if '.DS_Store' in List_motor :
        List_motor.remove('.DS_Store')
    List_motor.sort()
    
    

    #####################   import and inital all needed components     ###########
    initial_clamp(Clamping_dir)   


    ###################       get the needed data from data.csv     ############
    sub_BottomLength_all = read_subBottomLength(file_path + '/data.csv')
    BottomLength_all = read_bottomLength(file_path + '/data.csv')

    #list_noise,list_original,list_nonoise=random_list(len(List_motor))

    ###################################################
    #   scan all the files from the holder            #
    ###################################################   
    create_csv(save_path)
    
    for dirs in List_motor :
        delete_allElement()
        Motor_path = file_path + '/' + dirs
        save_dir = save_path
        k = dirs.split('_')
        sub_BottomLength = sub_BottomLength_all[int(k[1])-1]
        BottomLength = BottomLength_all[int(k[1])-1]

        cover_position = random_cover_position(Bottom_length=sub_BottomLength+BottomLength,Motor_Type=Motor_type)

        import_MotorPart_obj(Motor_path, filters)

        Initial_motor_position(Motor_type,sub_BottomLength+BottomLength)
        random_cam_info = random_CameraPosition(radius_camera = random.uniform(2.8, 3.2), csv_path = save_path, save_RandomInfor=True)
        random_cly_info=[]
        random_cly_info = random_Clymping_position()

        # ####### save the random info######################
        #all_info=random_cam_info
        # for pos in random_cly_info:
        #     all_info.append(pos)
        # for pos in cover_position: 
        #     all_info.append(pos)
        # csv_path = save_path + '/RandomInfor.csv'
        # with open(csv_path, 'a+', newline = '') as f:
        #     csv_writer = csv.writer(f)
        #     csv_writer.writerow(random_cam_info)
        #######################################################

        if not os.path.exists(save_dir) :
            os.makedirs(save_dir)
        scan_cut(save_dir = save_dir, Motor_type = Motor_type, scanner = bpy.data.objects['Camera'], sequence_Motor = k[1],cam_info=random_cam_info)
        break
        





if __name__ == '__main__':
    main()