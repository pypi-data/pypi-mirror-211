import torch
import bittensor as bt
import copy
import unittest
from unittest.mock import MagicMock
from openvalidators.dendrite import AsyncDendritePool

class DendriteTestCase(unittest.TestCase):
    def setUp(self):
        """
        Creates a mock metagraph with 1024 mock axons.
        """
        mock_metagraph = MagicMock(spec=bt.metagraph)
        mock_metagraph.uids = torch.tensor(range(0, 1024))
        mock_metagraph.axons = [MagicMock(
            spec=bt.axon_info,
            hotkey=str(num),
            ip='0.0.0.0/0',
            port=12345
        ) for num in range(0, 1024)]

        self.metagraph = mock_metagraph
        self.keypair = 'test'

    def test_resync_uid_change(self):
        dendrite_pool = AsyncDendritePool(keypair=self.keypair, metagraph=self.metagraph)

        # Modify the hotkey of the first axon of the metagraph
        index = 0
        modified_metagraph = copy.deepcopy(self.metagraph)
        modified_metagraph.axons[index].hotkey = 'hotkey-test'

        dendrite_pool.resync(modified_metagraph)

        dendrite_hot_keys = list(map(lambda dendrite: dendrite.axon_info.hotkey, dendrite_pool.dendrites))
        new_metagraph_hot_keys = list(map(lambda axon: axon.hotkey, modified_metagraph.axons))

        self.assertEqual(dendrite_hot_keys, new_metagraph_hot_keys)

    def test_resync_uid_add(self):
        original_metagraph = self.metagraph

        smaller_metagraph = copy.deepcopy(original_metagraph)

        # Remove the last axon from the metagraph
        smaller_metagraph.axons.pop()

        # Creates dendrite pool with smaller metagraph
        dendrite_pool = AsyncDendritePool(keypair=self.keypair, metagraph=smaller_metagraph)

        # Resync the dendrite pool with the original metagraph, that has one more axon
        dendrite_pool.resync( original_metagraph )

        assert len(dendrite_pool.dendrites) == len(original_metagraph.axons)

        dendrite_hot_keys = list(map(lambda dendrite: dendrite.axon_info.hotkey, dendrite_pool.dendrites))
        new_metagraph_hot_keys = list(map(lambda axon: axon.hotkey, original_metagraph.axons))

        self.assertEqual(dendrite_hot_keys, new_metagraph_hot_keys)

if __name__ == '__main__':
    unittest.main()