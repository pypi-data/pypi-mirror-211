from setuptools import setup

setup(
    name='hj-generate',
    version='3.1.0',
    author='hj',
    author_email='864655329@qq.com',
    description='代码生成',
    packages=['generate'],
    install_requires=['Jinja2'],
    entry_points={'console_scripts': ['hj-generate = generate.generate_code:main']},
    package_data={
        'generate': ['templates/*.tpl']
    }
)
