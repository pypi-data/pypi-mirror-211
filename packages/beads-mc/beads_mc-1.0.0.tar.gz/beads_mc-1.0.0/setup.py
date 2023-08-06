from setuptools import setup, find_packages

setup(
    name='beads_mc',
    version='1.0.0',
    description='Bead-like Metropolis-Hastings algorithm for genetic/trait simulation',
    author='Smiruthi Ramasubramanian',
    author_email='smir.bayer@gmai.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'Pillow',
        'seaborn',
    ],
)