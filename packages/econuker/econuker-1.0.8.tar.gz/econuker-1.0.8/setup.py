from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='econuker',
    version='1.0.8',
    author='YumYummity',
    author_email='034nop@gmail.com',
    description='API wrapper for https://api.econuker.xyz',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Specify the content type
    url='https://github.com/EcoNuker/EcoNuker-API-Python/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.9',
    install_requires=[
        'requests',
        'aiohttp'
    ],
)
