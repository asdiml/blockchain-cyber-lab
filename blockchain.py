import hashlib
import time
from dataclasses import dataclass
import copy

@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float


@dataclass
class Block:
    index: int
    transactions: list[Transaction]
    proof: int
    previous_hash: str


class Blockchain:
    def __init__(self, address, difficulty_number, mining_reward):
        self.address = address
        self.difficulty_number = difficulty_number
        self.mining_reward = mining_reward
        self.chain = []
        self.current_transactions = []

        # Create first block
        first_block = self.create_block(1, [], 0, "0")
        while not self.check_proof(first_block):
            first_block.proof += 1
        self.chain.append(first_block)

    def create_block(self, index, transactions, proof, previous_hash):
        return Block(index, copy.copy(transactions), proof, previous_hash)

    def create_transaction(self, sender, recipient, amount):
        return Transaction(sender, recipient, amount)

    def get_transactions(self):
        return self.current_transactions

    def current_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append(Transaction(sender, recipient, amount))

    def next_index(self):
        return len(self.chain) + 1

    def get_length(self):
        return len(self.chain)

    def add_block(self, block):
        if self.check_proof(block):
            self.chain.append(block)

    def hash_block(self, block):
        return hashlib.sha256(str(block).encode()).hexdigest()

    def check_proof(self, block):
        # Check that the hash of the block ends in difficulty_number many zeros
        block_hash = self.hash_block(block)
        for i in range(1, self.difficulty_number + 1):
            if block_hash[-i] != '0':
                return False
        return True

    def mine(self):
        # Give yourself a reward at the beginning of the transactions
        self.add_transaction("NULL", self.address, 10)

        # Find the right value for proof
        guess = 0
        while True:
            block = self.create_block(self.next_index(), self.current_transactions, guess, self.hash_block(self.current_block()))
            if(self.check_proof(block)):
                self.add_block(block)
                break
            guess+=1
        # Add the block to the chain
        # Clear your current transactions
        self.current_transactions = []
