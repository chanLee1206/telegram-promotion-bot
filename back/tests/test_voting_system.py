import unittest
from smart_contracts.voting_system import VotingSystem

class TestVotingSystem(unittest.TestCase):
    def test_cast_vote(self):
        # Test voting functionality
        self.assertTrue(VotingSystem.cast_vote(token_address))

    def test_get_trending_tokens(self):
        # Test retrieval of trending tokens
        self.assertGreater(len(VotingSystem.get_trending_tokens(50)), 0)
