import os
import sys
import atexit
from setuptools import setup, Extension
from setuptools.command.install import install

_easyice_module = Extension(
    "_easyice",
    define_macros=[("TS_NO_PCSC", 1)],
    runtime_library_dirs=["easyice_lib"],
    include_dirs=["sdk/include"],
    library_dirs=["sdk/lib"],
    libraries=["easyice", "dvbpsi", "tr101290", "hlsanalysis"],
    language="cpp",
    extra_compile_args=["-std=gnu++17", "-fPIC"],
    sources=["_easyicemodule.cpp"],
)

NAME = "easyice"


def find_module_dir():
    module_file_name = NAME + ".py"
    for p in sys.path:
        if os.path.isdir(p) and module_file_name in os.listdir(p):
            return p


# CustomInstall 参考
# https://stackoverflow.com/questions/20288711/post-install-script-with-python-setuptools
#
#
# {'distribution': <setuptools.dist.Distribution object at 0x7f17e6320ad0>, 'prefix': '/home/codetalks/.pyenv/versions/3.7.6', 'exec_prefix': '/home/codetalks/.pyenv/versions/3.7.6', 'home': None, 'user': 0, 'install_base': '/home/codetalks/.pyenv/versions/3.7.6', 'install_platbase': '/home/codetalks/.pyenv/versions/3.7.6', 'root': 'build/bdist.linux-x86_64/wheel', 'install_purelib': 'build/bdist.linux-x86_64/wheel/easyice-0.2.data/purelib', 'install_platlib': 'build/bdist.linux-x86_64/wheel/', 'install_headers': 'build/bdist.linux-x86_64/wheel/easyice-0.2.data/headers', 'install_lib': 'build/bdist.linux-x86_64/wheel/', 'install_scripts': 'build/bdist.linux-x86_64/wheel/easyice-0.2.data/scripts', 'install_data': 'build/bdist.linux-x86_64/wheel/easyice-0.2.data/data', 'install_userbase': '/home/codetalks/.local', 'install_usersite': '/home/codetalks/.local/lib/python3.7/site-packages', 'compile': False, 'optimize': None, 'extra_path': None, 'install_path_file': 1, 'force': None, 'skip_build': 0, 'warn_dir': False, 'build_base': 'build', 'build_lib': 'build/lib.linux-x86_64-3.7', 'record': None, 'old_and_unmanageable': None, 'single_version_externally_managed': True, '_dry_run': None, 'verbose': 1, 'help': 0, 'finalized': 1, 'config_vars': {'dist_name': 'easyice', 'dist_version': '0.2', 'dist_fullname': 'easyice-0.2', 'py_version': '3.7.6', 'py_version_short': '3.7', 'py_version_nodot': '37', 'sys_prefix': '/home/codetalks/.pyenv/versions/3.7.6', 'prefix': '/home/codetalks/.pyenv/versions/3.7.6', 'sys_exec_prefix': '/home/codetalks/.pyenv/versions/3.7.6', 'exec_prefix': '/home/codetalks/.pyenv/versions/3.7.6', 'abiflags': 'm', 'userbase': '/home/codetalks/.local', 'usersite': '/home/codetalks/.local/lib/python3.7/site-packages', 'base': '/home/codetalks/.pyenv/versions/3.7.6', 'platbase': '/home/codetalks/.pyenv/versions/3.7.6'}, 'path_file': None, 'extra_dirs': '', 'install_libbase': 'build/bdist.linux-x86_64/wheel/'}
class CustomInstall(install):
    def run(self):
        def _post_install():
            install_dir = find_module_dir()
            print("install dir:", install_dir)

            # Add your post install code here

        print(self.__dict__)
        atexit.register(_post_install)
        install.run(self)


setup(
    name="easyice",
    author="codetalks",
    author_email="banxi1988@gmail.com",
    version="0.2",
    description="libeasyice 工具包 包装库",
    py_modules=["easyice"],
    ext_modules=[_easyice_module],
    include_package_data=True,
    zip_safe=True,
    cmdclass={"install": CustomInstall},
    data_files=[
        (
            "easyice_lib",
            [
                "sdk/lib/libdvbpsi.so",
                "sdk/lib/libhlsanalysis.so",
                "sdk/lib/libtr101290.so",
                "sdk/lib/libeasyice.so",
            ],
        )
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
