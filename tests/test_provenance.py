from simprov.core import SimProv

from simprov.provenance import Activity, Entity


def build_specifying_simulation_experiment_activity(was_created=True):
    demo_path = "/tmp/experiment.py"
    activity = Activity("Specifying Simulation Experiment")
    if not was_created:
        used_experiment = Entity("Simulation Experiment")
        used_experiment.attributes["File Path"] = demo_path
        activity.used_entities.append(used_experiment)
    generated_experiment = Entity("Simulation Experiment")
    generated_experiment.attributes["File Path"] = demo_path
    activity.generated_entities.append(generated_experiment)
    return activity


def build_specifying_simulation_model_activity(was_created=True):
    demo_path = "/tmp/model.mlr"
    activity = Activity("Specifying Simulation Model")
    if not was_created:
        used_model = Entity("Simulation Model")
        used_model.attributes["File Path"] = demo_path
        activity.used_entities.append(used_model)
    generated_model = Entity("Simulation Model")
    generated_model.attributes["File Path"] = demo_path
    activity.generated_entities.append(generated_model)
    return activity


def test_provenance_graph_chaining(real_rules_path, specs_path):
    simprov = SimProv(real_rules_path, specs_path,start_api=False)
    activity = build_specifying_simulation_experiment_activity(was_created=True)
    simprov.specification_manager.normalize_activity(activity)
    simprov.provenance_graph.chain_provenance_activity(activity)
    assert activity in simprov.provenance_graph.activities
    assert len(simprov.provenance_graph.activities) == 1
    assert activity.id in simprov.provenance_graph.node_map
    for entity in activity.entities:
        assert entity in simprov.provenance_graph.entities
        assert entity.id in simprov.provenance_graph.node_map
        assert entity.id in simprov.provenance_graph.graph.nodes
    for used_entity in activity.used_entities:
        assert (activity.id, used_entity.id) in simprov.provenance_graph.graph.edges
    for generated_entity in activity.generated_entities:
        assert (generated_entity.id, activity.id) in simprov.provenance_graph.graph.edges
    assert len(simprov.provenance_graph.entities) == 1
    simprov.delete_study_state()


def test_provenance_graph_chaining_2(real_rules_path, specs_path):
    simprov = SimProv(real_rules_path, specs_path,start_api=False)
    activity_1 = build_specifying_simulation_experiment_activity()
    simprov.specification_manager.normalize_activity(activity_1)

    activity_2 = build_specifying_simulation_experiment_activity(was_created=False)
    simprov.specification_manager.normalize_activity(activity_2)

    simprov.provenance_graph.chain_provenance_activity(activity_1)
    simprov.provenance_graph.chain_provenance_activity(activity_2)
    assert activity_1 in simprov.provenance_graph.activities
    assert activity_2 in simprov.provenance_graph.activities
    assert activity_1.id in simprov.provenance_graph.node_map
    assert activity_2.id in simprov.provenance_graph.node_map

    for entity in activity_1.entities:
        assert entity in simprov.provenance_graph.entities
        assert entity.id in simprov.provenance_graph.node_map
        assert simprov.provenance_graph.last_entities_map[entity.primary_key] != entity
    for used_entity in activity_1.used_entities:
        assert (activity_1.id, used_entity.id) in simprov.provenance_graph.graph.edges
    for generated_entity in activity_1.generated_entities:
        assert (generated_entity.id, activity_1.id) in simprov.provenance_graph.graph.edges

    for entity in activity_2.entities:
        assert entity in simprov.provenance_graph.entities
        assert entity.id in simprov.provenance_graph.node_map
    for used_entity in activity_2.used_entities:
        assert (activity_2.id, used_entity.id) in simprov.provenance_graph.graph.edges
        assert simprov.provenance_graph.last_entities_map[used_entity.primary_key] != used_entity
    for generated_entity in activity_2.generated_entities:
        assert (generated_entity.id, activity_2.id) in simprov.provenance_graph.graph.edges
        assert simprov.provenance_graph.last_entities_map[generated_entity.primary_key] == generated_entity
    simprov.delete_study_state()


def test_provenance_graph_chaining_complex(real_rules_path, specs_path):
    ## Setup
    simprov = SimProv(real_rules_path, specs_path,start_api=False)
    creating_experiment_activity = build_specifying_simulation_experiment_activity()
    specifying_experiment_activity = build_specifying_simulation_experiment_activity(was_created=False)
    creating_model_activity = build_specifying_simulation_model_activity()
    specifying_model_activity = build_specifying_simulation_model_activity(was_created=False)

    data_entity = Entity("Data")
    data_entity.attributes["File Path"] = "/tmp/demo.dat"
    run_experiment_activity = Activity("Run Experiment")
    run_experiment_activity.used_entities.append(specifying_model_activity.generated_entities[0])
    run_experiment_activity.used_entities.append(specifying_experiment_activity.generated_entities[0])
    run_experiment_activity.generated_entities.append(data_entity)

    activities = [creating_experiment_activity, specifying_experiment_activity, creating_model_activity,
                  specifying_model_activity, run_experiment_activity]
    for activity in activities:
        simprov.specification_manager.normalize_activity(activity)
        simprov.specification_manager.validate_activity(activity)
        simprov.provenance_graph.chain_provenance_activity(activity)

    for activity in activities:
        assert activity in simprov.provenance_graph.activities
        for entity in activity.entities:
            assert entity in simprov.provenance_graph.entities
        for used_entity in activity.used_entities:
            assert (activity.id, used_entity.id) in simprov.provenance_graph.graph.edges
        for generated_entity in activity.generated_entities:
            assert (generated_entity.id, activity.id) in simprov.provenance_graph.graph.edges
    recent_entities = [specifying_model_activity.generated_entities[0],
                       specifying_experiment_activity.generated_entities[0],
                       run_experiment_activity.generated_entities[0]]
    for recent_entity in recent_entities:
        assert simprov.provenance_graph.last_entities_map[recent_entity.primary_key] == recent_entity
    simprov.delete_study_state()
