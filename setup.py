from setuptools import setup, Extension

_easyice_module = Extension(
    "_easyice",
    define_macros=[("TS_NO_PCSC", 1)],
    runtime_library_dirs=["sdk/lib"],
    include_dirs=["sdk/include"],
    library_dirs=["sdk/lib"],
    libraries=["easyice", "dvbpsi", "tr101290", "hlsanalysis"],
    language="cpp",
    extra_compile_args=["-std=gnu++17", "-fPIC"],
    sources=["_easyicemodule.cpp"],
)

setup(
    name="easyice",
    author="codetalks",
    author_email="banxi1988@gmail.com",
    version="0.1",
    description="libeasyice 工具包 包装库",
    py_modules=["easyice"],
    ext_modules=[_easyice_module],
    zip_safe=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
