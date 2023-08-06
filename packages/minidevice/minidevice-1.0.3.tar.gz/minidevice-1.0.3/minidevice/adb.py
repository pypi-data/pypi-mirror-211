import subprocess

from .config import ADB_PATH


def get_sdk(device):
    """获取设备sdk版本

    Args:
        device (str): 设备id

    Returns:
        int: 设备sdk版本号
    """
    return int(
         subprocess.run(
         [ADB_PATH,"-s",device, "shell",'getprop', 'ro.build.version.sdk'],
         stdout=subprocess.PIPE, text=True
         ).stdout.strip())

def get_vmsize(device):
    """获取设备分辨率

    Args:
        device (str): 设备id

    Returns:
        str: 设备分辨率格式为 "宽x高"
    """
    return subprocess.run(
         [ADB_PATH, "-s", device, "shell", "wm", "size"],
         stdout=subprocess.PIPE, text=True
         ).stdout.split(":")[-1].strip()

def get_abi(device):
    """获取设备abi版本

    Args:
        device (str): 设备id

    Returns:
        str: 设备abi版本号
    """
    return subprocess.run(
         [ADB_PATH,"-s",device, "shell",'getprop', 'ro.product.cpu.abi'],
         stdout=subprocess.PIPE, text=True).stdout.strip()

def adb_screen(device):
        """adb 截图 
        - dx模式效率: 简单界面0.25s 复杂界面0.6s~0.8s 
        - vk模式效率: 简单界面0.3s 复杂界面0.5s~0.6s 
        """
        # 调用adb命令进行截图，并将输出传递给OpenCV进行处理
        process = subprocess.Popen([ADB_PATH,"-s",device, "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
        screenshot_data, _ = process.communicate()
        return screenshot_data

def adb_press(device,x,y,duration=150):
    subprocess.run([ADB_PATH,"-s",device, "shell", "input","touchscreen", "swipe",str(x),str(y),str(x),str(y),str(duration)])


def adb_silde(device,pointArray,duration=250):
    cmd = [ADB_PATH,"-s",device, "shell", "input","touchscreen", "swipe"]
    cmd.extend([str(coord) for point in pointArray for coord in point])
    cmd.append(str(duration))
    subprocess.run(cmd)

if __name__=="__main__":
    print(get_abi("127.0.0.1:5555"))