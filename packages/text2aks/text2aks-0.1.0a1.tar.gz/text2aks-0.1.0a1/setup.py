# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text2aks']

package_data = \
{'': ['*'], 'text2aks': ['fonts/vazir/*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0']

setup_kwargs = {
    'name': 'text2aks',
    'version': '0.1.0a1',
    'description': 'A simple python library to put text into an image.',
    'long_description': '![license](https://img.shields.io/github/license/imanhpr/text2aks?style=for-the-badge) ![enter image description here](https://img.shields.io/github/commit-activity/m/imanhpr/text2aks?style=for-the-badge)\n\n# Text2Aks\n**This project is under active development and anything can change in the future**\n___\n### What is text2aks ?\n**Text2Aks** is a simple library that can generate simple pictures with text input.\n___\n### Installing\nInstall and update using pip:\n\n```$ pip install text2aks```\n___\n### How dose it work ?\n***You have to have [Pillow](https://pillow.readthedocs.io/en/stable/) installed on your system.***\nIn the below example I will show you how can you genrate image with text2aks\n```python\nfrom text2aks import Text2Aks, Fonts\nfrom text2aks.elements import make_darker\nfrom PIL import Image\n\nmy_image = \'path to my image\'\ntext : str = "Nothing is more difficult, and therefore more precious, than to be able to decide"\nwrtier_of_text : str = \'Napoleon Bonaparte\'\n\nwith Image.open(my_image) as raw_image :\n    darker_image = make_darker(raw_image)\n    image_maker = Text2Aks(darker_image , Fonts.VAZIR_BOLD , font_size=50)\n    image_maker.genrate(text , wrtier_of_text , \'ltr\') # left ro right (ltr) | right to left (rtl)\n    result : Image.Image = image_maker.resault()\n    # If you want to save it in your file system you can use save method of Image class\n    # or if you want just takes a look at it you can use show method.\n    # result.save(\'name of new image , \'JPEG\')\n    # result.show()\n```\n![Result image](https://user-images.githubusercontent.com/56130647/168424164-0c3089cc-5793-4093-8675-a3315fdd9eea.jpg)\n![enter image description here](https://user-images.githubusercontent.com/56130647/168424324-95aa680b-40a6-4c67-b8f7-a7a6012d0201.jpg)\n\nYou can find all available fonts for this project in the ```fonts_data``` moduel\n***The only available font in this version of the project, is [Vazir](https://github.com/rastikerdar/vazirmatn) font. it\'s an open-source and free font that you can use it in your projects.***\n\nYou can use different weights of it in this project :\n```python\nfrom text2aks.fonts_data import  Fonts\n\nFonts.VAZIR_BLACK  # "Vazirmatn-Black.ttf"\nFonts.VAZIR_BOLD  # "Vazirmatn-Bold.ttf"\nFonts.VAZIR_EXTRABOLD  # "Vazirmatn-ExtraBold.ttf"\nFonts.VAZIR_EXTRALIGHT  # "Vazirmatn-ExtraLight.ttf"\nFonts.VAZIR_LIGHT  # "Vazirmatn-Light.ttf"\nFonts.VAZIR_MEDIUM  # "Vazirmatn-Medium.ttf"\nFonts.VAZIR_REGULAR  # "Vazirmatn-Regular.ttf"\nFonts.VAZIR_SEMIBOLD  # "Vazirmatn-SemiBold.ttf"\nFonts.VAZIR_THIN  # "Vazirmatn-Thin.ttf"\n\n```\n___\n## LICENSE\n```\nMIT License\n\nCopyright (c) 2022 Iman Hosseini Pour\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n```',
    'author': 'ImanHpr',
    'author_email': 'imanhpr1999@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/imanhpr/text2aks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
