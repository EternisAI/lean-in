import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CompilationResult:
    success: bool
    error_message: str = ""

def check_lean_proof(program: str) -> CompilationResult:
    # Write to a temporary file
    temp_file = Path("temp.lean")
    temp_file.write_text(program)
    
    try:
        result = subprocess.run(
            ['lean', 'temp.lean'],
            capture_output=True,
            text=True
        )
        return CompilationResult(
            success=result.returncode == 0,
            error_message=result.stderr if result.returncode != 0 else ""
        )
    finally:
        temp_file.unlink(missing_ok=True)
