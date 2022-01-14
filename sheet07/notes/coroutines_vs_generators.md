# Coroutines vs Generators.

From python glossary we read:

> **generator**
> 
> A function which returns a **generator iterator**. It looks like a normal function 
> except that it contains **yield expressions** for producing a series of values usable in 
> a for-loop or that can be retrieved one at a time with the next() function.
> 
> Usually refers to a **generator function**, but may refer to a **generator iterator** in some contexts. 
> In cases where the intended meaning isn’t clear, using the full terms avoids ambiguity.

A **yield expression** is mentioned in the definition above let's see what that's all about.

We can find the definition for it in <a href="https://docs.python.org/3/reference/expressions.html">
python reference chapter discussing expressions</a>. It states the following.



So as we can see generator is just a function that returns some object. That object happens to be
called **generator iterator**, let's see what glossary has to say about those.

> **generator iterator**
> 
> An object created by a generator function.
> Each yield temporarily suspends processing, remembering the location execution state 
> (including local variables and pending try-statements). When the generator iterator resumes, 
> it picks up where it left off (in contrast to functions which start fresh on every invocation).

Sadly in glossary there is no explanation of what a **generator function** is. To find that we need
to take a little detour.

We'll visit <a href="https://www.python.org/dev/peps/pep-0255/#specification-yield">PEP 255</a>
it introduced generators to python back in 2001. In 
<a href="https://www.python.org/dev/peps/pep-0255/#specification-yield">
section discussing `yield` keyword</a> mentioned earlier we see.

>The yield statement may only be used inside functions. 
> **A function that contains a yield statement is called a generator function**. 
> A generator function is an ordinary function object in all respects, 
> but has the new `CO_GENERATOR` flag set in the code object's `co_flags` member.

# Important terms:

- **generator** - a sepcial iterator
- **generator function** - a function that contains `yield` expression or statement
- **generator expression** - list comprehension-like syntax for defining generators 
- **coroutine**
- **yield statement**
- **yield expression**
- ****

# References:

Glossary:
- https://docs.python.org/3/glossary.html

Python language expressions:
- https://docs.python.org/3/reference/expressions.html

Related PEP's:
- https://www.python.org/dev/peps/pep-0255/
- https://www.python.org/dev/peps/pep-0289/
- https://www.python.org/dev/peps/pep-0342/
- https://www.python.org/dev/peps/pep-0380/
- https://www.python.org/dev/peps/pep-0492/