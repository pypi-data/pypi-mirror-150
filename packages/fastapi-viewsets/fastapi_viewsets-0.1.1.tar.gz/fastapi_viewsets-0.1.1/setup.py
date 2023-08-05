from setuptools import setup


setup(
    name='fastapi_viewsets',
    author='Alexander Valenchits',
    version='0.1.1',
    description="""Package for creating endpoint
     controller classes for models in the database""",
    url='http://example.com',
    install_requires=['fastapi>=0.76.0', 'uvicorn>=0.17.6', 'SQLAlchemy>=1.4.36'],
    packages=['fastapi_viewsets'],
    classifiers=[
            "Programming Language :: Python :: 3.9",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
	python_requires='>=3.6',
)