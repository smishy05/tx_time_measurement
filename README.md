# Steps to run

1. Install geth using the instructions from https://github.com/ConsenSysMesh/local\_ethereum\_network .
2. Clone this repository.
3. Run the shell script `./run_lbc_1.sh`. This terminal should keep running.
4. Go into the `python-1` directory and run the `script` code using `python script.py 5 5 10 250` where the arguments are number of wallets that are generating transactions, number of accounts that are receiving transactions, number of transactions per second and transaction size (in bytes) respectively.
5. After you see the prompt that the setup is complete in the terminal, open another terminal and run `python validation_time.py`.
