from blockchain import Blockchain
from ecdsa import SigningKey

def main():
    # Initialize Blockchain
    blockchain = Blockchain()

    # Create a private and public key for digital signatures
    sk = SigningKey.generate(curve=SECP256k1)
    private_key = sk.to_string()
    public_key = sk.get_verifying_key()

    # Add some certificates (transactions)
    blockchain.new_transaction(
        sender="UniversityXYZ",
        recipient="Student123",
        certificate_data="Bachelor's Degree Certificate"
    )

    # Perform Proof of Work to add block to chain
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Add the new block to the blockchain
    blockchain.new_block(proof)

    # Sign the certificate data
    certificate_data = "Bachelor's Degree Certificate"
    signature = blockchain.digital_signature(private_key, certificate_data)
    
    # Verify the signature
    is_verified = blockchain.verify_signature(public_key, signature, certificate_data)
    print(f"Certificate verified: {is_verified}")

if __name__ == "__main__":
    main()
