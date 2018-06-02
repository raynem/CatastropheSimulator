#!/usr/bin/env python3
import numpy as np
import sys
import argparse

def create_servers_random(n):
    shards = 100
    while True:
        try:
            R1 = np.random.permutation(range(shards))
            R2 = np.random.permutation(range(shards))
            servers = np.random.permutation(np.concatenate((R1, R2)).reshape(n, -1)).tolist()
            break
        except:
            shards -= 1    
    return servers

def create_servers_mirror(n):
    shards = 100
    while True:
        try:
            servers = np.tile(range(shards), 2).reshape(n, -1).tolist()
            break
        except:
            shards -= 1  
    return servers

def probability_calculation(servers):
    buf = []
    for index, server in enumerate(servers):
        buf_servers = servers.copy()
        buf_servers.pop(index)
        for other_server in buf_servers:
            buf.append(set(server).isdisjoint(set(other_server)))  
    return 'Killing 2 arbitrary servers results in data loss in {:.2%} cases'.format(buf.count(False) / len(buf))

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-n', type=int)
    parser.add_argument ('--random', action = "store_true")
    parser.add_argument ('--mirror', action = "store_true")
    return parser

if __name__ == "__main__":
    parser = createParser()
    args = parser.parse_args(sys.argv[1:])
    if args.n:
        if args.random:
            print(probability_calculation(create_servers_random(args.n)))
        elif args.mirror:
            print(probability_calculation(create_servers_mirror(args.n)))
        else:
            print('Error! Expected --random or --mirror')
    else:
        print('Error! Expected -n')