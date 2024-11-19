# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2023 Eternis


# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
import numpy as np
from typing import List
import bittensor as bt

from template.validator.lean_tools import check_lean_proof, make_lean_program


def reward(query: str, response: str) -> float:
    """
    Reward the miner response to the dummy request. This method returns a reward
    value for the miner, which is used to update the miner's score.

    Returns:
    - float: The reward value for the miner.
    """

    lean_program = make_lean_program(proposition=query, proof=response)
    compilation = check_lean_proof(lean_program)
    reward = 1.0 if compilation.success else 0.0

    bt.logging.info(
        f"In rewards, query val: {query}, response val: {response}, rewards val: {reward}"
    )
    return reward


def get_rewards(
    self,
    query: str,
    responses: List[str],
) -> np.ndarray:
    """
    Returns an array of rewards for the given query and responses.

    Args:
    - query (str): The query sent to the miner.
    - responses (List[str]): A list of responses from the miner.

    Returns:
    - np.ndarray: An array of rewards for the given query and responses.
    """
    # Get all the reward results by iteratively calling your reward() function.

    return np.array([reward(query, response) for response in responses])
