import setuptools

setuptools.setup(
    name="agile-py",
    version="0.0.2",
    author="Jia-Yau Shiau",
    author_email="jiayau_shiau@gmail.com",
    description="agile python project utilities",
    url="https://github.com/Janus-Shiau/agile-py",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "agpy=agile_py.cli.cli:cli",
        ]
    },
    include_package_data=True,
    package_data={
        "": [
            "settings/*.toml",
            "settings/*.yaml",
            "settings/*.json",
            "settings/gitignore",
            "settings/*.md" "scripts/*.sh",
        ],
    },
    python_requires=">=3.7",
    license="LICENSE",
    install_requires=["click", "rich", "black", "isort", "ruamel.yaml", "toml"],
)
