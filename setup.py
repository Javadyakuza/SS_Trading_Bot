from setuptools import setup, find_packages

setup(
    name='SS_TRADING_BOT',
    version='0.1.0',
    description=' this project uses the "( ͡° ʖ̯ ͡°) Scalping vs Swing Trading" indicator by edward_Z represented in trading view to trade in kucoin CEX',
    author='javad yakuza',
    author_email='javadyakuzaa@gmail.com-_-javad.solidity.dev@gmail.com',
    url='https://github.com/Javadyakuza/SS_TRADING_BOT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='setuptools making-money ',
    python_requires='>=3.7,<4',
    install_requires=[
        'email_listener',
        'kucoin-futures-python'
    ],
    entry_points={
        'console_scripts': [
            'python/python3 src/signal_maker.py : runs a signal maker {see readMe.md "T_1"}',
            'python/python3 src/excutioner.py : runs the trader bot {see readMe.md} "T_2"',

        ],
    },
)
