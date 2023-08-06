import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Mask anonymization framework",
    version="1.2.0",
    author="University of Manchester & ICES",
    author_email="nikola.milosevic86@gmail.com",
    description="Anonymization of clinical texts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nikolamilosevic86/mask",
    project_urls={
        "Bug Tracker": "https://github.com/nikolamilosevic86/mask/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    install_requires=[
        "tensorflow",
        "python-crfsuite==0.9.6",
        "tqdm==4.34.0",
"sphinx_rtd_theme==0.4.*",
"nltk>=3.4.5",
"numpy==1.17.0",
"scikit-learn==0.21.3",
"sklearn-crfsuite==0.3.6",
"Sphinx==1.8.5",
"tqdm==4.34.0",
"attrs==19.1.0",
"python-crfsuite==0.9.6",
"pytest==5.1.1",
"Keras==2.2.5"

    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
