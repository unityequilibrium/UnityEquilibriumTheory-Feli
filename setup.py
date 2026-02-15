from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="research-uet",
    version="0.9.0",
    author="Unity Equilibrium Theory Team",
    author_email="contact@unityequilibrium.io",
    description="A Unified Physics Simulation Framework (UET)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/unityequilibrium/UnityEquilibriumTheory",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Aritificial Intelligence",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    keywords=[
        "physics",
        "simulation",
        "unified-field-theory",
        "quantum-gravity",
        "dark-matter",
        "fluid-dynamics",
        "navier-stokes",
        "thermodynamics",
        "information-theory",
        "general-relativity",
        "uet",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "pandas>=1.3.0",
        "sympy>=1.8",
    ],
)
