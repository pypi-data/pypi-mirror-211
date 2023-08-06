from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = "perfunctory"
LONG_DESCRIPTION = """Nope.
                    """

# Setting up
setup(
    name="perfunctory",
    version=VERSION,
    author="(Hank Singh)",
    author_email="<harpreetsingh1811@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy', 'pyttsx3', 'pyaudio', 'speedtest-cli', 'pynput', 'SpeechRecognition', 'geocoder', 'googlesearch-python', 'PyDictionary', 'psutil', 'calendar', 'wheel', 'twine' ],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)
