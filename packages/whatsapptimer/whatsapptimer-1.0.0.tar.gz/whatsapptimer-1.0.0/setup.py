from distutils.core import setup

import setuptools


VERSION = '1.0.0'
DESCRIPTION = 'Basic Whatsapp Scheduler'

# Setting up
setup(
    name="whatsapptimer",
    version=VERSION,
    author="aisgupta (Aishwarya Gupta)",
    author_email="<aisgupta06@gmail.com>",
    description=DESCRIPTION,
    packages=setuptools.find_packages(),
    install_requires=['pyautogui'],
    keywords=['python', 'whatsapp', 'message', 'scheduler', 'schedule', 'msg'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)
