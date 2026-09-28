import os
import time



def delete_files_except_largest(folder):
    # 获取文件夹下的所有文件
    files = os.listdir(folder)
    if not files:
        return
    
    # u字典序最大
    largest_file = max(files)
    
    # 删除除了最大文件之外的其他文件
    for file in files:
        if file != os.path.basename(largest_file):
            os.remove(os.path.join(folder, file))


if __name__ == "__main__":
    folder_path = "/root/catkin_ws/pcd"  # 更改为你要监视的文件夹路径
    check_interval = 1  # 检查间隔，单位为秒

    # mapping.py 在另一个后台进程里 mkdir，这里可能先启动；自己建好目录，否则会直接 FileNotFoundError 退出
    os.makedirs(folder_path, exist_ok=True)
    while True:
        delete_files_except_largest(folder_path)
        time.sleep(check_interval)
