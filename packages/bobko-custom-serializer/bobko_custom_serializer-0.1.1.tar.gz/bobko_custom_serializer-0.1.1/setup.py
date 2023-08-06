from setuptools import setup

setup (
    name="bobko_custom_serializer",
    version="0.1.1",
    packages=[
        "src",
        "src.encoder",
        "src.serializers"
    ],
    entry_points={
        "console_scripts": [
            "custom-serialize = src.custom_serializer:main"
        ]
    },
    url="",
    license="",
    author="Ilya_Bobko",
    author_email="ilya.deepak@yandex.ru",
    description="",
)
