#!/usr/bin/env python3
"""
Setup script para Iyari-ear
Permite instalar la aplicación como un paquete de Python
"""
from setuptools import setup, find_packages
from pathlib import Path

# Leer el README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Leer requirements
requirements = []
requirements_file = this_directory / "requirements.txt"
if requirements_file.exists():
    requirements = requirements_file.read_text().splitlines()
    # Filtrar comentarios y líneas vacías
    requirements = [r.strip() for r in requirements if r.strip() and not r.startswith('#')]

setup(
    name='iyari-ear',
    version='0.2.0',
    description='Subtítulos en tiempo real para que nadie se quede fuera de la conversación',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Blackmvmba88',
    author_email='',
    url='https://github.com/Blackmvmba88/Iyari-ear',
    license='MIT',
    packages=find_packages(exclude=['tests', 'tests.*']),
    py_modules=['image_tool', 'webui', 'main'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'iyari-ear=cli.iyari_ear_cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Accessibility',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    keywords='accessibility subtitles real-time speech-recognition transcription',
    project_urls={
        'Bug Reports': 'https://github.com/Blackmvmba88/Iyari-ear/issues',
        'Source': 'https://github.com/Blackmvmba88/Iyari-ear',
    },
    include_package_data=True,
    package_data={
        '': ['*.html', '*.css', '*.js', '*.json', '*.md', '*.txt'],
    },
)
