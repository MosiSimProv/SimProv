from simprov import *


@rule("DEMO EVENT")
def foo(event):
    return "Simulation Model"


@rule("CONFLICT")
def bar(event):
    return "Experiment"


@rule("DEMO EVENT")
def bar(event):
    return "Experiment"
