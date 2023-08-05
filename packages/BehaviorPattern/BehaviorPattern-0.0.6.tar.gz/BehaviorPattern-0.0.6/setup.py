import setuptools
import pkg_resources

# 读取README.md文件内容
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# 列出所有依赖包的名称
dependencies = [
    'numpy',
    'pandas',
    'tqdm',
    'efficient_apriori==2.0.3',
    'prefixspan==0.5.2',
]

def get_missing_dependencies() -> list:
    """
    检查依赖项是否已经安装
    :return: 返回缺失的依赖项的列表
    """
    installed = {pkg.key for pkg in pkg_resources.working_set}
    return [dependency for dependency in dependencies if dependency not in installed]

# 如果存在未安装的依赖库，安装未安装的依赖库
missing = get_missing_dependencies()
if missing:
    setuptools.setup(
        name='BehaviorPattern',
        version='0.0.6',
        author='Chen Chen',
        author_email='cchen56@163.com',
        description='The tool is designed to mine behavior patterns',
        long_description=long_description,
        long_description_content_type='text/markdown',
        packages=setuptools.find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
        ],
        python_requires='>=3.6',
        install_requires=missing,
    )
else:
    setuptools.setup(
        name='BehaviorPattern',
        version='0.0.6',
        author='Chen Chen',
        author_email='cchen56@163.com',
        description='The tool is designed to mine behavior patterns',
        long_description=long_description,
        long_description_content_type='text/markdown',
        packages=setuptools.find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
        ],
        python_requires='>=3.6',
    )