import json
import hashlib
import os
import mempool

# Define constants
DIFFICULTY_TARGET = "0000ffff00000000000000000000000000000000000000000000000000000000"
MINING_REWARD = 10  # Reward for mining a block


def read_transactions_from_mempool():
    transactions = []
    mempool_folder = "mempool"
    for filename in os.listdir(mempool_folder):
        with open(os.path.join(mempool_folder, filename), "r") as file:
            transaction_data = json.load(file)
            transactions.append(transaction_data)
    return transactions


def validate_transaction(transaction):
    # Check if transaction structure is valid
    if "vin" not in transaction or "vout" not in transaction:
        return False

    # Check if vin and vout are non-empty
    if not transaction["vin"] or not transaction["vout"]:
        return False

    # Perform additional validation checks
    # For example, you can check if inputs are properly formatted and valid
    for vin in transaction["vin"]:
        if "txid" not in vin or "vout" not in vin:
            return False
        # Add further validation logic as needed

    # Check if outputs are properly formatted and non-negative
    for vout in transaction["vout"]:
        if "scriptpubkey" not in vout or "value" not in vout:
            return False
        if vout["value"] < 0:
            return False
        # Add further validation logic as needed

    # Add more validation checks as necessary

    return True



def create_coinbase_transaction():
    coinbase_transaction = {
        "id": "coinbase",
        "vin": [],
        "vout": [{"scriptpubkey": "76a914miner_public_key", "value": MINING_REWARD}]
    }
    return coinbase_transaction


def calculate_block_hash(block_header):
    block_hash = hashlib.sha256(block_header.encode()).hexdigest()
    return block_hash


def mine_block(transactions, coinbase_transaction):
    block_header = ""
    nonce = 0

    # Include coinbase transaction in the list of transactions
    transactions.insert(0, coinbase_transaction)

    # Construct block header
    block_header += str(transactions)  # Serialize transactions
    block_header += str(nonce)

    # Mine block
    while True:
        block_hash = calculate_block_hash(block_header)
        if block_hash < DIFFICULTY_TARGET:
            break
        nonce += 1
        block_header = str(transactions) + str(nonce)

    return block_hash


def write_output(block_header, coinbase_transaction, mined_transactions):
    with open("output.txt", "w") as file:
        file.write(block_header + "\n")
        file.write(json.dumps(coinbase_transaction) + "\n")
        for transaction_id in mined_transactions:
            file.write(transaction_id + "\n")


def main():
    transactions = read_transactions_from_mempool()
    valid_transactions = [tx for tx in transactions if validate_transaction(tx)]
    coinbase_transaction = create_coinbase_transaction()
    mined_block_hash = mine_block(valid_transactions, coinbase_transaction)
    # Extract transaction IDs from valid transactions
    mined_transactions = [tx["id"] for tx in valid_transactions]
    write_output(mined_block_hash, coinbase_transaction, mined_transactions)


if __name__ == "__main__":
    main()
