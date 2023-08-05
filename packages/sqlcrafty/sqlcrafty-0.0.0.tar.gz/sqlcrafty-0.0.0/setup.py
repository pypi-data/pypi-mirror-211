from setuptools import setup

setup(
    name="sqlcrafty",
    version="0.0.0",
    description="Turning writing SQL into an art",
    author="Richard Garcia",
    packages=['sqlcrafty'],
    install_requires=[
        'bcrypt'
    ],
    entry_points={
        'console_scripts': [
            'sqlcrafty = sqlcrafty.sqlcrafty:main',
        ],
    },
)
