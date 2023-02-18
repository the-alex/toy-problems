"""
Unit conversions
================

Given a list of 3-tuples mapping a unit of one type to a multiple of another
unit.

Input string map:
kilometer 1000 meter
meter 100 centimeter
meter 39.37 inch
mile 5280 foot
foot 12 inch
inch 2.54 centimeter
"""

from pprint import pprint
import sys
from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    from_: str
    to: str
    multiple: float


def read_input():
    """
    Read the input string from stdin.
    """
    return sys.stdin.read()


def parse_input(text) -> List[Rule]:
    """
    Parse the input string into a list of tuples.
    """
    tups = [tuple(line.split()) for line in text.splitlines() if line]
    rules = [
        Rule(from_=tup[0], to=tup[2], multiple=float(tup[1])) for tup in tups if tup
    ]
    return rules


def learn(rules: List[Rule]):
    """Takes a list of rules and builds a knowledge graph of unit conversion
    facts"""

    facts = {}
    for r in rules:
        facts[r.from_] = (r.to, r.multiple)
        facts[r.to] = (r.from_, 1 / r.multiple)

    return facts


def query(start, to, facts):
    conversion_multiple = 1
    for unit, (conversion, multiplier) in facts.items():

        # Rebuild facts without this node -- "touched" this node already
        facts = {u: (c, m) for u, (c, m) in facts.items() if u != unit}

        if unit == start:
            return conversion_multiple * multiplier

        else:
            start = conversion
            conversion_multiple *= multiplier * query(start, to, facts)

    return conversion_multiple


if __name__ == "__main__":
    input_string = """
    kilometer 1000 meter
    meter 1000 centimeter
    meter 39.37 inch
    inch 2.54 centimeter
    foot 12 inch
    mile 5280 feet
    """

    rules = parse_input(
        """
        kilometer 1000 meter
        meter 100 centimeter
    """
    )

    facts = learn(rules)

    pprint(rules)
    pprint(facts)
    print("-" * 80)

    # for q in queries:
    #     from_, to = q.split()
    #     print(q, query(from_, to, facts))

    km_to_m = query("kilometer", "meter", facts)
    assert km_to_m == 1000.0, f"{km_to_m} != 1000.0"

    km_to_m = query("kilometer", "centimeter", facts)
    assert km_to_m == 100000.0, f"{km_to_m} != 100000.0"