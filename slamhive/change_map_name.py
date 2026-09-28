import os
import sys
import time


folder_path = "/root/catkin_ws/pcd/"  # 更改为你要监视的文件夹路径
# pointcloud_to_pcd 以时间戳命名，文件名最大的是最后一帧地图（listdir 的顺序是任意的）
files = [name for name in os.listdir(folder_path) if name.endswith(".pcd")] if os.path.isdir(folder_path) else []
if not files:
    print("[change_map_name] no pcd file in {}; no map was saved".format(folder_path))
    sys.exit(0)
os.rename(folder_path + max(files), "/root/catkin_ws/pcd/Map.pcd")
