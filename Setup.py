from setuptools import setup, find_packages

# Funzione per leggere i requisiti dal file requirements.txt
def read_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()

setup(
    name="ScriptManager",
    version="1.0",
    packages=find_packages(),  # Cerca automaticamente i pacchetti nel progetto
    include_package_data=True,  # Include anche file non Python specificati in MANIFEST.in
    install_requires=read_requirements(),  # Legge e installa i requisiti da requirements.txt
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
