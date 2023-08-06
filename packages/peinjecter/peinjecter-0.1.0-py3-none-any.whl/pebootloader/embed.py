import glob
import inspect
import os
import pathlib
import shutil
import textwrap

from typing import Literal


def encode(*files, length: int = 8, byteorder: Literal["little", "big"] = 'little', signed: bool = False) -> bytes:
    all_bytes = b''
    for file in files:
        if not isinstance(file, bytes):
            with open(file, 'rb') as f:
                file = f.read()
        file_len = len(file)
        all_bytes += file + file_len.to_bytes(length, byteorder, signed=signed)
    return all_bytes


def decode(file, length: int = 8, byteorder: Literal["little", "big"] = 'little', signed: bool = False):
    if not isinstance(file, bytes):
        with open(file, 'rb') as f:
            file = f.read()
    offset = len(file)
    while offset > 0:
        file_len = int.from_bytes(file[offset - length:offset], byteorder, signed=signed)
        yield file[offset - file_len - length:offset - length]
        offset -= file_len + length


def main():
    module_path = pathlib.Path(inspect.getsourcefile(main)).parent
    os.chdir(module_path.parent)
    for executable in ['boot', 'sboot']:
        # shutil.rmtree(pathlib.Path(f'build/{executable}'), True)
        os.system(rf'pyinstaller -F -w --uac-admin pebootloader\{executable}.py')
        boot_path = glob.glob(module_path.parent.joinpath(f'dist/{executable}*').as_posix())[0]
        with open(boot_path, 'rb') as file:
            boot_bytes = file.read()
        with open(module_path.parent.joinpath('peinjecter').joinpath(f'__{executable}.py'), 'w') as file:
            file.write(textwrap.dedent('''
                def get_bytes():
                    return {}
            ''')[1:].format(boot_bytes))


if __name__ == '__main__':
    main()
