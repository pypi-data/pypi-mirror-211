import setuptools

# 读取README.md文件内容
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 列出所有依赖包的名称
dependencies = [
    'numpy',
    'pandas',
    'tqdm',
    'efficient_apriori==2.0.3',
    'prefixspan==0.5.2',
]

# 安装依赖包
setuptools.setup(
    name="BehaviorPattern",
    version="0.0.3",
    author="Chen Chen",
    author_email="cchen56@163.com",
    description="The tool is designed to mine behavior patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=dependencies,
)