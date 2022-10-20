# Bosch-Motors-Dataset
This project is a sub-project of the research project **AgiProbot** from KIT and Bosch. We develop a 3D synthetic point cloud datasets. In this project, small electric motors are used as the key objects. This part explains how to generate the datasets, including motor mesh model dataset, point cloud dataset and noise point cloud dataset. We also build a synthetic **clamping** **system** with Blender to simulate the motor being clamped by the fixture in the real scenario.
## Software Preparation
* As our programming is based on the python language, we recommend a [Python>=3.7.0](https://www.python.org/) environment, including [Numpy](https://numpy.org/) and [Matplotlib](https://matplotlib.org/).
* We use [Blender 2.9](https://www.blender.org/) to generate the synthetic motor mesh model with the addon named motor factory. For specific details including how to install, you can see [Motor Factory](https://github.com/cold-soda-jay/blenderMotorFactoryVer2.0).

* We use another Blender addon named [Blensor](https://www.blensor.org/) to generate the point cloud dataset. Blensor is based on the Blender 2.79 version, may require additional libraries. (I used the third party released Blensor for mac)
### 1. Motor Mesh Model Dataset 
We generate 5 kinds of synthetic motor mesh (Type A0, A1, A2, B0, B1) with Blender addon in randomly different size ranges in each motor's parts. 
> Run the Blender (version 2.9 above is recommended), open Text Editor(hotkey: Shift + F11) and open the script named `synthetic_motor_generate.py`. You should specify the path to save in BASE_DIR and the number of total motors in main() function. (Tips: The input here is the total number of motors. Since 5 types of motors will be generated, please ensure that the input is an integer multiple of 5) Click "Run Script".


### 2. Point Cloud Dataset Generation
To generate the point cloud dataset, we are using [Blensor_1.0.18_RC_Mac](https://www.blensor.org/pages/downloads.html). Make sure it is installed correctly. Since I am using the Mac version of blensor, if you are using other systems, please pay attention to modifying the address format of the relevant python scripts. You can generate the whole point cloud dataset by running 'augmented_pc_generation.py'.
> Run the Blensor, open Text Editor and open the script named `augmented_pc_generation.py`. You should specify the motor_path (where the mesh models stored) and the save_path(where the generated numpy file stored) and click "Run Script".

In the script, there are some parameter which should be initialized, and its meaning are denoted as followd chart.
| cmd  | Description          | Type | Property |
| ------- | ----------------------------------------------------------| --- | ---------- |
| -i   | path of motor mesh model                                | string     | obligatory |
| -o   | path of save directory                                  | string     | obligatory |
| -clp | path of clamping system                                 | string     | obligatory |
| -cf   | cuboid file format, option: npy, pcd, both (default: npy)  | string | optional |
| -n    | number of total generation (an integer multiple of 5)     | integer | obligatory  |
| -mode    | which kind of dataset to be generated     | integer | obligatory  |

 * When we set mode as 1,there is no any augmentation integrated in the scene.
 * When we set mode as 2, the bandary of box will be randomly limited in specific range
 * When we set mode as 3, the motor components will be roteted in a limit range and other configuration is same with mode 2
 * When we set mode as 4, the tile will be covered over the motor

Here is a sample image for augmented point cloud of cuboid(.  
![](https://github.com/LinxiQIU/Motor_Datasets_Generation/blob/master/images/cuboid_img.jpg)
