from setuptools import setup

setup(
    name="novapy",  # Il nome del tuo pacchetto
    version="0.1",  # La versione del tuo pacchetto
    py_modules=["__init__"],  # Lista dei moduli da includere nel pacchetto
    install_requires=[  # Dipendenze del tuo pacchetto
        "functools",
        "rich",
        "typing",
        "time"
    ],
)
