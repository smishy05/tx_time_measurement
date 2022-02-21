#!/bin/bash

cd local_bc_1

geth --datadir node1 init genesis.json
wait

geth --datadir node2 init genesis.json
wait

geth --datadir node3 init genesis.json
wait

geth --datadir node4 init genesis.json
wait

geth --datadir node5 init genesis.json
wait

gnome-terminal --tab --title=Node_1 -- bash -c "geth --datadir node1 --port 7020 --nodiscover --networkid 1000 --http --http.api 'web3,eth,net,debug,personal,admin,miner,txpool' --http.port 7018 --http.corsdomain '*' --allow-insecure-unlock"

gnome-terminal --tab --title=Node_2 -- bash -c "geth --datadir node2 --port 7024 --nodiscover --networkid 1000 --http --http.api 'web3,eth,net,debug,personal,admin,miner,txpool' --http.port 7022 --http.corsdomain '*' --allow-insecure-unlock"

gnome-terminal --tab --title=Node_3 -- bash -c "geth --datadir node3 --port 7028 --nodiscover --networkid 1000 --http --http.api 'web3,eth,net,debug,personal,admin,miner,txpool' --http.port 7026 --http.corsdomain '*' --allow-insecure-unlock"

gnome-terminal --tab --title=Node_4 -- bash -c "geth --datadir node4 --port 7032 --nodiscover --networkid 1000 --http --http.api 'web3,eth,net,debug,personal,admin,miner,txpool' --http.port 7030 --http.corsdomain '*' --allow-insecure-unlock"

gnome-terminal --tab --title=Node_5 -- bash -c "geth --datadir node5 --port 7036 --nodiscover --networkid 1000 --http --http.api 'web3,eth,net,debug,personal,admin,miner,txpool' --http.port 7034 --http.corsdomain '*' --allow-insecure-unlock"