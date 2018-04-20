import importlib.util
from .settings import ACTION_RECOGNITION_PATH, OBJECT_DETECTION_PATH

object_detection_spec = importlib.util.spec_from_file_location("object_detection", OBJECT_DETECTION_PATH)
object_detection = importlib.util.module_from_spec(object_detection_spec)

action_recognition_spec = importlib.util.spec_from_file_location("action_recognition", ACTION_RECOGNITION_PATH)
action_recognition = importlib.util.module_from_spec(action_recognition_spec)