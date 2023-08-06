"""Main module."""

import pandas as pd
import logging
import itertools
import re
from pyparsing import *

from ruleminer.const import DUNDER_DF
from ruleminer.const import VAR_Z

AND = one_of(["AND", "and", "&"])
OR = one_of(["OR", "or", "|"])
NOT = one_of(["NOT", "~"])
SEP = Literal(",")

QUOTE = Literal("'") | Literal('"')
ARITH_OP = one_of("+ - * /")
LOGIC_OP = one_of("& |")
COMPA_OP = one_of(">= > <= < != == in")
PREFIX_OP = one_of("min max abs quantile MIN MAX ABS QUANTILE")
NUMBER = Combine(Word(nums) + "." + Word(nums)) | Word(nums)
STRING = srange(r"[a-zA-Z0-9_.,:;<>*=+-/\\?|@#$%^&()']") + " "
COLUMN = Combine("{" + QUOTE + Word(STRING) + QUOTE + "}")
QUOTED_STRING = Combine(QUOTE + Word(STRING) + QUOTE)

PARL = Literal("(").suppress()
PARR = Literal(")").suppress()

# STRING_2 = srange(r"[a-zA-Z0-9_.,:;*+-/\\?|@#$%^&']") + " "
# COLUMN_VARIABLE = (PARL+Literal("?P<")+Word(STRING_2)+Literal(">")+COLUMN+PARR) | (PARL+Literal("?P=")+Word(STRING_2)+PARR)

ARITH_COLUMNS = Group((COLUMN | NUMBER) + (ARITH_OP + (COLUMN | NUMBER))[1, ...])
COLUMNS = (PARL + ARITH_COLUMNS + PARR) | ARITH_COLUMNS | COLUMN | NUMBER
PREFIX_COLUMN = PREFIX_OP + Group(PARL + COLUMNS + (SEP + COLUMNS)[0, ...] + PARR)
QUOTED_STRING_LIST = Group(
    Literal("[") + QUOTED_STRING + (SEP + QUOTED_STRING)[0, ...] + Literal("]")
)

# TERM = PREFIX_COLUMN | COLUMNS | QUOTED_STRING | QUOTED_STRING_LIST | COLUMN_VARIABLE
TERM = PREFIX_COLUMN | COLUMNS | QUOTED_STRING | QUOTED_STRING_LIST

COMP_EL = TERM + COMPA_OP + TERM
COMP = Group((PARL + COMP_EL + PARR))
CONDITION = infixNotation(
    COMP,
    [
        (
            NOT,
            1,
            opAssoc.RIGHT,
        ),
        (
            AND,
            2,
            opAssoc.LEFT,
        ),
        (
            OR,
            2,
            opAssoc.LEFT,
        ),
    ],
)
IF_THEN = "if" + CONDITION + "then" + CONDITION
RULE_SYNTAX = IF_THEN | "if () then " + CONDITION | CONDITION


def python_code_lengths(expression: str = "", required: list = []):
    """ """

    regex_condition = re.compile(r"if(.*)then(.*)", re.IGNORECASE)
    rule = regex_condition.search(expression)

    if_part = rule.group(1).strip()
    then_part = rule.group(2).strip()

    python_expressions = {}
    for variable in required:
        if variable == "N":
            python_expressions[variable] = "len("+DUNDER_DF+".values)"
        if variable == "X":
            if if_part == "()":
                python_expressions[variable] = "len("+DUNDER_DF+".index)"
            else:
                python_expressions[variable] = "("+replace_columns(if_part)+").sum()"
        elif variable == "~X":
            python_expressions[variable] = "(~("+replace_columns(if_part)+")).sum()"
        elif variable == "Y":
            python_expressions[variable] = "("+replace_columns(then_part)+").sum()"
        elif variable == "~Y":
            python_expressions[variable] = "(~("+replace_columns(then_part)+")).sum()"
        elif variable == "X and Y":
            python_expressions[variable] = "(("+replace_columns(if_part)+") & ("+replace_columns(then_part)+ ")).sum()"
        elif variable == "X and ~Y":
            python_expressions[variable] = "(("+replace_columns(if_part)+") & ~("+replace_columns(then_part)+ ")).sum()"
        elif variable == "~X and ~Y":
            python_expressions[variable] = "(~("+replace_columns(if_part)+") & ~("+replace_columns(then_part)+ ")).sum()"

    for e in python_expressions.keys():
        python_expressions[e] = python_expressions[e].replace("[(())]", "")
        python_expressions[e] = python_expressions[e].replace("(()) & ", "")
        python_expressions[e] = python_expressions[e].replace("[~(())]", "[False]")
    return python_expressions


def python_code_index(expression: str = "", required: list = []):
    """ """

    regex_condition = re.compile(r"if(.*)then(.*)", re.IGNORECASE)
    rule = regex_condition.search(expression)

    if_part = rule.group(1).strip()
    then_part = rule.group(2).strip()

    python_expressions = {}
    for variable in required:
        if variable == "N":
            python_expressions[variable] = DUNDER_DF + ".index"
        if variable == "X":
            python_expressions[variable] = (
                DUNDER_DF + ".index[(" + replace_columns(if_part) + ")]"
            )
        elif variable == "~X":
            python_expressions[variable] = (
                DUNDER_DF + ".index[~(" + replace_columns(if_part) + ")]"
            )
        elif variable == "Y":
            python_expressions[variable] = (
                DUNDER_DF + ".index[(" + replace_columns(then_part) + ")]"
            )
        elif variable == "~Y":
            python_expressions[variable] = (
                DUNDER_DF + ".index[~(" + replace_columns(then_part) + ")]"
            )
        elif variable == "X and Y":
            python_expressions[variable] = (
                DUNDER_DF
                + ".index[("
                + replace_columns(if_part)
                + ") & ("
                + replace_columns(then_part)
                + ")]"
            )
        elif variable == "X and ~Y":
            python_expressions[variable] = (
                DUNDER_DF
                + ".index[("
                + replace_columns(if_part)
                + ") & ~("
                + replace_columns(then_part)
                + ")]"
            )
        elif variable == "~X and ~Y":
            python_expressions[variable] = (
                DUNDER_DF
                + ".index[~("
                + replace_columns(if_part)
                + ") & ~("
                + replace_columns(then_part)
                + ")]"
            )
    for e in python_expressions.keys():
        python_expressions[e] = python_expressions[e].replace("[(())]", "")
        python_expressions[e] = python_expressions[e].replace("(()) & ", "")
        python_expressions[e] = python_expressions[e].replace("[~(())]", "[False]")
    return python_expressions


def replace_columns(s: str = ""):
    """Function to replace the column names by a numpy expressions

    Numpy approach:
    {"A"} is rewritten to __df__.values[:, __df__.columns.get_loc("A")]

    Pandas approach:
    {"A"} is rewritten to __df__["A"]

    """
    # return s.replace(
    #     "{", DUNDER_DF + ".values[:, " + DUNDER_DF + ".columns.get_loc("
    # ).replace("}", ")]")
    return s.replace("{", DUNDER_DF + "[").replace("}", "]")


def python_code_for_columns(expression: str = ""):
    """ """
    return {
        VAR_Z: (DUNDER_DF + "[(" + replace_columns(expression) + ")]").replace("[()]", "")
    }


def python_code_for_intermediate(expression: str = ""):
    """ """
    return {VAR_Z: (replace_columns(expression)).replace("[()]", "")}
