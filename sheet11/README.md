# A

As for tests I used tests that I originally supplied with my solutions for sheet05 ex1c.
I also added new tests for sheet03 ex1 (primes).

Tests reside in directories `sheet03/test` and `sheet05/test`.

# B

## Instructions for the `cProfile` module.

```
PS > py -m cProfile sheet03/Ex1-Depta.py -o "sheet03-profile.txt"
PS > py -m pstats "sheet03-profile.txt"
```

## Instructions for the `pstats` module.

```
sheet03-profile.txt% sort time calls
sheet03-profile.txt% stats
Sun Jan  9 00:03:16 2022    sheet03-profile.txt

         2079275 function calls (2079269 primitive calls) in 5.126 seconds                          

   Ordered by: internal time, call count                                                            

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)                             
  1000000    4.754    0.000    4.851    0.000 sheet03/ex1_Depta.py:18(is_prime)                     
        1    0.138    0.138    2.582    2.582 sheet03/ex1_Depta.py:33(prime_imperative)             
        1    0.115    0.115    2.531    2.531 sheet03/ex1_Depta.py:80(<listcomp>)                   
   999998    0.097    0.000    0.097    0.000 {built-in method math.ceil}                           
    78521    0.008    0.000    0.008    0.000 {method 'append' of 'list' objects}                   
        1    0.007    0.007    2.538    2.538 sheet03/ex1_Depta.py:44(prime_comprehension)          
        1    0.004    0.004    5.124    5.124 sheet03/ex1_Depta.py:127(main)                        

        [...] # other entries skipped (mostly python runtime lib calls as well as profiler intrinsic calls)

        1    0.000    0.000    0.000    0.000 sheet03/ex1_Depta.py:82(prime_functional)
```

## Discussion

I sorted the profiling results by time of execution. I omitted a large chunk of input which I guess was
related to python runtime and profiler itself.

As expected `is_prime` function is called the most often and program spends most of it's running time in it.
It's also make it a *prime* ( hehe ) candidate for optimizations. Other interesting thing that we can observe is extensive
use of `math.ceil` function. Number of calls as well as the total time spent within the function is somewhat substantial.
`append` method of the `list` is another function that is called quite frequently and takes up a fair chunk of time.
We cannot do anything about it other than using the alternative implementations.

# C

Accordingly to PyCharm all my code follows PEP8 guidelines. I also double checked all files with online PEP8 utility most of complaints
that I received stemmed from my docstrings where I talked about my solution which in my mind does not count.

Test code unfortunately is not compliant.
This is due to unittest module being older than PEP8 itself. This is acknowledged by the PEP8.

> Some other good reasons to ignore a particular guideline:
> 1. When applying the guideline would make the code less readable, even for someone who is used to reading code that follows this PEP.
> 2.To be consistent with surrounding code that also breaks it (maybe for historic reasons) -- although this is also an opportunity to clean up someone else's mess (in true XP style).
> **3. Because the code in question predates the introduction of the guideline and there is no other reason to be modifying that code.**
> 4. When the code needs to remain compatible with older versions of Python that don't support the feature recommended by the style guide.

During this course I also found similar issues with the following standard modules:
- `datetime.datetime` - it's a class so it should be capitalized.
- `sched.scheduler` - again class should be capitalized.


# D

I tried using both `sphinx` package and the standard `pydoc` but it appears that both require explicit annotations and descriptions of input/output params. Maybe this is not the case I don't know really.

