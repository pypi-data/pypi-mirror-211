from setuptools import setup

setup(
    name='pdfGeneratorpython',
    version='0.0.1',
    packages=['pdf_generator'],
    install_requires=[
        'pandas',
        'jinja2',
        'pdfkit',
        'PyPDF2'
    ],
)
