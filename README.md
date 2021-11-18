# Python 项目加密部署及License生成和验证

---
#### 概要

旨在为基于python开发的各类工具、服务端的简单部署提供解决方案

**注：** 不适用于大型项目、商用部署

具有保护源码、防止复制、时间控制等功能，可以用于各种操作系统及基于docker的部署环境

- **保护代码：** 通过Cython编译为pyd或so文件
- **防止复制：** 获取和验证机器的唯一标识
- **时间控制：** 在License中加入失效时间

---
#### 使用

#### 环境

```shell
pip install pycryptodome Cython
```
**注：** Cython仅用于编译

#### 结构和功能

**./server** 秘钥管理
- assets : ui界面资源
- data : 储存生成的秘钥文件
- func.py : 生成秘钥和加密License
- gui.py : ui界面
- main.py : ui界面入口

使用时直接运行：
```shell
python main.py
```

**./client** 集成部署在客户端
- license_getter.py : 获取机器标识，生成License
- license_verifier.py : 验证License
- main.py : 调用示例

集成时，main.py中的调用过程必须编译，且对关键函数重命名或重写

**./build** 用于编译python源码，使用时先修改main.py中的待编译文件列表
```shell
python main.py build_ext --inplace
```

#### 集成示例

以一个简单的flask项目为例

在app.py中，定义app启动函数，在未检测到License文件时，调用get_license获取机器标识，在检测到有License时，调用is_license_valid判断License是否有效：

```python
from license_verifier import is_license_valid
from license_getter import get_license

def app_run():
    if not os.path.exists(lic_file):
        get_license(lic_file)
        print('License is generated')
        return
    if is_license_valid(lic_file=lic_file, aes_key_file=aes_key, rsa_key_file=rsa_key):
        app.run(host=host, port=port, threaded=True)
    else:
        print('License is invalid')
        return
```
**注：** 如前文，实际情况下先将关键函数重命名或重写，提高安全性

部署时，编译app.py, license_getter.py, license_verifier.py，设置manage.py作为启动入口

```python
from app import app_run

if __name__ == '__main__':
    app_run()
```

---
#### 具体实现
![Alt](https://github.com/sunchang272/python-license/blob/main/images/frame.png?raw=true)

原理非常简单，如上图所示


