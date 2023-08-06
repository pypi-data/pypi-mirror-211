# pytokr

Very simple, somewhat stoned tokenizer for teaching purposes.

Current pip-installable version is 0.0.2 but the current status
of the repository is version 0.1.0.

Behaviorally inspired by the early versions of the 
[easyinput module](https://github.com/jutge-org/easyinput); 
shares with it some similar aims, but not the aim of 
conceptual consistency with C/C++. 

<!--- Actually easyinput 
has grown in ways I find somewhat inappropriate for 
many of my current (non-CS) students and I want to 
try now a different road. --->

A separate, different evolution of `easyinput` is 
[yogi](https://github.com/jutge-org/yogi).

## Install

The usual incantation should work: pip install pytokr
(maybe with either "sudo" or "--user" or within a 
virtual environment).

If that does not work, download or clone the repo, then 
put the pytokr folder where Python can see it from 
wherever you want to use it.

## Simplest usage since version 0.1.0

Finds items (simple tokens white-space separated) in a 
string-based iterable such as stdin (default). Ends of 
line are counted as white space but are otherwise ignored. Usage:

`from pytokr import pytokr`

then call pytokr to obtain the tokenizer function; give it 
whatever name you see fit, say, `item`:

`item = pytokr()`

Then, successive calls to `item()` will provide you with
successive tokens from `stdin`. In case no items remain,
an EndOfDataError exception will be raised. Note that, 
as white-space is ignored, in case only white-space remains 
then the program *is* at end of data.

If a different source of items is desired, say `source` 
(e.g. a `file` just `open`'ed or a list of strings), 
simply pass it on:

`item = pytokr(source)`

In either case, a second output can be requested, namely, an
iterator over the items, say you want to name it `items`:

`item, items = pytokr(iter = True)`

(such call would accept as well a `source` as first parameter).
Then you can run `for itm in items():` or make up a `ls = list(items())`
and, with some care, avoid the dependence on the EndOfDataError
exception.

Both combine naturally: the individual item function can be called 
inside a for loop on the iterator, provided there is still 
at least one item not yet read. That call will advance the 
items; so, the next item at the loop will be the current one after 
the local advances. Briefly: both advance *the same* iterator.

<!--- Both calls combine naturally: it is valid to call `item()` 
within a `for w in items()` loop provided there is still 
at least one item not yet read. The reading will advance 
on and the next item in the loop will correspond to the 
advance. 

Token items are returned as strings; the user should cast them as
int or float or whatever when appropriate. --->

All items provided are of type `str` and will not contain 
white space; casting into `int` or `float` or whatever, if
convenient, falls upon the caller. 

## Example

Based on [Jutge problem P29448](https://jutge.org/problems/P29448_en)
Correct Dates (and removing spoilers):

    from pytokr import pytokr
    item, items = pytokr(f, iter = True)
    for d in items():
        m, y = item(), item()
        if correct_date(int(d), int(m), int(y)):
            print("Correct Date")
        else:
            print("Incorrect Date")

## Deprecated usage of versions 0.0.*

These versions were employed in a different manner. Version
0.1.0 can still be employed in the same way for some
backwards compatibility, but will print a deprecation
message to `stderr`. This old usage was:

`from pytokr import item, items`

(or only one of them as convenient). Then `item()` will provide
the next item in `stdin` and `for w in items()` will iterate on
whatever remains there. Calling `item()` at end of file will
raise an exception EndOfDataError. 

### Old, deprecated usage on other string-based iterables

Again, this still works on 0.1.0 but will print a deprecation
message on `stderr`:

`from pytokr import make_tokr`

Then, if `g` is an iterable of strings such as an open
file or a list of strings, the call

`items, item = make_tokr(g)`

will provide adapted versions of `item` and `items` that
will read them in from `g` instead of from `stdin`.

<!--- ## To do: 

- As said, call to `item()` raises `StopIteration` on 
end of file; it will be a common error when mixing it 
with `items()`. Consider catching it and raising instead 
an exception more understandable by beginners.

- Sources in the 'deprecated/jutge-like' folder use 
obsolete identifiers; keep updating them and moving
them to 'jutge_like'.

- I called initially the items 'toks' (for very simple 
'tokens') but that sounded a bit inappropriate to me, 
first, because of the simplicity of the case and, 
second, due to the early programming level of my 
target students. Calling them 'items' seems suboptimal 
though, since we are going to study `dict`'s later on 
and then risk confusions. But I settled on 'items' for 
the time being anyway; alternative suggestions welcome.
--->
