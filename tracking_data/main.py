from Game import Game
import argparse
import pandas as pd
import os
import json
from write_toCSV import CSVWriter
import csv



game = Game(path_to_json='D:/genika desktop/mark/diplwma/diploma_thesis/tracking_data/0021500001.json', event_index=0)
#game.read_json()
#game.start()


events = game.json_len()
for i in range(events):
    game = Game(path_to_json='D:/genika desktop/mark/diplwma/diploma_thesis/tracking_data/0021500001.json', event_index=i)

    game.read_json()

    game.start()