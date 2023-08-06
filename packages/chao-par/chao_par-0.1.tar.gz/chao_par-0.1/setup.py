from setuptools import setup, find_packages

setup(
    name="chao_par",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "torch",
        "torchvision",
        "opencv-python",
        "numpy",
        "tqdm",
        "Pillow",
        # 其他依赖项...
    ],
)

