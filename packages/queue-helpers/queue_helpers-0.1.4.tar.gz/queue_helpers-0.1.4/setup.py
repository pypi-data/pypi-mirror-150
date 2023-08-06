from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.rst").read_text(encoding="utf-8")

setup(
    name="queue_helpers",
    version="0.1.4",
    description="A helper to manage Rabbit queues.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/ChamRun/queue_helpers",
    author="Gradient Data Processing",
    author_email="info@gradientdp.com",
    keywords="queue, pika, rabbit",
    packages=find_packages('src'),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=["pika"],
    project_urls={
        "Organization": "https://gradientdp.com/",
    },
)
