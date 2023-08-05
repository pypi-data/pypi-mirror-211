from setuptools import setup, find_packages
with open('README.md', 'r') as r_file:
    desc = r_file.read()

setup(
    name="Qmlview",
    version="3.2.1",
    packages=find_packages(),
    install_requires=['PyQt6-Qt6', 'PyQt6>=6.5.1'],
    entry_points={
            'console_scripts': ['qmlview = Qmlview.qmlview:main_run'],
    },

    author="Amoh - Gyebi Godwin Ampofo Michael",
    author_email="amohgyebigodwin@gmail.com",
    description="An alternative to qmlscene",
    long_description=desc,
    long_description_content_type="text/markdown",
    keywords="qmlview, qmlscene, ninja-preview, qml, pyqt, pyqt6, pyside, pyside6",
    url="https://github.com/amoh-godwin/Qmlview-wheel",
    project_urls={
        "Bug Tracker": "https://github.com/amoh-godwin/Qmlview-wheel/issues",
        "Documentation": "https://github.com/amoh-godwin/Qmlview-wheel/wiki",
        "Source Code": "https://github.com/amoh-godwin/Qmlview-wheel",
    },
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
