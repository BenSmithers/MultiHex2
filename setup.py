from distutils.core import setup
from setuptools import find_packages



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
    package_data["assets"]=[
        "MultiHex2/assets/buttons/*.svg",
        "MultiHex2/assets/buttons/*.png",
        "MultiHex2/assets/map_icons/*.svg",
        "MultiHex2/assets/map_icons/*.png",
        "MultiHex2/assets/mobiles/*.svg",
        "MultiHex2/assets/mobiles/*.png"
        "MultiHex2/assets/*.png",
        "MultiHex2/assets/*.svg"
    ]
    
    these_packages = find_packages()
    these_packages=["MultiHex2."+entry for entry in these_packages]

    setup(name="MultiHex2",
        version=1.0,
        description="Hex map making software",
        author="Ben Smithers",
        packages=find_packages(),
        package_data=package_data
    )

if __name__=='__main__':
    do_setup()