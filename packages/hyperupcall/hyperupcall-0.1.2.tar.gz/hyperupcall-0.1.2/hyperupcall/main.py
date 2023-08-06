from typing import TypeAlias

number: TypeAlias = int | float

def add(a: number, b: number) -> number:
    return a + b
