# LEAN INtro and Overview

## Proof Assistants

[LEAN](https://leanprover-community.github.io/) is a proof assistant, i.e. a programming language in which one can write **proofs** for **statements**, and then use its compiler to verify that the proof is valid for the given statement. For example, we might want a proof of a statement like “adding zero to any natural number gives you that number back”. Just as in any other programming language, we would need to convert this natural language—-henceforth “classical”—-statement into LEAN syntax—-this conversion process is called **formalization**. For this example, that would be the following.

```haskell
theorem add_zero (n : Nat) : n + 0 = n
```

Breaking this down piece by piece 

- `theorem` is a LEAN keyword for a statement, just like `def` is a Python keyword for a function
- `add_zero` is the name we are giving to this statement
- `(n : Nat)` says we are given a natural number `n`
- `n + 0 = n` is the statement that `n` satisfies this property we want to show

A **proof** of a statement is an argument justifying its truth. In this case, the proof uses induction; i.e. one shows that both of the following sub-statements are true, which together prove that the full statement is true.

- `0 + 0 = 0`
- if `n + 0 = n` then `(n+1) + 0 = (n+1)`

This proof can also be formalized—-in many distinct but often equivalent ways!—-in LEAN, like so.

```haskell
theorem add_zero (n : Nat) : add n zero = n :=
  by induction n with
  | zero => rfl
  | succ n ih => 
    simp [add]
    rw [ih]
```

The syntax is `statement := proof` so in the above, what comes before the `:=` is our statement, and what comers after it is the proof that justifies it. This formal proof looks pretty similar to our classical proof above:

- we use induction, which is introduced at the top formally as `by induction n with`
- we consider the case for the base case, applying the statement to `0` via `| zero`
- we consider the inductive case, applying the statement to `n+1` via `| succ n`
    - assuming it holds for `n` via the `ih` (inductive hypothesis) keyword

What follows after the two `=>` symbols is a call to LEAN's [tactics](https://leanprover.github.io/theorem_proving_in_lean4/tactics.html), which we won't go over here. The magic of proof assistants is that one can simply run the LEAN compiler on the above block of code and have it tell us whether the proof justifies the statement! So running it on the above would (essentially) return `true`, while running it on an incorrect proof would return `false`.

## LEAN IN Bittensor Subnet

The LEAN IN Bittensor subnet has behaviors for both **validators** and **miners**. Roughly the order of operations is:

1. The validators make a **query** in the form of a random LEAN statement*
2. The miners give a **response** in the form of a LEAN proof that claims to justify this statement
3. The validator assigns a constant **reward** to the miners which submitted a correct proof---this is done by running the LEAN compiler on `query := response`

*At the moment, we start with simple LEAN statements like `a+b=c`, but will expand to a larger set of claims.

# How to Run

1. Set up your wallet and keys on your machine.
2. Build the container
```bash
docker build -t leanin .
```
3. Run as `role=` `validator` or `miner`
```bash
docker run -it \
    -v <your local wallet path>:/root/.bittensor/wallets \
    leanin \
    --role <role> \
    --wallet.name <name> \
    --wallet.hotkey <hotkey>
```

In particular, before running the miner node, one must add mining logic, e.g. an LLM prompting loop with working API key, to the function `generate_proof` in `neurons/miner.py`.
