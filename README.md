<div align="center">
<img src="https://github.com/sepandhaghighi/typio/raw/main/otherfiles/logo.png" width="320">
<h1>Typio: Make Your Terminal Type Like a Human</h1>
<br/>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/built%20with-Python3-green.svg" alt="built with Python3"></a>
<a href="https://github.com/sepandhaghighi/typio"><img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/sepandhaghighi/typio"></a>
<a href="https://badge.fury.io/py/typio"><img src="https://badge.fury.io/py/typio.svg" alt="PyPI version"></a>
<a href="https://codecov.io/gh/sepandhaghighi/typio"><img src="https://codecov.io/gh/sepandhaghighi/typio/graph/badge.svg?token=UPhwanwQVw"></a>
</div>			
				
## Overview	

<p align="justify">
Typio is a lightweight Python library that prints text to the terminal as if it were being typed by a human. It supports multiple typing modes (character, word, line, sentence, typewriter, and adaptive), configurable delays and jitter for natural variation, and seamless integration with existing code via a simple function or a decorator. Typio is designed to be minimal, extensible, and safe, making it ideal for demos, CLIs, tutorials, and storytelling in the terminal.
</p>

<table>
	<tr>
		<td align="center">PyPI Counter</td>
		<td align="center"><a href="http://pepy.tech/project/typio"><img src="http://pepy.tech/badge/typio"></a></td>
	</tr>
	<tr>
		<td align="center">Github Stars</td>
		<td align="center"><a href="https://github.com/sepandhaghighi/typio"><img src="https://img.shields.io/github/stars/sepandhaghighi/typio.svg?style=social&label=Stars"></a></td>
	</tr>
</table>



<table>
	<tr> 
		<td align="center">Branch</td>
		<td align="center">main</td>	
		<td align="center">dev</td>	
	</tr>
	<tr>
		<td align="center">CI</td>
		<td align="center"><img src="https://github.com/sepandhaghighi/typio/actions/workflows/test.yml/badge.svg?branch=main"></td>
		<td align="center"><img src="https://github.com/sepandhaghighi/typio/actions/workflows/test.yml/badge.svg?branch=dev"></td>
	</tr>
</table>

<table>
    <tr> 
        <td align="center">Code Quality</td>
        <td align="center"><a href="https://www.codefactor.io/repository/github/sepandhaghighi/typio"><img src="https://www.codefactor.io/repository/github/sepandhaghighi/typio/badge" alt="CodeFactor"></a></td>
        <td align="center"><a href="https://app.codacy.com/gh/sepandhaghighi/typio/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade"><img src="https://app.codacy.com/project/badge/Grade/e047db39052a4be2859f299dd7f7ce3c"></a></td>
    </tr>
</table>

## Installation		

### Source Code
- Download [Version 0.1](https://github.com/sepandhaghighi/typio/archive/v0.1.zip) or [Latest Source](https://github.com/sepandhaghighi/typio/archive/dev.zip)
- `pip install .`				

### PyPI

- Check [Python Packaging User Guide](https://packaging.python.org/installing/)     
- `pip install typio==0.1`						


## Usage

### Function

Use `type_print` function to print text with human-like typing effects. You can control the typing speed, randomness, mode, and output stream.

```python
from typio import type_print
from typio import TypeMode

type_print("Hello, world!")

type_print(
    "Typing with style and personality.",
    delay=0.06,
    jitter=0.02,
    mode=TypeMode.ADAPTIVE,
)
```

You can also redirect the output to any file-like object:

```python
with open("output.txt", "w") as file:
    type_print("Saved with typing effects.", file=file)
```

### Decorator

Use the `@typestyle` decorator to apply typing effects to all `print` calls inside a function, without changing the function's implementation.

```python
from typio import typestyle
from typio import TypeMode

@typestyle(delay=0.05, mode=TypeMode.TYPEWRITER)
def intro():
    print("Welcome to Typio.")
    print("Every print is typed.")

intro()
```

## Issues & Bug Reports			

Just fill an issue and describe it. We'll check it ASAP!

- Please complete the issue template

## Show Your Support
								
<h3>Star This Repo</h3>					

Give a ⭐️ if this project helped you!

<h3>Donate to Our Project</h3>	

<h4>Bitcoin</h4>
1KtNLEEeUbTEK9PdN6Ya3ZAKXaqoKUuxCy
<h4>Ethereum</h4>
0xcD4Db18B6664A9662123D4307B074aE968535388
<h4>Litecoin</h4>
Ldnz5gMcEeV8BAdsyf8FstWDC6uyYR6pgZ
<h4>Doge</h4>
DDUnKpFQbBqLpFVZ9DfuVysBdr249HxVDh
<h4>Tron</h4>
TCZxzPZLcJHr2qR3uPUB1tXB6L3FDSSAx7
<h4>Ripple</h4>
rN7ZuRG7HDGHR5nof8nu5LrsbmSB61V1qq
<h4>Binance Coin</h4>
bnb1zglwcf0ac3d0s2f6ck5kgwvcru4tlctt4p5qef
<h4>Tether</h4>
0xcD4Db18B6664A9662123D4307B074aE968535388
<h4>Dash</h4>
Xd3Yn2qZJ7VE8nbKw2fS98aLxR5M6WUU3s
<h4>Stellar</h4>		
GALPOLPISRHIYHLQER2TLJRGUSZH52RYDK6C3HIU4PSMNAV65Q36EGNL
<h4>Zilliqa</h4>
zil1knmz8zj88cf0exr2ry7nav9elehxfcgqu3c5e5
<h4>Coffeete</h4>
<a href="http://www.coffeete.ir/opensource">
<img src="http://www.coffeete.ir/images/buttons/lemonchiffon.png" style="width:260px;" />
</a>

