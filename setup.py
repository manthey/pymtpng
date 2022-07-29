from distutils.core import Extension, setup

mtpng_module = Extension(
    '_mtpng', sources=[], libraries=['mtpng'])

setup(
    name='pymtpng',
    version='0.1',
    description='mtpng wrapper',
    ext_modules=[mtpng_module],
    packages=['mtpng'],
)
