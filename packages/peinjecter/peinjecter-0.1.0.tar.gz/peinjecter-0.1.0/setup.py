# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pebootloader', 'peinjecter']

package_data = \
{'': ['*']}

install_requires = \
['configloaders>=2.2.2,<3.0.0', 'pyinstaller>=5.10.1,<6.0.0']

setup_kwargs = {
    'name': 'peinjecter',
    'version': '0.1.0',
    'description': 'PEInjecter is a Python library that allows you to inject any executable file into the call lifecycle of an exe. This can be useful for a variety of purposes, such as adding custom functionality to an existing program or modifying its behavior.',
    'long_description': "PE(可执行文件)注入器，可实现在目标PE文件运行之前、之间、之后运行其他的可执行文件或脚本\n\n启动流程\n\n```mermaid\ngraph LR;\n    boot --> sboot;\n    sboot --> target;\n```\n\n1. 在boot阶段，boot、sboot、resources、config、target等信息被解压，备份自身为self，并保存当前可执行文件的路径到self.txt中\n2. 在sboot阶段，读取config文件中记录的入口点信息，以及self.txt中记录的目标可执行程序的路径信息，执行注入逻辑并启动目标可执行程序\n\n直接破解\n\n```python\nimport peinjecter\n\nif __name__ == '__main__':\n    injecter = peinjecter.PEInjecter()\n    injecter.add_resource(r'.\\dist\\test.exe', 'test.exe')\n    injecter.inject('target.exe', 'output.exe', before='test.exe')\n```\n\n制作破解器\n\n```python\nimport argparse\nimport os\nimport pathlib\nimport sys\n\nimport peinjecter\n\nif __name__ == '__main__':\n    if getattr(sys, 'frozen', False):\n        root = pathlib.Path(getattr(sys, '_MEIPASS'))\n        parser = argparse.ArgumentParser()\n        parser.add_argument('target', nargs='?', default='cpuz_x64.exe')\n        args = parser.parse_args()\n\n        with open(args.target, 'rb') as file:\n            target_bytes = file.read()\n        with open(root.joinpath('injecter_header'), 'rb') as file:\n            header_bytes = file.read()\n        with open(args.target, 'wb') as file:\n            file.write(header_bytes + peinjecter.encode(target_bytes[::-1]))\n    else:\n        injecter_header = 'injecter_header'\n        injecter = peinjecter.PEInjecter()\n        injecter.add_resource(r'.\\dist\\test.exe', 'test.exe')\n        with open(injecter_header, 'wb') as file:\n            file.write(injecter.header(before='test.exe'))\n        os.system(f'pyinstaller -F -w --uac-admin {sys.argv[0]} --add-data {injecter_header};.')\n        os.remove(injecter_header)\n\n```",
    'author': 'jawide',
    'author_email': '596929059@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
