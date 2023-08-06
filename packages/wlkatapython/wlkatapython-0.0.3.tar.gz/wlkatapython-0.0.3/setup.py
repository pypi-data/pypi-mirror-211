from setuptools import setup

setup(
    name='wlkatapython', # 自定义包名
    version='0.0.3', # 包的版本号
    description='Mirobot机械臂控制'
                ' Mirobot六自由度机械臂 Python SDK 安装包 ------ Windows'
                'pip install wlkatapython', # 描述信息
    author='dong shuo', # 作者
    py_modules=[
        'wlkatapython'
    ] # 包中包含的模块
)