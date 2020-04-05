This is the *degrees* project for [Week 0 : Search]() of the [CS50's Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/).

Video lesson can be found [here](https://cs50.harvard.edu/ai/weeks/0/).
Project page is [here](https://cs50.harvard.edu/ai/projects/0/degrees/).

According to the [Six Degrees of Kevin Bacon game](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon), anyone in the Hollywood film industry can be connected to Kevin Bacon within six steps, where each step consists of finding a film that two actors both starred in.

# Usage
Clone this repo or download the content of this folder, and run the following command in your terminal : 
```
python degrees.py large
```
This will run the program on the *large* dataset. For smaller test, run `python degrees.py small`.

# Example
```
> python3 degrees.py large
Loading data...
Data loaded.
Name: Tom Hanks
Name: Tom Cruise
2 degrees of separation.
1: Tom Hanks and Bill Paxton starred in Apollo 13
2: Bill Paxton and Tom Cruise starred in Edge of Tomorrow
```

# Requirements
No requirements. Only for Python 3.