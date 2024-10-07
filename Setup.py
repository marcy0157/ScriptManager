from setuptools import setup, find_packages

setup(
    name="ScriptManager",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyQt5",  # Dipendenza necessaria per l'interfaccia grafica
    ],
    entry_points={
        'console_scripts': [
            'ScriptManager = ScriptManager.Start:main',
        ],
    },
    author="Marcello Maccagnola",
    author_email="marcello.maccagnola@gmail.com",
    description="Un tool manager multipiattaforma per eseguire script Python per la cybersecurity",
    license="Licenza d'Uso Personalizzata",
    url="https://github.com/marcy0157/ScriptManager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License"
        "Operating System :: OS Independent",
    ],
)
