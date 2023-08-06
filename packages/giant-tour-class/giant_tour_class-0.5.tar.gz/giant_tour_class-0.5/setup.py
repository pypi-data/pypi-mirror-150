from setuptools import setup

# with open("README.md", "r") as fh:
#     long_description=fh.read()
setup(
    name="giant_tour_class",
    version="0.5",
    description="giant tour class",
    py_modules=["giant_tour_class"],
    package_dir={"": "src"},
    # classifiers=[
    #         "Programming Language :: Python :: 2.7",
    #         "License :: OSI Approved :: MIT License",
    # ],
    # long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["ortools", "kmedoids", "math", "numpy"],
    license="LICENSE.txt",
    author="Mr. Hanh",
)