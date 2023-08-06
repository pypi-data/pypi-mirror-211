import io
import json
import pathlib
import zipfile

import configloaders

from pebootloader import encode
from .__boot import get_bytes as get_boot_bytes
from .__sboot import get_bytes as get_sboot_bytes


class Config:
    class pointcut:
        before: str | None = None
        around: str | None = None
        after: str | None = None


class PEInjecter:
    def __init__(self):
        self.config = configloaders.load({}, Config)
        self.boot_bytes = get_boot_bytes()
        self.sboot_bytes = get_sboot_bytes()
        self.resources_bytesio = io.BytesIO()
        self.resources_zip = zipfile.ZipFile(self.resources_bytesio, 'w')

    def add_resource(self, file: str | pathlib.Path, filename: str | pathlib.Path | None = None):
        file = pathlib.Path(file)
        if file.name == 'config.json':
            with open(file) as f: self.config = json.load(f)
        self.resources_zip.write(file, arcname=filename)

    def add_resources(self, file: str | pathlib.Path, dirname: str | pathlib.Path | None = None):
        file = pathlib.Path(file)
        files = []
        for f in file.glob('**/*'):
            files.append(f)
        for file in files:
            self.add_resource(file.relative_to(dirname))

    def header(self, config: dict | Config = {}, **kwargs) -> bytes:
        configloaders.load(self.config, config, {'pointcut': kwargs})
        self.resources_zip.close()
        self.resources_bytes = self.resources_bytesio.getvalue()
        self.config_bytes = json.dumps(self.config).encode('utf-8')
        return encode(self.boot_bytes, self.sboot_bytes[::-1], self.resources_bytes[::-1], self.config_bytes[::-1])

    def inject(self, target: str | io.TextIOWrapper, output: str | io.TextIOWrapper, config: dict | Config = {}, **kwargs) -> None:
        if isinstance(target, str): target = open(target, 'rb')
        if isinstance(output, str): output = open(output, 'wb')
        target_bytes = target.read()
        target.close()
        output.write(self.header(config, **kwargs) + encode(target_bytes.read()[::-1]))
        output.close()
