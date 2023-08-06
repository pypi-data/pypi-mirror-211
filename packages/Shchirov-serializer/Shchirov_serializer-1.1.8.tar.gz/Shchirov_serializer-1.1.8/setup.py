from setuptools import setup


setup(
    name="Shchirov_serializer",
    version="1.1.8",
    description="python library for serialization",
    url="https://github.com/PaShampusik/PythonLabs/Lab_3",
    author="PaShampusik",
    author_email="shchirovpavel@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    install_requires = [
        'regex'
    ],
    packages=["serializers/json_serializer", "serializers/base",
              "serializers/xml_serializer", "serializers"],
    include_package_data=True
)
