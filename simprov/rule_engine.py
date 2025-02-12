from dataclasses import dataclass
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from typing import Callable, Dict, Union

from simprov import Activity
from simprov.exceptions import InvalidRuleSpecificationException, InvalidRuleResultException, NoRuleFoundException

ENGINE = None


@dataclass
class Rule:
    """Represents a rule that is used for extracting an activity from an event.

    :ivar str event_type:
        The name of the event for which the rule should be executed.
    :ivar Callable func:
        The function that extracts the activity.
    """
    event_type: str
    func: Callable


def rule(event_type:str):
    """
    The decorator that shall be used to mark a python function as a rule for SimProv

    :param str event_type:
        The name of the event
    """
    def _inner(func):
        rule = Rule(event_type, func)
        ENGINE.register_rule(rule)
        return func

    return _inner


class RuleEngine:
    """ Represents the rule engine that manages the rules for extracting a provenance activity from the incoming events.

    :param Union[str, Path], optional rule_path:
        When provided the rules are loaded from the file.

    :ivar Dict[str,Rule] rule_table:
        A lookup table from an event type to its corresponding rule
    """

    def __init__(self, rule_path: Union[str, Path] = None):
        super().__init__()
        self.rule_table: Dict[str, Rule] = {}
        if rule_path:
            self.load_rules(rule_path)

    def register_rule(self, rule: Rule):
        """ Registers a new rule.

        :param Rule rule:
            The rule.
        :raises InvalidRuleSpecificationException:
            If a rule for the corresponding event type is already registered.
        """
        if rule.event_type in self.rule_table:
            raise InvalidRuleSpecificationException(f"Rule for event type \"{rule.event_type}\" already exists.")
        self.rule_table[rule.event_type] = rule

    def load_rules(self, file_path: Union[str, Path]):
        """ Loads all rules from a given file.

        :param Union[str, Path] file_path:
            The file path.
        """
        global ENGINE
        ENGINE = self
        self.rule_table.clear()
        spec = spec_from_file_location("my.rules", file_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        ENGINE = None

    def execute_rule(self, event: Dict) -> Activity:
        """Executes the rule that corresponds to the event type to extract the activity..

        :param Dict event:
            The event.
        :rtype: Activity
        :return: The extracted activity.
        :raises NoRuleFoundException:
            If no rule for the event type can be found.
        :raises InvalidRuleResultException:
            If the result of the rule is not an activity.
        """
        processing_rule = self.rule_table.get(event["type"], None)
        if processing_rule is None:
            raise NoRuleFoundException(f"Can't find rule for event: {event}")
        rule_result = processing_rule.func(event)
        if not isinstance(rule_result, Activity):
            raise InvalidRuleResultException(f"Rule has to return an activity")
        return rule_result
