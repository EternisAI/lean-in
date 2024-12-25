import typer
import subprocess
import os

app = typer.Typer()

@app.command()
def run(
    role: str = typer.Option(..., "--role", help="Choose validator or miner"),
    wallet_name: str = typer.Option(None, "--wallet.name", help="Wallet name (defaults to role)"),
    wallet_hotkey: str = typer.Option("default", "--wallet.hotkey", help="Hotkey name (defaults to 'default')"),
    wallet_path: str = typer.Option(
        os.path.normpath(os.path.expanduser("~/.bittensor/wallets")),
        "--wallet.path",
        help="Path to wallet directory"
    ),
) -> None:
    """Run a neuron (validator or miner) with the specified configuration."""
    if role not in ["validator", "miner"]:
        typer.echo(f"Invalid role: {role}")
        raise typer.Exit(1)
    
    cmd = [
        "pdm", "run", f"neurons/{role}.py",
        "--netuid", "63",
        "--logging.debug",
        "--wallet.name", wallet_name or role,
        "--wallet.hotkey", wallet_hotkey,
        "--wallet.path", wallet_path,
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    app()
