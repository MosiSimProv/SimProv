from simprov import *


@rule("Experiment Specified")
def process_experiment_specified_event(event):
    activity = Activity("Specifying Simulation Experiment")
    used_entities = []
    generated_entities = []

    out_question = Entity("Simulation Experiment")
    out_question.attributes["File Path"] = event["filePath"]
    generated_entities.append(out_question)

    if not event["newlySpecified"]:
        in_question = Entity("Simulation Experiment")
        in_question.attributes["File Path"] = event["filePath"]
        used_entities.append(in_question)

    activity.generated_entities = generated_entities
    activity.used_entities = used_entities
    return activity


@rule("Research Question Specified")
def process_research_question_specified_event(event):
    activity = Activity("Specifying Research Question")
    used_entities = []
    generated_entities = []

    out_question = Entity("Research Question")
    out_question.attributes["File Path"] = event["filePath"]
    generated_entities.append(out_question)

    if not event["newlySpecified"]:
        in_question = Entity("Research Question")
        in_question.attributes["File Path"] = event["filePath"]
        used_entities.append(in_question)

    activity.generated_entities = generated_entities
    activity.used_entities = used_entities
    return activity


@rule("Assumption Specified")
def process_assumption_specified_event(event):
    activity = Activity("Specifying Assumption")
    used_entities = []
    generated_entities = []

    out_question = Entity("Assumption")
    out_question.attributes["File Path"] = event["filePath"]
    generated_entities.append(out_question)

    if not event["newlySpecified"]:
        in_question = Entity("Assumption")
        in_question.attributes["File Path"] = event["filePath"]
        used_entities.append(in_question)

    activity.generated_entities = generated_entities
    activity.used_entities = used_entities
    return activity


@rule("Requirement Specified")
def process_requirement_specified_event(event):
    activity = Activity("Specifying Requirement")
    used_entities = []
    generated_entities = []

    out_question = Entity("Requirement")
    out_question.attributes["File Path"] = event["filePath"]
    generated_entities.append(out_question)

    if not event["newlySpecified"]:
        in_question = Entity("Requirement")
        in_question.attributes["File Path"] = event["filePath"]
        used_entities.append(in_question)

    activity.generated_entities = generated_entities
    activity.used_entities = used_entities
    return activity


@rule("Reference Specified")
def process_reference_specified_event(event):
    activity = Activity("Specifying Reference")
    used_entities = []
    generated_entities = []

    out_question = Entity("Reference")
    out_question.attributes["File Path"] = event["filePath"]
    generated_entities.append(out_question)

    if not event["newlySpecified"]:
        in_question = Entity("Reference")
        in_question.attributes["File Path"] = event["filePath"]
        used_entities.append(in_question)

    activity.generated_entities = generated_entities
    activity.used_entities = used_entities
    return activity


@rule("Model Specified")
def process_model_specified_event(event):
    activity = Activity("Specifying Simulation Model")
    used_entities = []
    generated_entities = []

    out_question = Entity("Simulation Model")
    out_question.attributes["File Path"] = event["filePath"]
    generated_entities.append(out_question)

    if not event["newlySpecified"]:
        in_question = Entity("Simulation Model")
        in_question.attributes["File Path"] = event["filePath"]
        used_entities.append(in_question)

    activity.generated_entities = generated_entities
    activity.used_entities = used_entities
    return activity

@rule('Invalid Result Event')
def invalud_result_rule(event):
    return 42
