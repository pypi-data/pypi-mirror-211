import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    description = fh.read()

setuptools.setup(
    name="movies-download",
    version="0.0.2",
    author="碧海苍鹰",
    author_email="348249063@qq.com",
    packages=["movies_download"],
    description="视频下载助手",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/cgq/movies-download",
    license='MIT',
    python_requires='>=3.8',
    install_requires=[]
)
