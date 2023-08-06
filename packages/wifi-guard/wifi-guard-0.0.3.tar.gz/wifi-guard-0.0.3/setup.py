from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='wifi-guard',
    version='0.0.3',
    description='A simple WiFi Guard package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wifi-guard = wifi_guard.wifi_guard:run_wifi_guard'
        ]
    },
    python_requires='>=3.9',
    author='Lee Jongyoung',
    author_email='leejongyoung@icloud.com',
    url='https://github.com/wifi-guard/wifi-guard',
    license='MIT',
)
