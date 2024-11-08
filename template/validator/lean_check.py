import subprocess
from pathlib import Path
from os import environ
from dataclasses import dataclass

CACHE_DIR = Path(__file__).parent / "lean_cache"

LAKEFILE_TEMPLATE = """
import Lake
open Lake DSL
package «temp-project»
"""

@dataclass
class CompilationResult:
    success: bool
    error_message: str = ""

def ensure_directory_exists(path: Path) -> None:
    path.mkdir(exist_ok=True, parents=True)

def create_lakefile(directory: Path) -> None:
    for f in ['lakefile.lean', 'lakefile.toml']:
        lakefile = directory / f
        if lakefile.exists():
            lakefile.unlink()
            
    (directory / 'lakefile.lean').write_text(LAKEFILE_TEMPLATE)

def write_program(directory: Path, program: str) -> None:
    (directory / 'Main.lean').write_text(program)

def run_command(cmd: list[str], directory: Path, description: str = "") -> tuple[bool, str]:    
    elan_path = Path.home() / ".elan" / "bin"
    env = environ.copy()
    env["PATH"] = f"{elan_path}:{env.get('PATH', '')}"
        
    result = subprocess.run(
        cmd,
        cwd=directory,
        capture_output=True,
        text=True,
        env=env
    )
    error_msg = ""
    if result.returncode != 0:
        error_msg = f"Error:\n{result.stderr}"
        if result.stdout:
            error_msg += f"\nOutput:\n{result.stdout}"
    return result.returncode == 0, error_msg

def initialize_if_needed() -> tuple[bool, str]:
    try:
        if not CACHE_DIR.exists():
            ensure_directory_exists(CACHE_DIR)
            create_lakefile(CACHE_DIR)
            
            success, error = run_command(
                ['lake', 'update'], 
                CACHE_DIR, 
                "Fetching dependencies (first time setup)"
            )
            if not success:
                return False, error
        else:
            current_lakefile = (CACHE_DIR / 'lakefile.lean').read_text()
            if current_lakefile.strip() != LAKEFILE_TEMPLATE.strip():
                print("Updating lakefile...")
                create_lakefile(CACHE_DIR)
                success, error = run_command(
                    ['lake', 'update'],
                    CACHE_DIR,
                    "Updating dependencies"
                )
                if not success:
                    return False, error
                    
        return True, ""
    except Exception as e:
        return False, str(e)

def check_lean_proof(program: str) -> CompilationResult:
    success, error_msg = initialize_if_needed()
    if not success:
        return CompilationResult(False, error_msg)

    write_program(CACHE_DIR, program)
    
    success, error_msg = run_command(
        ['lean', 'Main.lean'], 
        CACHE_DIR, 
        "Verifying proof"
    )

    return CompilationResult(success, error_msg)
