import inspect
import json
import os.path

from info import Information
from setting import CACHE_PATH, INTERFACE_PATH,DATA_STORAGE_TYPE, DATA_DATA_TYPE, DATA_LANGUAGE, DATA_TASK_TYPE

import os
import sys
from query import QueryDigit
import requests

def find_py(path):
    # 获取指定路径下的所有文件
    files = os.listdir(path)

    # 检查是否存在 __init__.py 文件，如果不存在则创建
    init_file = "__init__.py"
    if init_file not in files:
        with open(os.path.join(path, init_file), "w") as f:
            pass

    # 查找名为 "code.py" 的文件
    if "code.py" in files:
        return "code.py"

    # 判断是否只有一个py文件
    py_files = [file for file in files if file.endswith(".py")]
    if len(py_files) == 1:
        return py_files[0]


    return False


def check_config(config_path, qd):
    fp, fn = os.path.split(config_path)
    errors = []
    if fn!="config.json":
        errors.append("config文件名错误，必须为config.json")
        return errors


    cats = ['storage_type', 'data_type', 'language', 'task_type', ]
    cats_name = [DATA_STORAGE_TYPE, DATA_DATA_TYPE, DATA_LANGUAGE, DATA_TASK_TYPE]
    category = {c: cats_name[index] for index, c in enumerate(cats)}


    fields = ['name','url_or_path','storage_type','data_type','language','task_type','description','tags']

    fields_type = {
        'name':'str',
        'url_or_path':'str',
        'storage_type':'int',
        'data_type':'int',
        'language':'int',
        'task_type':'int',
        'description':'str',
        'tags':'list'
    }


    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)


    for field in fields:
        if field not in config:
            errors.append(f"{field}缺失")
            continue
        if type(config[field]) != fields_type[field]:
            errors.append(f"{field}字段值格式错误，应为{fields_type[field]}, 实际为{type(config[field])}")
            continue

        if field in fields[2:-2] :
            if config[field] not in category.get(field):
                errors.append(f"字段{field}的值为{config[field]},不在规定类型的数字代号范围中:{list(category.get(field).keys())}")

    return errors



class Data():

    def __init__(self):
        self.info = Information()
        self.qd = QueryDigit()


    def _get_data_id(self,data_id_or_name):
        # 检测是否已经缓存,
        qs = self.qd.get_resources(api_type="dataid", id=data_id_or_name)
        if not qs:
            print(f"data_id_or_name = {data_id_or_name}的资源不存在")
            return False
        data_id = qs[0].get('data_id')
        return data_id

    def load(self, data_id:str, imp_class="DigitData"):
        path = os.path.join(CACHE_PATH,data_id)
        if not  os.path.exists(path):
            print(f"路径不存在：{path}")
            return False

        code = find_py(path=path)
        if not code:
            print(f"未在该路径下找到代码文件")
            return False


        # 找到路径下的代码文件后
        # 动态加载
        # 添加路径，加载code.py文件，
        imp_class = imp_class
        sys.path.append(path)

        ip_module = __import__(f"{path}.code", fromlist=['code'])
        clss = inspect.getmembers(ip_module, inspect.isclass)
        # 判断DigitData类是否存在
        for cls in clss:
            if cls[0] == imp_class:
                if inspect.getmro(cls[1])[1].__name__ in ['TableData', 'LabelData', 'DocData', 'ImageData',
                                                          'AudioData',
                                                          'VideoData', 'GraphData']:
                    break
                else:
                    print("DigitData类不是规定类 TableData, LabelData, DocData, ImageData, AudioData, VideoData, GraphData 的子类")
                    return False
            else:
                print("DigitData类不存在")
                return False
        # 加载DIgitData类
        DD = getattr(ip_module, imp_class)  # 获取类
        return DD()  # 实例化类并返回



    def upload(self,md_instruction_path,config_path):
        """
        :param config_file:
        :param md_instruction_file:
        :param file_upload:
        :param kwargs:
        :return: data_id
        两种上传方式， 第一种文文件上传，第二种为字典格式上传
        """
        url  = f"{INTERFACE_PATH}/api/data/"
        headers = {'api-token':self.info.get_api_token()}


        errors = check_config(config_path=config_path, qd=self.qd)
        if errors:
            print(errors)
            return False


        files = {
            'cj': open(config_path, 'rb'),
            'md': open(md_instruction_path, 'rb')
        }
        response = requests.post(url=url, headers=headers, files=files)
        if response.status_code !=201:
            print(f"错误，错误代码为：{response.status_code}")

        content = response.json()

        if content['status']!=200:
            print(content.get('error'))
            return False

        print("上传成功")
        return content['data']








    def delete(self,data_id_or_name:str):

        data_id = self._get_data_id(data_id_or_name=data_id_or_name)
        if not data_id:
            return False

        url = INTERFACE_PATH + "/api/data/"
        headers = {'api-token':self.info.get_api_token()}
        response = requests.delete(url=url,headers=headers)
        if response.status_code != 204:
            print(f"删除时出现错误,错误代码{response.status_code}")
            return False
        content = response.json()

        if content.get("status") != 200:
            print(content.get('error'))
            return False

        print(content.get('msg'))
        return None # 成功删除

