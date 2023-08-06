import setuptools

# 读取项目的readme介绍
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zzd",# 项目名称，保证它的唯一性，不要跟已存在的包名冲突即可
    version="0.1.4",
    author="zzd lab", # 项目作者
    author_email="1965770446@qq.com",
    description="encode and scores", # 项目的一句话描述
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/miderxi/zzd",# 项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

