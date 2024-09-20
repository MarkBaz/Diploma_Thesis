from Ball import Ball
from Player import Player
from write_toCSV import CSVWriter
import csv


class Moment:
    """A class for keeping info about the moments"""
    def __init__(self, moment, eventid_from_event):
        self.quarter = moment[0]  # Hardcoded position for quarter in json
        self.game_clock = moment[2]  # Hardcoded position for game_clock in json
        self.shot_clock = moment[3]  # Hardcoded position for shot_clock in json
        self.eventid_from_event = eventid_from_event
        ball = moment[5][0]  # Hardcoded position for ball in json

        ballCSV = [ball[2],ball[3]]
        # Creating an instance of CSVWriter
        fieldnames = ['ball poss', 'player1', 'player2', 'player3', 'player4', 'player5', 'player6', 'player7', 'player8', 'player9', 'player10', 'eventid']
        csv_writer = CSVWriter('json1.csv', fieldnames)
        CSV = [ballCSV]
        

        self.ball = Ball(ball)

        players = moment[5][1:]  # Hardcoded position for players in json
        playersPos = []
        for playerid in players:
            playerZ = [playerid[2],playerid[3]] 
            playerpos = [playerZ]
            playersPos.extend(playerpos)

        if(len(playersPos) == 0):
            extender0 = [0,0]
            extenderpos0 = [extender0]
            playersPos.extend(extenderpos0)
        if(len(playersPos) == 1):
            extender1 = [0,0]
            extenderpos1 = [extender1]
            playersPos.extend(extenderpos1)
        if(len(playersPos) == 2):
            extender2 = [0,0]
            extenderpos2 = [extender2]
            playersPos.extend(extenderpos2)
        if(len(playersPos) == 3):
            extender3 = [0,0]
            extenderpos3 = [extender3]
            playersPos.extend(extenderpos3)
        if(len(playersPos) == 4):
            extender4 = [0,0]
            extenderpos4 = [extender4]
            playersPos.extend(extenderpos4)
        if(len(playersPos) == 5):
            extender5 = [0,0]
            extenderpos5 = [extender5]
            playersPos.extend(extenderpos5)
        if(len(playersPos) == 6):
            extender6 = [0,0]
            extenderpos6 = [extender6]
            playersPos.extend(extenderpos6)
        if(len(playersPos) == 7):
            extender7 = [0,0]
            extenderpos7 = [extender7]
            playersPos.extend(extenderpos7)
        if(len(playersPos) == 8):
            extender8 = [0,0]
            extenderpos8 = [extender8]
            playersPos.extend(extenderpos8)
        if(len(playersPos) == 9):
            extender9 = [0,0]
            extenderpos9 = [extender9]
            playersPos.extend(extenderpos9)
        
        # Writing rows to the CSV file
        csv_writer.write_row({'ball poss': ballCSV, 'player1': playersPos[0], 'player2': playersPos[1], 'player3': playersPos[2], 'player4': playersPos[3], 'player5': playersPos[4], 'player6': playersPos[5], 'player7': playersPos[6], 'player8': playersPos[7], 'player9': playersPos[8], 'player10': playersPos[9], 'eventid': self.eventid_from_event})

        # Closing the CSV file
        csv_writer.close_file()
        


        self.players = [Player(player) for player in players]



