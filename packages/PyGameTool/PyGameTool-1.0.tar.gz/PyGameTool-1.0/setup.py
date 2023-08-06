from distutils.core import setup
 
setup(
    name='PyGameTool',  # 对外模块的名字
    version='1.0',  # 版本号
    description='some game tools about pygame',  # 描述
    author='pbcat2022',  # 作者
    author_email='yuyao_100804@outlook.com',
    packages=['PyGameTool'],
    install_requires=['pygame'],#安装所需要的库
)