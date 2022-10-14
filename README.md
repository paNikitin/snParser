# Social Network parser with captcha byPass
## _snParser_


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

snParser is a web-scraping software to parse info about VK users.

## Features

- Import a .txt file with user IDs and watch it automatically parse users` profile info
- Program outputs a .txt with user info

## Tech

snParser uses a bit of open source projects to work properly:

- [Selenium](https://github.com/SeleniumHQ/selenium) - Browser automation
- [numPy](https://github.com/numpy/numpy) - The fundamental package for scientific computing with Python
- [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI) - Simple Python GUI Builder.
- [BeautifulSoup4](https://github.com/wention/BeautifulSoup4) - Python library for pulling data out of HTML and XML files.
- [captcha-solver](https://pypi.org/project/captcha-solver/) - Library for captcha solving.

snParser is open source with a [public repository](https://github.com/paNikitin/snParser) on GitHub.

## Installation

snParser requires [Python](https://www.python.org/) v3+ to run.
To get started we need to install some libraries:

numPy to handle some arrays
```sh
pip install numpy
```
Selenium to get web pages` source
```sh
pip install selenium
```
captcha-solver to avoid login problems
```sh
pip install captcha-solver
```
BeautifulSoup4 to take info out of pages
```sh
pip install beautifulsoup4
```
PySimpleGUI to build our interface
```sh
pip install PySimpleGUI
```
Also, to make selenium work, we need to get Chrome browser and Chrome drivers of the same version as the browser itself. Latest drivers can be found [here](https://chromedriver.chromium.org/downloads).
## When everything is set
User needs to put user IDs to ```user_ids.txt``` (one on a single line) and a path to chromedriver to ```driver_path.txt```.
## Working with snParser
![alt text](https://i.imgur.com/rkWLwCd.png)

After all the data entered, you are welcome to scrape VK. Also there is a progress bar to track the progress of parsing. When the progress bar is full, user can check out screenshots of parser`s work as well as ```output.txt```

![alt text](https://i.imgur.com/KXAVzqo.png)
## License
MIT



