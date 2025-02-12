.. code-block:: python

	from pathlib import Path
	from simprov import Activity, Entity, rule

	# Auxilary function extracting the file name from a file path
	def file_name_from(path):
		return Path(path).name

	# Rule function for events of type "Experiment Executed"
	@rule("Experiment Executed")
	def process_experiment_executed_event(event:dict)-> Activity:
		activity = Activity("Executing Experiment")

		experiment = Entity("Experiment")
		experiment_path = event["executed_experiment"]
		experiment["File Path"] = experiment_path
		experiment["Name"] = file_name_from(experiment_path)
		experiment["Specification"] = event["experiment_specification"]

		model = Entity("Simulation Model")
		model_path = event["with_model"]
		model["File Path"] = model_path
		model["Name"] = file_name_from(model_path)
		model["Specification"] = event["model_specification"]

		data = Entity("Data")
		data_path = event["generated_data"]
		data["File Path"] = data_path
		data["Name"] = file_name_from(data_path)
		data["Content"] = event["data_content"]

		tel = Agent("Tellurium")
		tel["Version"] = event["tellurium_version"]


		activity.entities_used = [model, experiment]
		activity.entities_generated = [data]
		activity.agents_associated = [tel]

		return activity