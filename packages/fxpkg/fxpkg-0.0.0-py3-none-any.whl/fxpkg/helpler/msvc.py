import json
import os
import xml.etree.ElementTree as ET
from fxpkg.internal import *

import typing
if typing.TYPE_CHECKING:
    from fxpkg.buildctx import BuildContext


__all__ = [
    'find_vswhere_path',
    'get_msvc_infos',
    'MSVCInfoProxy',
    'VCXProjParser',
    'MSVCPathHelpler'
]



def find_vswhere_path() -> Path:
    msvc_installer_path = Path() / os.environ['ProgramFiles(x86)'] / 'Microsoft Visual Studio/Installer'
    vswhere_path = msvc_installer_path/'vswhere.exe'    # use vswhere.exe to get msvc info
    if vswhere_path.exists():
        return vswhere_path
    else:
        raise FindFailException

async def get_msvc_infos(bctx:'BuildContext'):
    try:
        vswhere_path = find_vswhere_path()
        stdout, stderr = await bctx.run_cmd_async(f'{vswhere_path.quote} -format json -utf8', cwd=vswhere_path.prnt)
        msvc_infos: list = json.loads(stdout)
        return msvc_infos
    except json.JSONDecodeError or FindFailException as e:
        bctx.log.warning(e)
        return []
        

class MSVCInfoProxy:
    def __init__(self, msvc_info:dict):
        self.msvc_info = msvc_info

    def __getitem__(self, i):
        return self.msvc_info[i]
    
    @property
    def line_version(self) -> str:
        """example: 2019"""
        return self['catalog']['productLineVersion']

    @property
    def install_version(self) -> str:
        return self['installationVersion']

    @property
    def install_path(self) -> Path:
        return Path(self["installationPath"])

    @property
    def vcvars64(self) -> Path:
        return self.install_path/r'VC\Auxiliary\Build\vcvars64.bat'

    @property
    def vcvarsall(self) -> Path:
        return self.install_path/r'VC\Auxiliary\Build\vcvarsall.bat'


class VCXProjParser:
    def __init__(self, content:str):
        self.root = root = ET.fromstring(content)
        self.property_groups = pgs = {}
        self.property_groups:typing.Dict[str, ET.Element]
        for g in root.iter():
            tag = g.tag
            if tag.endswith('}PropertyGroup') or tag == 'PropertyGroup':
                k = g.get('Label')
                pgs[k] = g
    
    def has_label(self, label:str):
        return label in self.property_groups

    def get_platform_toolset(self, label:str):
        g = self.property_groups[label]
        for ele in g.iter():
            tag = ele.tag
            if tag.endswith('}PlatformToolset') or tag == 'PlatformToolset':
                text = ele.text
                return text


class MSVCPathHelpler:
    def __init__(self, bin_root:Path):
        self.bin_root = bin_root

    def get_lib_path(self, platform:str, arch:str, build_type:str, vc_toolset:str) -> Path:
        res_path = self._get_base_path(platform, arch, build_type, vc_toolset)
        return res_path/'static'
     

    def get_dll_path(self, platform:str, arch:str, build_type:str, vc_toolset:str) -> Path:
        res_path = self._get_base_path(platform, arch, build_type, vc_toolset)
        return res_path/'dynamic'


    def _get_base_path(self,platform:str, arch:str, build_type:str, vc_toolset:str) -> Path:
        res_path = self.bin_root
        if platform == 'windows':
            if arch == 'amd64':
                res_path = res_path/'x64'/build_type.capitalize()/vc_toolset
        return res_path

