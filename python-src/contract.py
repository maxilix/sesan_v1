#!/usr/bin/python3

#from web3 import Web3
import solcx
#import sys
import time


source_folder = "../contracts-src/"


def unlock_account(i, password, time = 3600):
    #defaultAccount = w3.eth.accounts[0]
    #w3.eth.defaultAccount = defaultAccount
    #defaultAccountPassword = input("Password for " + defaultAccount + " : ")
    w3.geth.personal.unlockAccount(w3.eth.accounts[i],password,time)

def set_default_account(i):
    w3.eth.defaultAccount = w3.eth.accounts[i]



def deploy_contract(file_path, pulse_mining = False):

    compiled_sol = solcx.compile_files([source_path_file])
    contract_id, contract_interface = compiled_sol.popitem()
    tx_hash = w3.eth.contract(abi=contract_interface['abi'],bytecode=contract_interface['bin']).constructor().transact()
    print("Transaction hash : " + str(tx_hash.hex()))

    if (pulse_mining):
        w3.geth.miner.start(1)
        print("Mining started, waiting for transaction validation...")
    else:
        print("Waiting for transaction validation...")

    while True:
        try:
            address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
            break
        except:
            time.sleep(1)

    if (pulse_mining):
        w3.geth.miner.stop()
        print("Mining stopped")

    return w3.eth.contract(address=address,abi=contract_interface['abi'])


