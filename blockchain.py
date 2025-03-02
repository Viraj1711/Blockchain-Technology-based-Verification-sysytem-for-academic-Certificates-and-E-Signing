import hashlib
import time
import json
from ecdsa import SigningKey, SECP256k1


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block and add it to the chain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) Hash of previous block
        :return: New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    @staticmethod
    def hash(block):
        """
        Hash a Block
        :param block: Block
        :return: String of the block's hash
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def new_transaction(self, sender, recipient, certificate_data):
        """
        Creates a new transaction to be added to the next mined block
        :param sender: Address of the sender
        :param recipient: Address of the recipient
        :param certificate_data: Certificate data to be verified
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'certificate_data': certificate_data,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
        - Find a number p' such that hash(pp') contains 4 leading zeros, where p is the previous proof, and p' is the new proof
        :param last_proof: Previous proof
        :return: New proof
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeros?
        :param last_proof: Previous proof
        :param proof: Current proof
        :return: True if valid, False otherwise
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def digital_signature(self, private_key, message):
        """
        Generates a digital signature for the certificate data
        :param private_key: Private key for signing the certificate
        :param message: Certificate data
        :return: Signature
        """
        sk = SigningKey.from_string(private_key, curve=SECP256k1)
        signature = sk.sign(message.encode())
        return signature

    def verify_signature(self, public_key, signature, message):
        """
        Verifies a digital signature
        :param public_key: Public key of the signer
        :param signature: Signature of the certificate
        :param message: Certificate data
        :return: True if valid, False otherwise
        """
        vk = public_key.verifying_key
        try:
            vk.verify(signature, message.encode())
            return True
        except:
            return False
