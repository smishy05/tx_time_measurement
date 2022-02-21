from web3 import Web3
import sys
import pandas as pd
import time
import os
import random

BASE_PORT = 7014
NO_OF_NODES = 5
NO_OF_ACCOUNTS_PER_NODE = 5
TOTAL_ACCS = NO_OF_NODES * NO_OF_ACCOUNTS_PER_NODE
NUMBER_OF_CYCLES = 10
TRANSACTION_BASE_SIZE = 210

def setupNode(num):
    port = BASE_PORT + num * 4
    url = 'http://127.0.0.1:' + str(port)
    w3 = Web3(Web3.HTTPProvider(url))
    return w3.geth.admin.node_info()

def setupConnection(n1, n2):
    datadir = './data'
    nodesDataFilename = datadir + '/nodesData.csv'
    df1 = pd.read_csv(nodesDataFilename)
    l1 = df1.shape[0]
    enode = ''
    for i in range(l1):
        if i == n2:
            enode = df1.iat[i, 1]
    port = 7014 + (n1+1) * 4
    url = 'http://127.0.0.1:' + str(port)
    w3 = Web3(Web3.HTTPProvider(url))
    checkConn = w3.geth.admin.add_peer(enode)
    return checkConn

def setupAccount(n1, n2):
    port = BASE_PORT + n1 * 4
    url = 'http://127.0.0.1:' + str(port)
    w3 = Web3(Web3.HTTPProvider(url))
    p = "pass-" + str(n1) + str(n2)
    a = w3.geth.personal.new_account(p)
    w3.geth.personal.unlock_account(a, p, 15000)
    # w3.geth.miner.set_ether_base(w3.eth.accounts[n2])
    w3.geth.miner.start(1)
    time.sleep(60)
    w3.geth.miner.stop()

    if n2 != 0:
        p2 = "pass-" + str(n1) + str(0)
        w3.geth.personal.unlock_account(w3.eth.accounts[0], p2, 15000)
        transaction = {
            'from': w3.eth.accounts[0],
            'to': w3.eth.accounts[n2],
            'chainId': 1000,
            'value': w3.toWei(20, 'ether')
        }
        tx_hash = w3.eth.send_transaction(transaction)

    return a, p, w3.fromWei(w3.eth.get_balance(w3.eth.accounts[n2]), 'ether')

def setup():
    datadir = './data'
    dirIsExists = os.path.isdir(datadir)
    if dirIsExists == False:
        os.mkdir(datadir)
    
    number_of_nodes = 5
    nodes_num = [(i+1) for i in range(number_of_nodes)]
    nodes = []
    enodes = []

    for n in nodes_num:
        n_info = setupNode(n)
        enode = n_info['enode']
        enode = enode.replace('[::]', '127.0.0.1')
        nodes.append('Node-' + str(n))
        enodes.append(enode)

    nodesDataFilename = datadir + '/nodesData.csv'
    dict1 = {'Node': nodes, 'Enode': enodes}
    df1 = pd.DataFrame(dict1)
    df1.to_csv(nodesDataFilename, mode='w', index=False)

    for i in range(number_of_nodes):
        for j in range(i+1, number_of_nodes):
            setupConnection(i, j)

    accounts_per_node = 5
    nodes = []
    accounts = []
    balances = []
    passwords = []
    for n in nodes_num:
        for i in range(accounts_per_node):
            a, password, balance = setupAccount(n, i)
            accounts.append(a)
            balances.append(balance)
            nodes.append(n)
            passwords.append(password)

    accountsDataFilename = datadir + '/accountsData.csv'
    dict2 = {'Account': accounts, 'Node': nodes, 'Password': passwords, 'Balance': balances}
    df2= pd.DataFrame(dict2)
    df2.to_csv(accountsDataFilename, mode='w', index=False)

def runMiner():
    port = 7034
    url = 'http://127.0.0.1:' + str(port)
    w3 = Web3(Web3.HTTPProvider(url))
    p = "pass-50"
    a = w3.geth.personal.new_account(p)
    w3.geth.personal.unlock_account(a, p)
    w3.geth.personal.unlock_account(w3.eth.accounts[0], p, 15000)
    w3.geth.miner.start(1)

def send_transactions(data):
    datadir = './data'
    accountsDataFilename = datadir + '/accountsData.csv'
    df1 = pd.read_csv(accountsDataFilename)

    receiver_nums = data['receiver_nums']
    generator_nums = data['generator_nums']
    receivers = []
    generators = []
    for r in receiver_nums:
        receivers.append(df1.iat[r, 0])
    for g in generator_nums:
        generators.append(df1.iat[g, 0])

    input_size = int(data['tx_size']) - TRANSACTION_BASE_SIZE
    input = ''
    for i in range(input_size):
        input = input + 'a'
    
    tx_count = 0
    burst_time = 0.0
    generator_accounts = []
    tx_hashes = []
    urls = []
    start_times = []
    while tx_count != int(data['tx_per_sec']):
        generator_index = random.randint(0, len(generator_nums)-1)
        generator_num = generator_nums[generator_index]
        generator = generators[generator_index]
        p = df1.iat[generator_num, 2]
        port = BASE_PORT + (int((generator_num)/5)+1) * 4
        url = 'http://127.0.0.1:' + str(port)
        w3 = Web3(Web3.HTTPProvider(url))
        w3.geth.personal.unlock_account(generator, p, 15000)

        for receiver in receivers:
            transaction = {
                'to': receiver,
                'from': generator,
                'chainId': 1000,
                'data': input
            }
            start = time.time()
            tx_hash = w3.eth.send_transaction(transaction)
            end = time.time()
            time_needed = end - start
            burst_time = burst_time + time_needed
            generator_accounts.append(generator)
            tx_hashes.append(tx_hash.hex())
            urls.append(url)
            start_times.append(start)
            tx_count = tx_count + 1

            if burst_time > 1.0:
                break

        if burst_time > 1.0:
            break
    time.sleep(1 - burst_time)
    return generator_accounts, tx_hashes, urls, start_times


def main(arg1, arg2, arg3, arg4):
    setup()
    runMiner()
    count = 0

    datadir = './data'
    startFilename = datadir + '/startFile.csv'
    dict1 = {'Generator Accounts': [], 'Transaction Hashes': [], 'URLs': [], 'Start Times': []}
    df1 = pd.DataFrame(dict1)
    df1.to_csv(startFilename, mode='w', index=False)

    time.sleep(5)
    print('Preparation phase done')

    while count < NUMBER_OF_CYCLES:
        receiver_nums = random.sample(range(0, TOTAL_ACCS), int(arg2))
        generator_nums = random.sample(range(0, TOTAL_ACCS), int(arg1))
        burst_data = {'generator_nums': generator_nums, 'receiver_nums': receiver_nums, 'tx_per_sec': arg3, 'tx_size': arg4}
        list1, list2, list3, list4 = send_transactions(burst_data)
        dict1 = {'Generator Accounts': list1, 'Transaction Hashes': list2, 'URLs': list3, 'Start Times': list4}
        df1 = pd.DataFrame(dict1)
        df1.to_csv(startFilename, mode='a', index=False, header=False)
        count = count + 1

if __name__ == "__main__":
    no_of_wallets = sys.argv[1]
    no_of_receivers = sys.argv[2]
    tx_per_sec = sys.argv[3]
    tx_size = sys.argv[4]
    main(no_of_wallets, no_of_receivers, tx_per_sec, tx_size)