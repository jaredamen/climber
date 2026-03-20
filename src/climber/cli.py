"""CLI interface for Climber."""

from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import get_config
from .ingest import create_ingester
from .output import create_output_formatter
from .process import ContentProcessor

console = Console()


@click.group()
@click.version_option()
def cli():
    """Climber: A knowledge digester for technical content."""
    pass


@cli.group()
def config():
    """Manage configuration settings."""
    pass


@config.command("set")
@click.option("--api-key", help="Set API key")
@click.option(
    "--provider", type=click.Choice(["openai", "anthropic"]), help="Set LLM provider"
)
def config_set(api_key: Optional[str], provider: Optional[str]):
    """Set configuration values."""
    config_obj = get_config()
    if api_key:
        config_obj.set_api_key(api_key)
        console.print("✓ API key updated", style="green")

    if provider:
        config_obj.set_provider(provider)
        console.print(f"✓ Provider set to {provider}", style="green")


@config.command("show")
def config_show():
    """Show current configuration."""
    config_obj = get_config()
    console.print(f"Provider: {config_obj.provider}")
    console.print(f"API Key: {'✓ Set' if config_obj.api_key else '✗ Not set'}")


@cli.command()
@click.argument("source")
@click.option(
    "--output",
    type=click.Choice(["briefing", "flashcards", "audio-script", "all"]),
    default="briefing",
    help="Output format",
)
@click.option(
    "--preset",
    type=click.Choice(["general", "runbook", "changelog"]),
    default="general",
    help="Content preset",
)
@click.option("--save", type=click.Path(), help="Save output to directory")
def ingest(source: str, output: str, preset: str, save: Optional[str]):
    """Ingest content from URL or file path."""
    try:
        config_obj = get_config()
        if not config_obj.api_key:
            console.print(
                "❌ No API key configured. Run: climber config set --api-key <key>",
                style="red",
            )
            raise click.Abort()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Ingest content
            task1 = progress.add_task("Ingesting content...", total=None)
            ingester = create_ingester(source)
            content = ingester.ingest()
            progress.update(task1, completed=True)

            # Process content
            task2 = progress.add_task("Processing with LLM...", total=None)
            processor = ContentProcessor(config_obj)

            outputs = []
            if output == "all":
                outputs = ["briefing", "flashcards", "audio-script"]
            else:
                outputs = [output]

            results = {}
            for output_type in outputs:
                result = processor.process(content, output_type, preset)
                results[output_type] = result

            progress.update(task2, completed=True)

            # Format and display/save output
            task3 = progress.add_task("Formatting output...", total=None)
            for output_type, result in results.items():
                formatter = create_output_formatter(output_type)
                formatted = formatter.format(result)

                if save:
                    save_path = Path(save)
                    save_path.mkdir(parents=True, exist_ok=True)
                    filename = f"{output_type}.{formatter.file_extension}"
                    output_file = save_path / filename
                    output_file.write_text(formatted)
                    console.print(
                        f"✓ Saved {output_type} to {output_file}", style="green"
                    )
                else:
                    console.print(f"\n[bold]{output_type.upper()}:[/bold]")
                    console.print(formatted)
                    console.print()

            progress.update(task3, completed=True)

    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort() from e


def main():
    """Entry point for CLI."""
    cli()


if __name__ == "__main__":
    main()
