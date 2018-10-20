import json
import web3

from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract

# transform the string literals to bytes in order to pass it to solidity
candidates = [b'Team 1', b'Team 2', b'Team 3']

# Solidity source code
contract_source_code = open('Voting.sol','r').read().replace('\n',' ')

compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:Voting']

# web3.py instance
w3 = Web3(HTTPProvider("http://127.0.0.1:8545"))

# Instantiate and deploy contract
contract = w3.eth.contract(
	abi=contract_interface['abi'],
	bytecode=contract_interface['bin']
)

# Get transaction hash from deployed contract

# If constructor has arguments
tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 410000, value=1.0}, args=[candidates])

# Get tx receipt to get contract address
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']

# Contract instance in concise mode
abi = contract_interface['abi']
contract_instance = w3.eth.contract(address=contract_address, abi=abi,ContractFactoryClass=ConciseContract)

#################### examples of calling the functions in the contract
#contract_instance.voteForCandidate(b'Team 1', transact={'from': w3.eth.accounts[0]})
#contract_instance.voteForCandidate(b'Team 1', transact={'from': w3.eth.accounts[0]})
#contract_instance.voteForCandidate(b'Team 1', transact={'from': w3.eth.accounts[0]})

#print('Votes for Team 1 = {}'.format(contract_instance.totalVotesFor(b"Team 1")))

#print("Before = " + w3.eth.getBalance(w3.eth.accounts[0]))
#contract_instance.voteForCandidate(b'Team 1', transact={'from': w3.eth.accounts[0]})
#print("After = " + w3.eth.getBalance(w3.eth.accounts[0]))

#print(web3.eth_gasPrice)