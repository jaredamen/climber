"""Tests for CLI interface."""

from unittest.mock import Mock, patch

from click.testing import CliRunner

from climber.cli import cli, config_set, ingest


class TestCLI:

    def test_cli_version(self):
        """Test CLI version command."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert "version" in result.output or "1.0.0" in result.output

    def test_cli_help(self):
        """Test CLI help command."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "knowledge digester" in result.output.lower()

    @patch('climber.cli.get_config')
    def test_config_set_api_key(self, mock_get_config):
        """Test setting API key through CLI."""
        mock_config = Mock()
        mock_get_config.return_value = mock_config

        runner = CliRunner()
        result = runner.invoke(config_set, ['--api-key', 'test-key-123'])

        assert result.exit_code == 0
        mock_config.set_api_key.assert_called_once_with('test-key-123')
        assert "API key updated" in result.output

    @patch('climber.cli.get_config')
    def test_config_set_provider(self, mock_get_config):
        """Test setting provider through CLI."""
        mock_config = Mock()
        mock_get_config.return_value = mock_config

        runner = CliRunner()
        result = runner.invoke(config_set, ['--provider', 'anthropic'])

        assert result.exit_code == 0
        mock_config.set_provider.assert_called_once_with('anthropic')
        assert "Provider set to anthropic" in result.output

    @patch('climber.cli.get_config')
    def test_config_show(self, mock_get_config):
        """Test showing configuration."""
        mock_config = Mock()
        mock_config.provider = "openai"
        mock_config.api_key = "test-key"
        mock_get_config.return_value = mock_config

        runner = CliRunner()
        result = runner.invoke(cli, ['config', 'show'])

        assert result.exit_code == 0
        assert "openai" in result.output
        assert "✓ Set" in result.output

    @patch('climber.cli.create_output_formatter')
    @patch('climber.cli.ContentProcessor')
    @patch('climber.cli.create_ingester')
    @patch('climber.cli.get_config')
    def test_ingest_no_api_key(self, mock_get_config, mock_create_ingester,
                              mock_processor, mock_formatter):
        """Test ingest command without API key."""
        mock_config = Mock()
        mock_config.api_key = None
        mock_get_config.return_value = mock_config

        runner = CliRunner()
        result = runner.invoke(ingest, ['https://example.com'])

        assert result.exit_code == 1
        assert "No API key configured" in result.output

    @patch('climber.cli.create_output_formatter')
    @patch('climber.cli.ContentProcessor')
    @patch('climber.cli.create_ingester')
    @patch('climber.cli.get_config')
    def test_ingest_success(self, mock_get_config, mock_create_ingester,
                           mock_processor_class, mock_formatter):
        """Test successful ingest command."""
        # Mock config
        mock_config = Mock()
        mock_config.api_key = "test-key"
        mock_get_config.return_value = mock_config

        # Mock ingester
        mock_ingester = Mock()
        mock_content = Mock(text="test content", title="Test", source="test")
        mock_ingester.ingest.return_value = mock_content
        mock_create_ingester.return_value = mock_ingester

        # Mock processor
        mock_processor = Mock()
        mock_processor.process.return_value = {
            "content": "processed content",
            "title": "Test",
            "source": "test"
        }
        mock_processor_class.return_value = mock_processor

        # Mock formatter
        mock_formatter_instance = Mock()
        mock_formatter_instance.format.return_value = "formatted output"
        mock_formatter_instance.file_extension = "md"
        mock_formatter.return_value = mock_formatter_instance

        runner = CliRunner()
        result = runner.invoke(ingest, ['https://example.com', '--output', 'briefing'])

        assert result.exit_code == 0
        mock_ingester.ingest.assert_called_once()
        mock_processor.process.assert_called_once_with(mock_content, "briefing", "general")

    def test_ingest_invalid_output(self):
        """Test ingest command with invalid output type."""
        runner = CliRunner()
        result = runner.invoke(ingest, ['https://example.com', '--output', 'invalid'])

        assert result.exit_code != 0
        assert "Invalid value" in result.output

    def test_ingest_invalid_preset(self):
        """Test ingest command with invalid preset."""
        runner = CliRunner()
        result = runner.invoke(ingest, ['https://example.com', '--preset', 'invalid'])

        assert result.exit_code != 0
        assert "Invalid value" in result.output
