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

import time
import bittensor as bt

from template.protocol import Dummy
from template.validator.reward import get_rewards
from template.utils.uids import get_random_uids
from template.validator.lean_tools import make_lean_query


async def forward(self):
    """
    The forward function is called by the validator every time step.

    It is responsible for querying the network and scoring the responses.

    Args:
        self (:obj:`bittensor.neuron.Neuron`): The neuron object which contains all the necessary state for the validator.

    """
    bt.logging.info("Starting validator forward pass...")
    
    miner_uids = get_random_uids(self, k=self.config.neuron.sample_size)
    bt.logging.info(f"Selected miner UIDs: {miner_uids}")
    for uid in miner_uids:
        axon = self.metagraph.axons[uid]
        bt.logging.info(f"Miner {uid}:")
        bt.logging.info(f"  Hotkey: {self.metagraph.hotkeys[uid]}")
        bt.logging.info(f"  Axon: {axon}")
    
    query = make_lean_query(self.step)
    bt.logging.info(f"Query: {query}")

    try:
        responses = await self.dendrite(
            axons=[self.metagraph.axons[uid] for uid in miner_uids],
            synapse=Dummy(dummy_input=query),
            deserialize=True,
        )
        for uid, response in zip(miner_uids, responses):
            bt.logging.info(f"Miner {uid} response: {response}")
    except Exception as e:
        bt.logging.error(f"Error: {str(e)}")

    # Adjust the scores based on responses from miners.
    rewards = get_rewards(self, query=query, responses=responses)

    bt.logging.info(f"Scored responses: {rewards}")
    # Update the scores based on the rewards. You may want to define your own update_scores function for custom behavior.
    self.update_scores(rewards, miner_uids)
    time.sleep(5)
