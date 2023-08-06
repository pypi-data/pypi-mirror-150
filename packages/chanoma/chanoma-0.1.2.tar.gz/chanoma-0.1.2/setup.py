from setuptools import setup
from setuptools_rust import Binding, RustExtension

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="chanoma",
    version="0.1.2",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Rust",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
    ],
    packages=["chanoma"],
    rust_extensions=[RustExtension(
        "chanoma.chanoma", "Cargo.toml", debug=False, binding=Binding.PyO3)],
    include_package_data=True,
    zip_safe=False,
    url="https://github.com/booink/chanoma/tree/main/bindings/python3",
    description='chanoma is Characters Normalization library.文字列正規化処理用のライブラリです。',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Booink',
    author_email='booink.work@gmail.com',
    keywords=['japanese', 'normalize'],
)
