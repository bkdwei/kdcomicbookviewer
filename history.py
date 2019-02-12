# coding: utf-8
# ~ 历史记录
import json
import os

json_path = os.environ["HOME"] + "/.config/kdcomicbookviewer/"
json_filename = "history.json"


def set_history(path, img_index):
    if os.path.exists(json_path) is not True:
        os.mkdir(json_path)
    history = {}
    history["img_path"] = path
    history["img_index"] = img_index
    history_file = open(json_path + json_filename, "w")
    jContent = json.dumps(history)
    history_file.write(jContent)
    history_file.close()
    print("保存历史记录成功")


def get_history():
    if os.path.exists(json_path) is not True:
        os.mkdir(json_path)
        print("目录不存在,新建目录" + json_path)

    print(os.path.exists(json_path + json_filename))
    if os.path.exists(json_path + json_filename):
        with open(json_path + json_filename, "r") as history_file:
            # ~ if history_file is not None :
            jContent = json.load(history_file)
            print(jContent)
            return jContent
    # ~ else:
        # ~ print("文件不存在,新建文件" + json_path + json_filename)
        # ~ history_file1 = open(json_path + json_filename, "w")
        # ~ history_file1.close()
