# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='token_manager',
    version="5.0",
    description="Certificate manager for CryptoPro CSP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wolandius/token-manager",
    author="Vladlen Murylyov",
    author_email="vladlen.murylyov@red-soft.biz",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Users",
        "Topic :: CRYPTO PRO GUI",
        "License :: OSI Approved :: MIT",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="cryptopro, gui",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6, <4",
    install_requires=["PyGObject"],
    data_files=[
                    ("/etc/pam.d/", ["data/pam.d/cpconfig-amd64", "data/pam.d/cpconfig-ia32"]),
                    ("/etc/security/console.apps/", ["data/cpconfig-amd64", "data/cpconfig-ia32"]),
                    ("share/polkit-1/actions/", ["data/ru.red-soft.token-manager.policy"]),
                    ("share/token_manager/ui/", ["data/ui/style.css",
                                                 "data/ui/templates.glade",
                                                 "data/ui/token_manager.glade"
                                                 ]),
                    ("share/locale/en_US/LC_MESSAGES/", ["data/locale/en_US/LC_MESSAGES/token_manager.mo"]),
                    ("share/locale/ru/LC_MESSAGES/",    ["data/locale/ru/LC_MESSAGES/token_manager.mo"]),
                    ("share/applications/", ["data/token-manager.desktop"]),
                    ("share/applications/", ["data/token-manager-ia32.desktop"]),
                    ("share/icons/hicolor/16x16/apps/",   ["pics/16x16/token-manager.png"]),
                    ("share/icons/hicolor/24x24/apps/",   ["pics/24x24/token-manager.png"]),
                    ("share/icons/hicolor/32x32/apps/",   ["pics/32x32/token-manager.png"]),
                    ("share/icons/hicolor/48x48/apps/",   ["pics/48x48/token-manager.png"]),
                    ("share/icons/hicolor/64x64/apps/",   ["pics/64x64/token-manager.png"]),
                    ("share/icons/hicolor/128x128/apps/", ["pics/128x128/token-manager.png"])
                ],
    entry_points={
        "console_scripts": [
            "token-manager=token_manager:main",
        ],
    },
    project_urls={
        "Source": "https://github.com/wolandius/token-manager",
        "Bug Reports": "https://support.red-soft.ru/"
    },
)
