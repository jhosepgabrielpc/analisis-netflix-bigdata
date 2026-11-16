#!/usr/bin/env python3
import sys

current_actor = None
show_ids = set()

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    partes = line.split('\t', 1)
    if len(partes) != 2:
        continue
        
    actor, show_id = partes
    
    if current_actor == actor:
        show_ids.add(show_id)
    else:
        if current_actor is not None:
            # Modificado para Python 3.5
            print("{0}\t{1}".format(current_actor, len(show_ids)))
        current_actor = actor
        show_ids = {show_id}

if current_actor is not None:
    # Modificado para Python 3.5
    print("{0}\t{1}".format(current_actor, len(show_ids)))