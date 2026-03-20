"""Tests for configuration management."""

from pathlib import Path
from unittest.mock import patch

import pytest

from climber.config import Config, get_config


class TestConfig:

    @patch('pathlib.Path.mkdir')
    @patch('climber.config.Path.home')
    def test_init(self, mock_home, mock_mkdir):
        """Test Config initialization."""
        mock_home.return_value = Path("/fake/home")

        with patch.object(Config, '_load_config'):
            config = Config()

        assert config.config_dir == Path("/fake/home/.config/climber")
        assert config.config_file == Path("/fake/home/.config/climber/config")
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    @patch.dict('os.environ', {'CLIMBER_API_KEY': 'env-key'})
    @patch('climber.config.Path.home')
    def test_load_config_from_env(self, mock_home):
        """Test loading API key from environment variable."""
        mock_home.return_value = Path("/fake/home")

        with patch('pathlib.Path.exists', return_value=False):
            with patch('pathlib.Path.mkdir'):
                config = Config()

        assert config.api_key == 'env-key'
        assert config.provider == 'openai'

    @patch('climber.config.Path.home')
    def test_load_config_from_file(self, mock_home):
        """Test loading config from file."""
        mock_home.return_value = Path("/fake/home")

        with patch.dict('os.environ', {}, clear=True):
            with patch('pathlib.Path.exists', return_value=True):
                with patch('pathlib.Path.read_text', return_value="api_key=file-key\nprovider=anthropic"):
                    with patch('pathlib.Path.mkdir'):
                        config = Config()

        assert config.api_key == 'file-key'
        assert config.provider == 'anthropic'

    @patch('pathlib.Path.chmod')
    @patch('pathlib.Path.write_text')
    @patch('pathlib.Path.mkdir')
    @patch('climber.config.Path.home')
    def test_save_config_permissions(self, mock_home, mock_mkdir, mock_write, mock_chmod):
        """Test that config file is saved with secure permissions."""
        mock_home.return_value = Path("/fake/home")

        with patch('pathlib.Path.exists', return_value=False):
            config = Config()
            config.set_api_key('test-key')

        # Verify secure permissions were set
        mock_chmod.assert_called_with(0o600)
        mock_write.assert_called()

    @patch('pathlib.Path.chmod')
    @patch('pathlib.Path.write_text')
    @patch('pathlib.Path.mkdir')
    @patch('climber.config.Path.home')
    def test_set_api_key(self, mock_home, mock_mkdir, mock_write, mock_chmod):
        """Test setting API key."""
        mock_home.return_value = Path("/fake/home")

        with patch('pathlib.Path.exists', return_value=False):
            config = Config()
            config.set_api_key('new-key')

        assert config.api_key == 'new-key'
        mock_write.assert_called()
        mock_chmod.assert_called_with(0o600)

    @patch('pathlib.Path.chmod')
    @patch('pathlib.Path.write_text')
    @patch('pathlib.Path.mkdir')
    @patch('climber.config.Path.home')
    def test_set_provider(self, mock_home, mock_mkdir, mock_write, mock_chmod):
        """Test setting provider."""
        mock_home.return_value = Path("/fake/home")

        with patch('pathlib.Path.exists', return_value=False):
            config = Config()
            config.set_provider('anthropic')

        assert config.provider == 'anthropic'
        mock_write.assert_called()
        mock_chmod.assert_called_with(0o600)

    @patch('pathlib.Path.mkdir')
    @patch('climber.config.Path.home')
    def test_set_invalid_provider(self, mock_home, mock_mkdir):
        """Test setting invalid provider raises error."""
        mock_home.return_value = Path("/fake/home")

        with patch('pathlib.Path.exists', return_value=False):
            config = Config()

            with pytest.raises(ValueError, match="Unsupported provider"):
                config.set_provider('invalid')


def test_get_config_singleton():
    """Test that get_config returns singleton instance."""
    with patch.object(Config, '__init__', return_value=None):
        config1 = get_config()
        config2 = get_config()

        assert config1 is config2
