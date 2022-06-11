from distutils.core import setup
from setuptools import find_packages

from glob import glob
import os

def do_setup():

    package_data = {}
    package_data[""] = [
        '*.md', 
        '*.rst', 
        'LICENSE*',
        '*.svg.',
        '*.png']
    package_data['tests']=[
        '*.py.',
        '*.sh'
    ]
    package_data["MultiHex2"]=[
        "assets/buttons/*.svg",
        "assets/buttons/*.png",
        "assets/map_icons/*.svg",
        "assets/map_icons/*.png",
        "assets/mobiles/*.svg",
        "assets/mobiles/*.png",
        "assets/*.png",
        "assets/*.svg"
    ]

    def get_in(folder):
        combined = os.path.join(os.path.dirname(__file__), "MultiHex2", folder)
        filtered = list(filter(lambda fname: ".svg" in fname or ".png" in fname, os.listdir(combined)))
        smoosh = [os.path.join("MultiHex2", folder, item) for item in filtered]
        return smoosh

    data_files = [
    ]

    folder = "assets"
    data_files.append((folder, get_in(folder)))
    data_files.append(("assets/buttons", get_in("assets/buttons")))
    data_files.append(("assets/map_icons", get_in("assets/map_icons")))
    data_files.append(("assets/mobiles", get_in("assets/mobiles")))
    print(data_files)

    these_packages = find_packages()
    these_packages=["MultiHex2."+entry for entry in these_packages]

    setup(name="MultiHex2",
        version=1.0,
        description="Hex map making software",
        author="Ben Smithers",
        packages=find_packages(),
        package_dir={'assets':'MultiHex2'},
        package_data=package_data,
    )

if __name__=='__main__':
    do_setup()