import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dmhe",  # 模快名称
    version="1.0",  # 当前版本
    author="Zhuangzhuang_He",  # 作者
    author_email="hyicheng223@gmail.com",  # 作者郎箱
    escription="一个为了减少代码重复的包",  # 模抉筒介
    long_description=long_description,  # 模快佯細介紹
    long_description_content_type="text/markdown",  # 模快洋細介紹格式
    packages=setuptools.find_packages(),  # 自劫找到項目中尋入的模快
    # 模快相美的元数据(更多描述信息)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依頼模快
    install_requires=[

    ],
    python_requires='>=3',
)
