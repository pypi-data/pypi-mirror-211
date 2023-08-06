from setuptools import setup

setup(
    name='wlkatapython', # 自定义包名
    version='0.0.4', # 包的版本号
    description='WLKATA-Mirobot Multiple robotic arm control', # 描述信息
    long_description='This SDK is suitable for controlling single or multiple Mirabot robotic arms, which must be controlled through a multi-functional controller',
    author='dong shuo', # 作者
    py_modules=[
        'wlkatapython'
    ] # 包中包含的模块
)