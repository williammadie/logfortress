class UserInterfaceUtils:
    _status_emojis = {
        "created": "🌟",
        "running": "🚀",
        "paused": "⏸️",
        "deleted": "❌",
        "stopped": "⏹️"
    }

    @staticmethod
    def get_status_emoji(status: str) -> str:
        """Return the emoji corresponding to the container status."""
        return UserInterfaceUtils._status_emojis.get(status.lower(), "Unknown status")
