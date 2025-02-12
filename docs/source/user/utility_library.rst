.. _utility_library:

Exemplary Utility Library
=========================

The following is an example for a utility library allowing the modeler to send events to SimProv from a Python script:

.. code-block:: python

    import glob
    from pathlib import Path

    SIMPROV_HOST = "localhost"
    SIMPROV_PORT = 5000
    SIMPROV_SIMULATOR_COMMAND = ""


    def setup_simprov(simulator_command, host="localhost", port=5000):
        global SIMPROV_HOST
        global SIMPROV_PORT
        global SIMPROV_SIMULATOR_COMMAND
        SIMPROV_HOST = host
        SIMPROV_PORT = port
        SIMPROV_SIMULATOR_COMMAND = simulator_command


    def glob_files_in_dir(path, glob_pattern):
        return list(path.glob(glob_pattern))


    def send_event(event):
        global SIMPROV_HOST
        global SIMPROV_PORT
        url = f"http://{SIMPROV_HOST}:{SIMPROV_PORT}/capturer/process-event"
        from urllib import request
        req = request.Request(url, method="POST")
        req.add_header('Content-Type', 'application/json')
        import json
        data = json.dumps(event)
        data = data.encode()
        r = request.urlopen(req, data=data)
        r.read()


    def send_experiment_executed_event(experiment_path, data_paths):
        if not isinstance(data_paths, list):
            data_paths = [data_paths]
        paths = [str(Path(path).resolve()) for path in data_paths]
        if len(data_paths) == 1:
            path_contents = {}
        else:
            path_contents = {path: open(path, "r").read() for path in paths}
        event = {"type": "Executing Simulation Experiment",
                 "experiment_path": str(experiment_path),
                 "data_paths": paths,
                 "path_contents": path_contents}
        send_event(event)

.. note::

    This library is just a proof of concept.
    The library was to be used with the corresponding rules and provenance pattern.
    The rules and patterns can be found as part of this artifact: ????


.. todo::

    Add the link above.