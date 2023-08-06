PE(可执行文件)注入器，可实现在目标PE文件运行之前、之间、之后运行其他的可执行文件或脚本

启动流程

```mermaid
graph LR;
    boot --> sboot;
    sboot --> target;
```

1. 在boot阶段，boot、sboot、resources、config、target等信息被解压，备份自身为self，并保存当前可执行文件的路径到self.txt中
2. 在sboot阶段，读取config文件中记录的入口点信息，以及self.txt中记录的目标可执行程序的路径信息，执行注入逻辑并启动目标可执行程序

直接破解

```python
import peinjecter

if __name__ == '__main__':
    injecter = peinjecter.PEInjecter()
    injecter.add_resource(r'.\dist\test.exe', 'test.exe')
    injecter.inject('target.exe', 'output.exe', before='test.exe')
```

制作破解器

```python
import argparse
import os
import pathlib
import sys

import peinjecter

if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        root = pathlib.Path(getattr(sys, '_MEIPASS'))
        parser = argparse.ArgumentParser()
        parser.add_argument('target', nargs='?', default='cpuz_x64.exe')
        args = parser.parse_args()

        with open(args.target, 'rb') as file:
            target_bytes = file.read()
        with open(root.joinpath('injecter_header'), 'rb') as file:
            header_bytes = file.read()
        with open(args.target, 'wb') as file:
            file.write(header_bytes + peinjecter.encode(target_bytes[::-1]))
    else:
        injecter_header = 'injecter_header'
        injecter = peinjecter.PEInjecter()
        injecter.add_resource(r'.\dist\test.exe', 'test.exe')
        with open(injecter_header, 'wb') as file:
            file.write(injecter.header(before='test.exe'))
        os.system(f'pyinstaller -F -w --uac-admin {sys.argv[0]} --add-data {injecter_header};.')
        os.remove(injecter_header)

```