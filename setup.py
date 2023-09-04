from setuptools import setup, find_packages

setup(
    name="wordsmyth",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "data": ["emojimap.json", "pytorch_model.bin", "vocabulary.json"],
    },
    data_files=[
        (
            "data",
            [
                "src/wordsmyth/data/emojimap.json",
                "src/wordsmyth/data/pytorch_model.bin",
                "src/wordsmyth/data/vocabulary.json",
            ],
        )
    ],
)
