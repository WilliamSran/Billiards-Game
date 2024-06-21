import sys
import cgi
import os
import glob
import Physics as ph
import re
from datetime import datetime
import random
import json  
#re package is used to match strings
#os is for opening files and changing attributes
#glob is used to just make finding paths easier
#the rest is from lab 2, simple functions or of course our python files we need to access

from http.server import HTTPServer as HT
from http.server import BaseHTTPRequestHandler as BH
from urllib.parse import urlparse, parse_qs
#base of lab 2 code (S.Kremer 2024)
x = ph.Database(reset=True)
x.createDB()
table = ph.Table
global TabID
global balla
global count
global tempshoora
global highball
highball = 1
global lowball
lowball =0
count = 0;
balla = -2;
TabID = 0;
#http://127.0.0.1:3000/Start.html
class MyHandler(BH):            
    
    #Responses to GET requests
    def do_GET(self):
        
        parsed = urlparse(self.path)
        
        if parsed.path in ['/Start.html']:
        
            fp = open('.'+parsed.path)
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send to browser
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();
        
        elif parsed.path.startswith('/script.js'):
            filepath = '.' + parsed.path  
            if os.path.isfile(filepath):
                with open(filepath, 'rb') as file:
                    self.send_response(200)  # OK
                    self.send_header('Content-type', 'application/javascript')
                    self.end_headers()
                    self.wfile.write(file.read())            
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )   
        
    def do_POST(self):

        parsed = urlparse(self.path)
        if parsed.path in [ '/Play.html' ]:
            
            #1. Receiving form data from shoot.html
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                   ); 
            global p1
            global p2
            Gn = "Game " + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            p1 = form.getvalue('player1Name')
            p2 = form.getvalue('player2Name')
            table = createStartingTable()
            global x
            x = ph.Database(reset=True)
            x.createDB()

            global shoota 
            shoota = random.choice([p1, p2])
            ph.Game(None,Gn, shoota,p2)
            x.writeTable(table)
            

            startingSVGString = table.svg()
            htmlContent = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>GAME ON</title>
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
                <script src="script.js"></script> 
                <style>
                    body{{
                        max-height: 100vh;
                        background-color: rgb(55, 55,55);
                    }}
                    #svg-container {{
                        top: 10%;
                        left: 33%;
                        border: 0px solid lightcoral;
                        transform-origin: top left; 
                        position: fixed;
                        margin:
                        margin: 0%;
                    }}
                    #Ball {{
                        top: 10%;
                        right: 33%;
                        margin: 0%;
                        font-size: 80px;
                    }}
                    #Ballt {{
                        top: 10%;
                        right: 33%;
                        margin: 0%;
                        font-size: 80px;
                    }}
                    #player {{
                        top: 10%;
                        right: 33%;
                        margin: 0%;
                        font-size: 80px;
                    }}
                </style>
            </head>
            <body">
                <!-- Player names placeholders -->
                <div id="player"> Player 1: {p1}</div>
                <div id="player"> Player 2: {p2}</div>
                <div id="Ball" > Player 1: is  </div>
                <div id="Ballt" > Player 2: is  </div>
                <div id="firstShooter" style="font-weight: bold; font-size: 80px; margin-bottom: 10px;"> Turn: {shoota}</div>
                
                <div id="svg-container">
                    {startingSVGString}
                </div>
                
            </body>
            </html>
            """

            
            # Send 200 response
            self.send_response(200)  
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", str(len(htmlContent)))
            self.end_headers()
            
            self.wfile.write(bytes(htmlContent, "utf-8"))
            #Error send 404 response
        
        if parsed.path in [ '/Playing.html' ]:  

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            decoded_data = post_data.decode('utf-8')
            parsed_data = parse_qs(decoded_data)
            Data = {key: float(value[0]) for key, value in parsed_data.items()}
            
            global TabID
            global balla
            global count
            global tempshoora
            global highball
            global lowball
            y=ph.Game(0)

            table = x.readTable(TabID)
            svgstring, TabID = y.shoot(gameName=y.gameName,playerName=shoota,table=table, xvel=Data['xvel'],yvel=Data['yvel'])
            Nxttable = x.readTable(TabID)

            con = 3
            playa =5
            

            if count == 0:
                tempshoora ="" + shoota
            BallerType = 3

            if balla == -2:
                lowball =Nxttable.numberlogic(0)
                highball =Nxttable.numberlogic(1)
                if lowball > 0:
                    balla = 0;
                    BallerType =0
                elif highball > 0:
                    balla =1
                    BallerType =1   
                if shoota == p1 and (balla == -2):
                    tempshoora = p2
                elif shoota ==p2 and (balla ==-2):
                    tempshoora = p1
                
            # if balla >-2:
            #     con =Nxttable.EndGame(balla)
            con = 2
            if count ==1 and (balla >-2):
                if balla >-2:
                    if balla == 0:
                        count = Nxttable.numberlogic(balla)
                        con = Nxttable.EndGame(balla)
                        playa = balla
                        if count > lowball +1:
                            lowball = count
                            #print("BALLA STILL 0")
                        else:
                            balla = 1
                            #print("BALLA CHANGED TO 1")
                            if tempshoora == p1:
                                tempshoora = p2
                            else:
                                tempshoora =p1
                
                    elif balla == 1:
                        count = Nxttable.numberlogic(balla)
                        con = Nxttable.EndGame(balla)
                        playa = balla
                        if count > highball +1:
                            highball = count
                            #print("BALLA STILL 1")                        
                        else:
                            balla = 0
                            #print("BALLA CHANGED TO 0")
                            if tempshoora == p1:
                                tempshoora = p2
                            else:
                                tempshoora =p1

            whichplayer =0
            count =1
            if tempshoora == p1:
                whichplayer = 1
            else:
                whichplayer = 2

            shoora = "oga" + tempshoora
            wincon = "oga" + str(con)
            LowHih = "oga" + str(BallerType)
            p1orp2 = "oga" + str(whichplayer)
            winner = "oga" + str(playa)
            xtra = "oga" +"howdy"
            self.wfile.write(svgstring.encode('utf-8'))
            self.wfile.write(bytes(shoora, "utf-8"))
            self.wfile.write(bytes(wincon, "utf-8"))
            self.wfile.write(bytes(LowHih, "utf-8"))
            self.wfile.write(bytes(p1orp2, "utf-8"))
            self.wfile.write(bytes(winner, "utf-8"))
            self.wfile.write(bytes(xtra, "utf-8"))
            BallerType = 3
            #TabID = tID
            
            # Send 200 response
            self.send_response(200)  
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )             
            
 #################################
#This function creates the Starting Table
def createStartingTable():
    table = ph.Table()

    ballPositions = [
                ph.Coordinate(675, 2025), # Cue Ball (White) 0
                ph.Coordinate(675, 675),  # Yellow 1
                ph.Coordinate(635, 622),  # Blue 2
                ph.Coordinate(604, 569),  # Red 3
                ph.Coordinate(574, 516),  # Purple 4  
                ph.Coordinate(797, 463),  # Orange 5
                ph.Coordinate(614, 463),  # Green   6          
                ph.Coordinate(706, 516),  # Brown 7
                ph.Coordinate(675, 569),  # Black  8
                ph.Coordinate(706, 622),  # Light Yellow 9
                ph.Coordinate(736, 569),  # Light Blue 10
                ph.Coordinate(767, 516),  # Pink 11
                ph.Coordinate(553, 463),  # Medium Purple 12
                ph.Coordinate(736, 463),  # Light Salmon 13
                ph.Coordinate(645, 516),  # Light Green 14
                ph.Coordinate(675, 463),  # Sandy Brown 15
                ]
         
    for ballNum in range(len(ballPositions)):
        table += ph.StillBall(ballNum, ballPositions[ballNum])        
    
    return table   



if __name__ == "__main__":
    httpd = HT( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();
    

