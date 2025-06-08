import json
import os
import platform


class LogPersistence:
    """
    Class to handle persistence of custom log sources to a JSON file.
    """

    APP_FOLDER = "logfortress"

    def __init__(self) -> None:
        """
        Initialize the LogPersistence with a specified file path.

        :param file_path: The path to the JSON file used for persistence.
        """
        self.file_path = self._get_file_path()

    def _get_file_path(self) -> str:
        """Determine the file path based on the operating system."""
        if platform.system() == 'Windows':
            base_dir = os.getenv('APPDATA', os.path.expanduser('~'))
        else:
            base_dir = os.getenv(
                'XDG_CONFIG_HOME', os.path.expanduser('~/.config'))

        app_dir = os.path.join(base_dir, "logfortress")
        os.makedirs(app_dir, exist_ok=True)
        return os.path.join(app_dir, 'custom_sources.json')

    def load(self) -> dict:
        """Load custom log sources from a JSON file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding="utf8") as file:
                return json.load(file)
        return {}

    def save(self, data: dict) -> None:
        """Save custom log sources to a JSON file."""
        with open(self.file_path, 'w', encoding="utf8") as file:
            json.dump(data, file, indent=4)
