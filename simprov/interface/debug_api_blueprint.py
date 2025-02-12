from flask import Blueprint, jsonify

from simprov.interface.wrapper import BlueprintWrapper


class DebugAPI(BlueprintWrapper):
    def _build_blueprint(self):
        blueprint = Blueprint("debug_api", __name__)

        # @blueprint.get("/show-graph")
        # def show_graph():
        #     self.simprov.provenance_graph.view_graph("G")
        #     self.simprov.reduced_graph.view_graph("G reduced")
        #     return ('', 204)

        @blueprint.get("/save")
        def save_state():
            self.simprov.write_study_state()
            return ('', 204)

        @blueprint.get("/demo-event")
        def demo_event():
            self.simprov.rest_api.socketio.emit("my-event-a")
            return ('', 204)

        return blueprint
