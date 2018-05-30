#LZ programming language


A programing language I made for really lazy typers


## Synopsis

Hello there. 2 days ago we were asked to submit a programming language for a class. I made it to for really **lazy** programmers. So I called it **lazy** or **lz**.

I wanted mine to have really lazy keywords, so all the keywords it used are only two letters long. Plus I tried that most of the symbols used, to the best of my ability didn't use the *SHIFT* key.

I hope that this can grow and be developed. I have actually never maintained any large project so this would be my first. Any help would be appreciated.


## Language Syntax
**comments**
```
\this is a comment it uses a backslash
```

**printing**

it uses the **pr** keyword and an **rp** keyword to end. To print a new line, write **nl**
```
pr '1 + 1 is' 1+1 rp
nl
pr '2 + 2 is' 2+2 rp

```
> 1 + 1 is 2
>
> 2 + 2 is 4

**input**

it uses the **ip** keyword so type the keyword then the variable name after **ip**
```
userInput = st "nothing"
pr 'input a value' rp
ip unserInput
pr 'user input is ' userInput rp

```
> 2
> userInput is 2

**if statements**
```
a = in 1
if[a == 1]
    pr 'this if works' rp
fi
```
> this if works

**if-else statements**
```
a = in 1
if[a < 1]
    pr 'it shouldn't be here a is equal to one' rp
fi
el
    pr 'eyy the code works' rp
le
```
> eyy the code works


**while loops**
```
count = in 1
asterisks = []
wh[count < 10]
    pu asterisks count up
    count = count + 1
hw
pa asterisks
```
>[1, 2, 3, 4, 5, 6, 7, 8, 9]

**integer declaration**
```
integer1 = in 1
```

**float declaration**
```
floatVar = fl 1.0
```

**string declaration**
```
stringVar = st 'heyyyy'
```

## Number System

Gab Lopez, a friend of mine designed a new phonetic number system since some numbers have 2 syllables or are hard to pronounce. Here is a modified version of his original number system.

wa - 0

oh - 1

to - 2

ti - 3

fo - 4

fi - 5

si - 6

se - 7

ei - 8

ni - 9

**word lz-number input**

it automatically converts the word form to a number form. It only needs the grave accent to mark the number.
```
pr `tiohfoohfinitositi rp
```
>314159263

The word *do* denotes a decimal point.
```
pr `tidoohfoohfinitositi rp
```
>3.14159263

These can also be used as a number

The word *do* denotes a decimal point.
```
pr `tidoohfoohfinitositi + `ohdowawawawawawa rp
```
>4.14159263

**numerical lz-number input**

When you type the number form with the grave accent it converts it to a string form. This form can no longer be used for operations.
```
pr `3.14159263 ' + ' `1.000000 ' equals ' `tidoohfoohfinitositi + `ohdowawawawawawa rp
```
> tidoohfoohfinitositi  +  ohdowawawawawawa  equals  4.14159263

## Motivation

I actually made this language to implement the number system above but I realized more people might want to use this language for its imperative laziness.

It is suprisingly a little better at lists and arrays than C (but isnt powerful yet to have pointers). It has push, pop, top, a length, and even an isEmpty function. I shall add these later on. Thanks to Python.

## Installation

**Dependencies:**

*-Python 2.7.15*

*-Linux OS*

*-(optional PLY)*


## Running and Compilation/Interpretation

To compile put the file in the same folder and copy the following text in terminal. You can replace readme.lz with any file name
```
python cidcompiler.py readme.lz
```

### For first time github users
To install, clone the git repository to your folder...

It's actually my first time using github as well. But I do want to make this part easy for people who don't know how to use github as well.

## Future Features

I plan to make this a fully fledged language by 2021. But so far I am currently learning everything, this was my first language and even github project as well.

- function implementation
- file reading
- its first standard library
- easier installation, compilation
- its own Jupyter notebook

## Contributors

I have been the only one developing this at this point. If you want to help me develop this language more. Maybe you know how to make a proper compiler or know how to make the grammar better or have ideas on the language or number system please do message me. or email me jjazcarraga@up.edu.ph

## License

The number system has been legally and appropriately requested permission for use from Gabriel Henry Lopez.

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
