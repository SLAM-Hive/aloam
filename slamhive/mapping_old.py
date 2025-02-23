import yaml, time, subprocess
from string import Template
# Generate mappingtask.yaml according to template.yaml and config.yaml
config_raw = open("/slamhive/config.yaml",'r',encoding="UTF-8").read()
config_dict = yaml.load(config_raw, Loader=yaml.FullLoader)

# Read algorithm-remap from config.yaml for mono.launch

algo_parameter_dict = config_dict["algorithm-parameters"]
algo_parameter_list = []
if(algo_parameter_dict is not None):
    for key, value in algo_parameter_dict.items():
        algo_parameter_list.append(key + ":=" + str(value))
algo_parameter = ' '.join(algo_parameter_list)

algo_remap_dict = config_dict["algorithm-remap"]
algo_remap_list = []
if(algo_remap_dict is not None):
    for key, value in algo_remap_dict.items():
        algo_remap_list.append(key + ":=" + str(value))
algo_remap = ' '.join(algo_remap_list)
roslaunch_command = "roslaunch /slamhive/aloam_velodyne_HDL_64.launch rviz:=false " + algo_parameter + " " + algo_remap

subprocess.run("bash -c 'source /opt/ros/kinetic/setup.bash;  \
                source /root/catkin_ws/devel/setup.bash; "
                + roslaunch_command 
                + " & sleep 10s ; \
                python3 /slamhive/dataset/rosbag_play.py; \
                rosnode kill -a ; \
                mv /root/catkin_ws/traj.txt /slamhive/result/traj.txt; \
                touch /slamhive/result/finished'", shell=True)
