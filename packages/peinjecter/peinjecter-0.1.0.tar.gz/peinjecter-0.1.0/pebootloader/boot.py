import pathlib
import shutil
import subprocess
import sys
import zipfile

from pebootloader import decode
from pebootloader.__log import log


def main():
    log.info('Boot started')
    self = sys.executable
    tempdir = pathlib.Path('.pebootloader').absolute()
    log.info('Arguments %s %s', self, tempdir)
    shutil.rmtree(tempdir, True)
    if not tempdir.exists(): tempdir.mkdir()
    log.info('Copy self')
    shutil.copy(self, tempdir.joinpath('self'))
    for file_bytes, name in zip(decode(self), ['boot', 'sboot', 'resources.zip', 'config', 'target'][::-1]):
        if name != 'boot': file_bytes = file_bytes[::-1]
        with open(tempdir.joinpath(name), 'wb') as file:
            file.write(file_bytes)
            log.info('Extract file %s %d', tempdir.joinpath(name), len(file_bytes))
    with open(tempdir.joinpath('self.txt'), 'w') as file: file.write(self)
    log.info('Extract resources.zip')
    zfile = zipfile.ZipFile(tempdir.joinpath('resources.zip'), 'r')
    zfile.extractall(tempdir.joinpath('resources'))
    log.info('Start sboot')
    subprocess.Popen(tempdir.joinpath('sboot').as_posix(), creationflags=subprocess.DETACHED_PROCESS)
    log.info('Boot ended')


if __name__ == '__main__':
    main()
