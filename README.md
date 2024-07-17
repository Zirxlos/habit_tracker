# My habit tracking app

This habit tracking app is a project made while learning how to use OOP with python during my training at IU 
International Hochschule.

## What is it?

This app is used to help a user track good habits they want to implement.
They can create new habits inside the app and chose whether they want to complete them daily or weekly.
You have on the menu the choice between:
- Creating a new habit (you will be prompted for a name, a description and then chose if you want to perform
that task daily or weekly)
- getting feedback on your habits (getting the habit with the longest streak and 
the one with the shortest streak both for weekly and daily habits)
- or calling a list of all your habits and there you can filter it by periodicity or directly select one and decide if
you want to check it for today, delete it, get your current streak or get the longest streak ever

## Installation

```
pip install -r requirements.txt
```

## Usage

To start the program, run in the local directory

```
python main.py
```

and follow instructions on screen.

## Tests
The app comes with tests.
Please navigate to the project to run them and then run the following test script:

```
pytest .
```

Make sure all tests pass.

N.B: Make sure you have python 3.x installed