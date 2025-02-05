import yaml, time, subprocess
from string import Template
# Generate mappingtask.yaml according to template.yaml and config.yaml
config_raw = open("/slamhive/config.yaml",'r',encoding="UTF-8").read()
config_dict = yaml.load(config_raw, Loader=yaml.FullLoader)
algo_dict = config_dict["algorithm-parameters"]
datatset_dict = config_dict["dataset-parameters"]
all_dict = {}
if(algo_dict is not None):
    for key, value in algo_dict.items():
        all_dict.update({key: value})
if(datatset_dict is not None):
    for key, value in datatset_dict.items():
        all_dict.update({key: value})
template_raw = Template(open("/slamhive/template.yaml",'r',encoding="UTF-8").read())
# template = template_raw.safe_substitute(config_parsed)#Replaces existing dictionary values, preserving non-existing replacement symbols.
template = template_raw.substitute(all_dict)#An exception occurs when all parameter values required by the template are not provided.
# Write template to mappingtask.yaml
with open("/slamhive/mappingtask.yaml","w") as f:
    f.write(template)

# Read algorithm-remap from config.yaml for mono.launch
algo_remap_dict = config_dict["algorithm-remap"]
algo_remap_list = []
if(algo_remap_dict is not None):
    for key, value in algo_remap_dict.items():
        algo_remap_list.append(key + ":=" + value)
algo_remap = ' '.join(algo_remap_list)
roslaunch_command = "roslaunch aloam_velodyne aloam_velodyne_HDL_64.launch rviz:=false " + algo_remap

subprocess.run("bash -c 'source /opt/ros/kinetic/setup.bash;  \
                source /root/catkin_ws/devel/setup.bash; "
                + roslaunch_command 
                + " & sleep 10s ; \
                python3 /slamhive/dataset/rosbag_play.py; \
                rosnode kill -a ; \
                mv /root/catkin_ws/traj.txt /slamhive/result/traj.txt; \
                touch /slamhive/result/finished'", shell=True)


































































































































































