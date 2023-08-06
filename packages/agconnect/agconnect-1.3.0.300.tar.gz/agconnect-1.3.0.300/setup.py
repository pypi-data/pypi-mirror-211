from setuptools import setup, find_namespace_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='agconnect',
    version = '1.3.0.300',
    packages=find_namespace_packages(include=['agconnect.*'], exclude=[
        'agconnect.auth_server.test',
        'agconnect.common_server.test',
        'agconnect.cloud_function.test',
        'agconnect.database_server.test',
        'agconnect.cloud_storage.test']),
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls={
        'Documentation': 'https://github.com/AppGalleryConnect/agc-server-demos-python',
        'Source': 'https://pypi.org/project/agconnect',
        'Tracker': 'https://github.com/AppGalleryConnect/agc-server-demos-python/issues',
    },
)
