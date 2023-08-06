from setuptools import find_packages, setup


with open("README.md") as f:
    long_description = f.read()

INSTALL_REQUIRES = [
    "fastapi==0.70.0",
    "numpy==1.21.3",
    "optuna==2.10.0",
    "pyarrow==6.0.0",
    "pydantic==1.8.2",
    "joblib==1.1.1",
    "pandas==1.3.4",
    "scikit-learn==1.0.1",
    "uvicorn==0.15.0",
    "xgboost==1.5.0",
    "google-cloud-aiplatform==1.25.0",
]

if __name__ == "__main__":
    setup(
        name="autovf",
        description="autovf: tuning xgboost with optuna",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Ali Cabukel",
        author_email="alicabukel@proton.me",
        url="https://github.com/alicabukel/autovf",
        license="Apache 2.0",
        package_dir={"": "src"},
        packages=find_packages("src"),
        entry_points={"console_scripts": ["autovf=autovf.cli.autovf:main"]},
        include_package_data=True,
        install_requires=INSTALL_REQUIRES,
        platforms=["linux", "unix"],
        python_requires=">=3.6",
    )
