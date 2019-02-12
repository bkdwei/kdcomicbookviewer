# coding: utf-8
# ~ 阅读模式
import json
import os

config_path =  os.environ["HOME"] + "/.config/kdcomicbookviewer/"
config_filename = "viewconfig.json"


def set_viewconfig(view_mode, scale_size):
    if os.path.exists(config_path) != True:
        os.mkdir(config_path)
    view_config = {}
    view_config["view_mode"] = view_mode
    view_config["scale_size"] = scale_size
    view_config_file = open(config_path + config_filename, "w")
    jContent = json.dumps(view_config)
    view_config_file.write(jContent)
    view_config_file.close()
    print("保存阅读模式成功")

def get_viewconfig():
    if os.path.exists(config_path) is not True:
        os.mkdir(config_path)
        print("目录不存在,新建目录" + config_path)

    print(os.path.exists(config_path + config_filename))
    if os.path.exists(config_path + config_filename):
        with open(config_path + config_filename, "r") as history_file:
            jContent = json.load(history_file)
            print(jContent)
            return jContent
    # ~ else:
        # ~ print("文件不存在,新建文件" + config_path + config_filename)
        # ~ history_file1 = open(config_path + config_filename, "w")
        # ~ history_file1.close()
