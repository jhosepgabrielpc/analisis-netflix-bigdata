#!/usr/bin/env python3
import sys
import csv

reader = csv.reader(sys.stdin)
for row in reader:
    if not row or row[0] == 'show_id':
        continue
    
    show_id = row[0]
    cast_str = row[4]
    
    if cast_str and cast_str.strip():
        actores = cast_str.split(',')
        for actor in actores:
            actor_limpio = actor.strip()
            if actor_limpio:
                # Modificado para Python 3.5
                print("{0}\t{1}".format(actor_limpio, show_id))