#!/bin/bash

source ~/projects/PokeDex/venv/bin/activate
python3 <<EOF
import redis

r = redis.Redis(host='127.0.0.1', port=6379, db=0)
r.set('teste', 'ok')
print(r.get('teste').decode())
EOF
