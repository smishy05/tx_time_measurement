from web3 import Web3
import pandas as pd

def main():
    datadir = './data'
    startFilename = datadir + '/startFile.csv'
    timeFilename = datadir + '/timeFile.csv'
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    dicttime = {'Transaction Hash': list1, 'Start Time': list2, 'End Time': list3, 'Time taken': list4}
    dftime = pd.DataFrame(dicttime)
    dftime.to_csv(timeFilename, mode='w', index=False)
    prev_len = 0
    while 1:
        df_start = pd.read_csv(startFilename)
        curr_file_len = df_start.shape[0]
        tx_hash = ''
        url = ''
        if prev_len < curr_file_len:
            tx_hash = df_start.iat[prev_len, 1]
            url = df_start.iat[prev_len, 2]
        # print(url)
        if url == '':
            continue
        w3 = Web3(Web3.HTTPProvider(url))
        tx = w3.eth.get_transaction(tx_hash)
        blockHash = tx['blockHash']
        if blockHash == None:
            continue
        block = w3.eth.get_block(blockHash)
        endTime = block['timestamp']
        startTime = df_start.iat[prev_len, 3]
        needed_time = float(endTime) - startTime

        prev_len = prev_len + 1

        print('')
        print(endTime, startTime)
        print(tx_hash)
        print(block)
        print('')

        dicttime = {'Transaction Hash': [tx_hash], 'Start Time': [startTime], 'End Time': [endTime], 'Time taken': [needed_time]}
        dftime = pd.DataFrame(dicttime)
        dftime.to_csv(timeFilename, mode='a', index=False, header=False)



if __name__ == '__main__':
    main()