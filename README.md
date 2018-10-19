## Python-Cool
### A compiler for COOL (Classroom Object Oriented Language) programming language built entirely in Python.

Python-Cool is a compiler for COOL (Classroom Object Oriented Language) targeting the MIPS 32-bit Architecture and written entirely in Python 3. COOL is a small statically-typed object-oriented language that is type-safe and garbage collected. It has mainly 3 primitive data types: Integers, Strings and Booleans (true, false). It supports conditional and iterative control flow in addition to pattern matching.

Python-COOL comprises of two main components the front-end and back-end.
- Compiler Frontend consists of the following three stages:
- - Lexical Analysis: regex-based tokenizer.
- - Syntax Analysis: An LALR(1) parser.
- - Semantic Analysis.

- Compiler Backend consists of the following two stages:
- - Code Generation:
- - Targets the MIPS 32-bit architecture
