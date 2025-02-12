import pytest

from simprov import Entity, Activity
from simprov.exceptions import InvalidEntitySpecificationException, PrimaryKeyAttributeNotDefinedException, \
    EntitySpecificationNotFoundException, ActivitySpecificationNotFoundException, InvalidActivityException
from simprov.specifications import SpecificationManager, OccurenceModifier


def test_simple_entity_specification_loading(specs_path):
    manager = SpecificationManager()
    manager.load_specification_file(specs_path)
    assert len(manager.entity_specifications) == 9
    assert len(manager.activity_specifications) == 8
    assert len(manager.agent_specifications) == 1



def test_invalid_entity_specification_loading(specs_path):
    manager = SpecificationManager()
    manager.load_specification_file(specs_path)
    with pytest.raises(EntitySpecificationNotFoundException):
        entity = Entity("FOOOO")
        manager.get_entity_specification(entity.name)


def test_invalid_activity_specification_loading(specs_path):
    manager = SpecificationManager()
    manager.load_specification_file(specs_path)
    with pytest.raises(ActivitySpecificationNotFoundException):
        activity = Activity("FOOOO")
        manager.get_activity_specification(activity.name)


def test_simple_entity_specification_loading_simulation_model(specs_path):
    manager = SpecificationManager()
    manager.load_specification_file(specs_path)
    simulation_model_entity = manager.entity_specifications["Simulation Model"]
    expected_attributes = ["File Path", "Content"]
    expected_attributes_required_attributes = ["File Path"]
    expected_primary_key_attributes = ["File Path"]
    assert (sorted(expected_attributes) == sorted(simulation_model_entity.attributes))
    assert (sorted(expected_attributes_required_attributes) == sorted(simulation_model_entity.required_attributes))
    assert (sorted(expected_primary_key_attributes) == sorted(simulation_model_entity.primary_key_attributes))


def test_simple_entity_specification_loading_demo_entity(specs_path):
    manager = SpecificationManager()
    manager.load_specification_file(specs_path)
    experiment_entity = manager.entity_specifications["Demo Entity"]
    expected_attributes = ["foo", "bar", "bak", "zar", "gag"]
    expected_attributes_required_attributes = ["foo", "bar", "bak", "zar"]
    expected_attributes_primary_attributes = ["foo", "zar"]
    assert (sorted(expected_attributes) == sorted(experiment_entity.attributes))
    assert (sorted(expected_attributes_required_attributes) == sorted(experiment_entity.required_attributes))
    assert (sorted(expected_attributes_primary_attributes) == sorted(experiment_entity.primary_key_attributes))


def test_invalid_entity_specification_loading2():
    error_entities = ("Error Entity", {"attributes": ["attribute_1", "attribute_2"]})
    with pytest.raises(InvalidEntitySpecificationException):
        manager = SpecificationManager()
        manager._build_entitiy_specification(error_entities)


def test_normalization_simple_entity(specs_path):
    demo_path = "/demo/path"
    manager = SpecificationManager()
    manager.load_specification_file(specs_path)
    entity = Entity("Simulation Model")
    entity.attributes["File Path"] = demo_path

    assert not "Content" in entity.attributes
    assert entity.primary_key is None
    manager.normalize_entity(entity)
    assert "Content" in entity.attributes and entity.attributes["Content"] is None
    assert entity.primary_key == (demo_path,)


def test_not_normalized_and_check_entity(specs_path):
    demo_path = "/demo/path"
    manager = SpecificationManager()
    manager.load_specification_file(specs_path)
    entity = Entity("Demo Entity")
    entity.attributes["foo"] = demo_path
    with pytest.raises(PrimaryKeyAttributeNotDefinedException):
        manager.validate_entity(entity)


def test_normalized_and_check_entity(specs_path):
    demo_path = "/demo/path"
    manager = SpecificationManager()
    manager.load_specification_file(specs_path)
    entity = Entity("Demo Entity")
    entity.attributes["foo"] = demo_path
    entity.attributes["zar"] = None
    manager.normalize_entity(entity)
    with pytest.raises(PrimaryKeyAttributeNotDefinedException):
        manager.validate_entity(entity)


def test_activity_validation_fail_1(specs_path):
    demo_path = "/demo/path"
    manager = SpecificationManager()
    manager.load_specification_file(specs_path)

    activity = Activity("Specifying Simulation Experiment")
    with pytest.raises(InvalidActivityException):
        manager.validate_activity(activity)


def test_activity_validation_fail_2(specs_path):
    demo_path = "/demo/path"
    manager = SpecificationManager()
    manager.load_specification_file(specs_path)

    activity = Activity("Specifying Simulation Experiment")
    used_entities = []
    generated_entities = []

    fail_entity = Entity("Fooo")
    used_entities.append(fail_entity)
    activity.used_entities = used_entities
    with pytest.raises(InvalidActivityException):
        manager.validate_activity(activity)


def test_activity_validation_fail_3(specs_path):
    manager = SpecificationManager()
    manager.load_specification_file(specs_path)

    activity = Activity("Specifying Simulation Experiment")
    used_entities = []
    generated_entities = []

    fail_entity = Entity("Fooo")
    generated_entities.append(fail_entity)
    activity.generated_entities = generated_entities

    with pytest.raises(InvalidActivityException):
        manager.validate_activity(activity)


def test_activity_validation_fail_4(specs_path):
    manager = SpecificationManager()
    manager.load_specification_file(specs_path)

    activity = Activity("Specifying Simulation Experiment")

    e1 = Entity("Simulation Experiment")
    e2 = Entity("Simulation Experiment")
    e3 = Entity("Simulation Experiment")
    activity.generated_entities = [e1, e2]
    activity.used_entities.append(e3)

    with pytest.raises(InvalidActivityException):
        manager.validate_activity(activity)


def test_activity_validation_fail_6(specs_path):
    manager = SpecificationManager()
    manager.load_specification_file(specs_path)

    activity = Activity("Specifying Simulation Experiment")

    e1 = Entity("Simulation Experiment")
    e2 = Entity("Simulation Experiment")
    e3 = Entity("Simulation Experiment")
    activity.used_entities = [e1, e2]
    activity.generated_entities.append(e3)

    with pytest.raises(InvalidActivityException):
        manager.validate_activity(activity)


def test_entity_name_parsing():
    manager = SpecificationManager()
    assert ("Foo", OccurenceModifier.SINGLE) == manager._parse_entity_name("Foo")
    assert ("Foo", OccurenceModifier.ONE_OR_MORE) == manager._parse_entity_name("Foo+")
    assert ("Foo+", OccurenceModifier.ONE_OR_MORE) == manager._parse_entity_name("Foo++")
    assert ("Foo", OccurenceModifier.ZERO_OR_ONE) == manager._parse_entity_name("Foo?")
    assert ("Foo", OccurenceModifier.ZERO_OR_MORE) == manager._parse_entity_name("Foo*")

def test_real_specs_parsing(real_specs_path):
    manager = SpecificationManager()
    manager.load_specification_file(real_specs_path)

