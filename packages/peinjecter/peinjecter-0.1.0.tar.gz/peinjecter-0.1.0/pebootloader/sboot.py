import json
import pathlib
import shutil
import subprocess

from pebootloader.__log import log


def main():
    log.info('Second boot started')
    tempdir = pathlib.Path('.pebootloader').absolute()
    log.info('Temporary directory %s', tempdir)
    with open(tempdir.joinpath('config'), 'r') as file:
        config = json.load(file)
    log.info('Config %s', config)
    with open(tempdir.joinpath('self.txt'), 'r') as file: self = file.read()
    log.info('Copy target executable')
    shutil.copy(tempdir.joinpath('target'), self)
    resources = tempdir.joinpath('resources')
    if config['pointcut']['before'] is not None:
        log.info('Execute before pointcut')
        before_process = subprocess.Popen(config['pointcut']['before'], cwd=resources.as_posix(), shell=True)
        log.info('Execute result %s', before_process.wait())
    if config['pointcut']['around'] is not None:
        log.info('Execute around pointcut')
        subprocess.Popen(config['pointcut']['around'], cwd=resources.as_posix())
    log.info('Start target executable')
    process = subprocess.Popen(self, cwd=pathlib.Path(self).parent.as_posix())
    process.wait()
    if config['pointcut']['after'] is not None:
        log.info('Execute after pointcut')
        after_process = subprocess.Popen(config['pointcut']['after'], cwd=resources.as_posix())
        log.info('Execute result %s', after_process.wait())
    log.info('Revert self')
    shutil.copy(tempdir.joinpath('self'), self)
    log.info('Second boot ended')


if __name__ == '__main__':
    main()
