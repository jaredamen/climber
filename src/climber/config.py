"""Configuration management for Climber."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration manager for Climber."""

    def __init__(self):
        self.config_dir = Path.home() / ".config" / "climber"
        self.config_file = self.config_dir / "config"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self._api_key: Optional[str] = None
        self._provider: str = "openai"

        self._load_config()

    def _load_config(self):
        """Load configuration from file and environment."""
        # Priority: env var > config file > default
        self._api_key = os.getenv("CLIMBER_API_KEY")

        if self.config_file.exists():
            lines = self.config_file.read_text().strip().split("\n")
            for line in lines:
                if "=" in line:
                    key, value = line.split("=", 1)
                    if key == "api_key" and not self._api_key:
                        self._api_key = value
                    elif key == "provider":
                        self._provider = value

    def _save_config(self):
        """Save configuration to file."""
        lines = []
        if self._api_key:
            lines.append(f"api_key={self._api_key}")
        lines.append(f"provider={self._provider}")

        self.config_file.write_text("\n".join(lines))

        # Set secure permissions (read/write for owner only)
        self.config_file.chmod(0o600)

    @property
    def api_key(self) -> Optional[str]:
        """Get the API key."""
        return self._api_key

    @property
    def provider(self) -> str:
        """Get the LLM provider."""
        return self._provider

    def set_api_key(self, api_key: str):
        """Set the API key."""
        self._api_key = api_key
        self._save_config()

    def set_provider(self, provider: str):
        """Set the LLM provider."""
        if provider not in ["openai", "anthropic"]:
            raise ValueError(f"Unsupported provider: {provider}")
        self._provider = provider
        self._save_config()


_config_instance: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
