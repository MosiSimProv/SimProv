import json
import traceback

from flask import Blueprint, request

from simprov.interface.wrapper import BlueprintWrapper


class CapturerAPI(BlueprintWrapper):
    def _build_blueprint(self):
        blueprint = Blueprint("capturer_api", __name__)

        @blueprint.post("/process-event")
        def process_event():
            try:
                event_json = request.get_json()
                if (isinstance(event_json, str)):
                    event_json = json.loads(event_json)
                self.simprov.process_event(event_json)
            except Exception as ex:
                traceback.print_exc()
                return ('', 404)

            return ('', 204)

        return blueprint
