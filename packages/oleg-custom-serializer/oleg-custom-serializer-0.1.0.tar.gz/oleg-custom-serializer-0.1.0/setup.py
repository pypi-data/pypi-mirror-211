from setuptools import setup

setup (
    name="oleg-custom-serializer",
    version="0.1.0",
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
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    license="",
    author="Oleg-Dainovich",
    author_email="olegdainovich@gmail.com",
    description="",
)
