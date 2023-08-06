# Mi diferenciación 
## This little package proof would help you solve some derivates given a defined function. 

<!-- This are visual tags that you may add to your package at the beginning with useful information on your package --> 
[![version 0.45](https://img.shields.io/pypi/v/pymiau?color=blue)](https://pypi.org/project/midiferenciacion/)
[![downloads](https://img.shields.io/pypi/dw/midiferenciacion)](https://pypi.org/project/midiferenciacion/)

Math is not easy, right? You can use some tools to make it easier at least for some calculations. 
This simple package will help you in that. 

<p align="center"><img src="https://drive.google.com/uc?export=view&id=1P4T-6cMTga6iO4rFBhVvevcg1CgBuUto" alt="Logo""/></p>

## Download and install

If you are using `PyPI` installation it's as simple as:

```
pip install midiferenciacion
```

You can also test the unstable version of the package with:

```
pip install -i https://test.pypi.org/simple/midiferenciacion
```

## Quick start

First import the midiferenciacion

```
import midiferenciacion

```
Now, you have to be careful with the input of the only function we have for now: derivative. This function gives you the first derivative and you can evaluate the result in two defined points. 

The function derivative receives a function in a string format and (very important) in terms of x variable, and it also receives two values to evaluate the solution.

Here's an example of a single function:

```
midiferenciacion.derivative("x**2", 1, 2)

```

## What's new



Version 0.45:

- README updates and beautiful meme

Version 0.4:

- First version of the package.

------------

This package has been designed and written by Fulanit@ de Tal (C) 2023