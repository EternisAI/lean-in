import random 


def make_query():
    a = random.randint(0, 1000)
    b = random.randint(0, 1000)
    return f"{a} + {b} = {a+b}"


def make_lean_program(proposition: str, proof: str) -> str:
    return f"""
theorem my_sum : {proposition} :=
    {proof}
""".strip()