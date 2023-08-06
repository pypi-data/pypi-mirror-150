import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

docs_extras = [
    "Sphinx >= 3.0.0",  # Force RTD to use >= 3.0.0
    "docutils",
    "pylons-sphinx-themes >= 1.0.8",  # Ethical Ads
    "pylons_sphinx_latesturl",
    "repoze.sphinx.autointerface",
    "sphinxcontrib-autoprogram",
    "sphinx-copybutton",
    "sphinx-tabs",
    "sphinx-panels",
    "sphinx-rtd-theme",
    "pillow>=6.2.0",
]

setuptools.setup(
    name="zellij",
    version="0.0.5",
    author="Thomas Firmin",
    author_email="thomas.firmin@univ-lille.fr",
    description="A software framework for HyperParameters Optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CeCILL-C Free Software License Agreement (CECILL-C)",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "fractal",
        "continuous optimization",
        "global optimization",
        "black-box functions",
        "decision space partitioning",
        "exploration",
        "exploitation",
        "metaheuristics",
        "tree search",
    ],
    url="https://github.com/ThomasFirmin/zellij",
    project_urls={
        "Bug Tracker": "https://github.com/ThomasFirmin/zellij/issues",
    },
    package_dir={"": "lib"},
    packages=setuptools.find_packages("lib"),
    install_requires=[
        "numpy>=1.21.4",
        "DEAP>=1.3.1",
        "botorch>=0.6.3.1",
        "gpytorch>=1.6.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.2",
        "pandas>=1.3.4",
    ],
    extras_require={"mpi": ["mpi4py>=3.1.2"], "docs": docs_extras},
    python_requires=">=3.6",
)
