import pytest

# from simprov import engine
# from simprov.api import start_simprov
from simprov.rule_engine import InvalidRuleSpecificationException, NoRuleFoundException, InvalidRuleResultException, \
    RuleEngine


def test_rule_loading_invalid_rules(error_rules_path):
    engine = RuleEngine()
    with pytest.raises(InvalidRuleSpecificationException):
        engine.load_rules(error_rules_path)


def test_rule_loading(real_rules_path):
    engine = RuleEngine()
    try:
        engine.load_rules(real_rules_path)
    except Exception as ex:
        pytest.fail("Unexpected error")


def test_rule_evaluation_invalid_event(real_rules_path):
    engine = RuleEngine()
    engine.load_rules(real_rules_path)
    event = {"type": "Error"}
    with pytest.raises(NoRuleFoundException):
        engine.execute_rule(event)


def test_rule_evaluation_invalid_result(real_rules_path):
    engine = RuleEngine()
    engine.load_rules(real_rules_path)
    event = {"type": "Invalid Result Event"}
    with pytest.raises(InvalidRuleResultException):
        engine.execute_rule(event)

# def test_rule_event_processing(real_rules_path, real_entities_path, real_activities_path, complex_event):
#     start_simprov(real_rules_path, real_entities_path, real_activities_path)
#     engine.load_rules(real_rules_path)
#     result = engine.process_event(complex_event)
#     # TODO: Asserts
