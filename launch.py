import typer
import subprocess


app = typer.Typer()

@app.command()
def run(
    role: str = typer.Option(..., "--role", help="Choose validator or miner"),
    wallet_name: str = typer.Option(..., "--wallet.name"),
    wallet_hotkey: str = typer.Option("default", "--wallet.hotkey"),
) -> None:
    cmd = [
        "pdm", "run", f"neurons/{role}.py",
        "--subtensor.network", "test",
        "--netuid", "242",
        "--logging.debug",
        "--wallet.name", wallet_name,
        "--wallet.hotkey", wallet_hotkey
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    app()
