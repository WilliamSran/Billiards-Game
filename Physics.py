import phylib;
import os;
import sqlite3 as sq

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER 
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS
FRAME_RATE = 0.01
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";

# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;

    def svg(self):
        st = f""" <circle id="{BALL_COLOURS[self.obj.still_ball.number]}" circle cx="{int(self.obj.still_ball.pos.x)}" cy="{int(self.obj.still_ball.pos.y)}" r="{int(BALL_RADIUS)}" fill="{BALL_COLOURS[self.obj.still_ball.number]}" />\n""" 
        return st


    # add an svg method here

class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number, position (x,y), velocity and acceleration
        as arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL,
                                       number, 
                                       pos, vel, acc, 0.0, 0.0); 
                                                    
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;
    def svg(self):
        st = f""" <circle id="{BALL_COLOURS[self.obj.rolling_ball.number]}" circle cx="{int(self.obj.rolling_ball.pos.x)}" cy="{int(self.obj.rolling_ball.pos.y)}" r="{int(BALL_RADIUS)}" fill="{BALL_COLOURS[self.obj.rolling_ball.number]}" />\n""" 
        return st

class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos):
        """
        Constructor function. requires position (x,y)
        as an argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE,
                                       0, 
                                       pos, None, None, 
                                       0.0,0.0);
      
        # this converts the phylib_object into a HOLE class
        self.__class__ = Hole;
    def svg(self):
        st = f"""<circle cx="{int(self.obj.hole.pos.x)}" cy="{int(self.obj.hole.pos.y)}" r="{int(HOLE_RADIUS)}" fill="black" />\n""" 
        return st    

class VCushion( phylib.phylib_object ):
    """
    Python Vcushion class.
    """

    def __init__( self, x,):
        """
        Constructor function. requires position (x)
        as an argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION,
                                       0, 
                                       None, None, None, 
                                       x, 0.0);
      
        # this converts the phylib_object into a VCUSHION class
        self.__class__ = VCushion;

    def svg(self):
        if self.obj.vcushion.x == 0.0:
            st = """ <rect width="25" height="2750" x="-25" y="-25" fill="darkgreen" />\n"""
        else:
            st = """ <rect width="25" height="2750" x="1350" y="-25" fill="darkgreen" />\n"""     
        return st
    
class HCushion( phylib.phylib_object ):
    """
    Python Vcushion class.
    """
    
    def __init__(self, y):
        """
        Constructor function. requires position (x)
        as an argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION,
                                       0,
                                       None, None, None, 
                                       0.0, y );
        # this converts the phylib_object into a HCUSHION class
        self.__class__ = HCushion;
        self.y = y
           
    def svg(self):
        if self.obj.hcushion.y == 0.0:
            st = """ <rect width="1400" height="25" x="-25" y="-25" fill="darkgreen" />\n"""
        else:
            st = """ <rect width="1400" height="25" x="-25" y="2700" fill="darkgreen" />\n"""     
        return st
    
################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
    
                # add ball to table
                new += new_ball;
    
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number, 
                                     Coordinate( ball.obj.still_ball.pos.x,
                                            ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;

        # return table
        return new;

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;
    # add svg method here
    def svg( self ):    
        ""
        ""
        obs = [ x.svg() for x in self if x is not None ]
        st = HEADER + ''.join(obs) + FOOTER

        return st

    def Cue(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 0 or obj.obj.rolling_ball.number == 0:
                    self.current = -1
                    return obj
    
    def Eball(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 8 or obj.obj.rolling_ball.number == 8:
                    self.current = -1
                    return obj

    def one(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 1 or obj.obj.rolling_ball.number == 1:
                    self.current = -1
                    return obj

    def two(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 2 or obj.obj.rolling_ball.number == 2:
                    self.current = -1
                    return obj

    def three(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 3 or obj.obj.rolling_ball.number == 3:
                    self.current = -1
                    return obj

    def four(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 4 or obj.obj.rolling_ball.number == 4:
                    self.current = -1
                    return obj

    def five(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 5 or obj.obj.rolling_ball.number == 5:
                    self.current = -1
                    return obj

    def six(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 6 or obj.obj.rolling_ball.number == 6:
                    self.current = -1
                    return obj

    def seven(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 7 or obj.obj.rolling_ball.number == 7:
                    self.current = -1
                    return obj

    def nine(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 9 or obj.obj.rolling_ball.number == 9:
                    self.current = -1
                    return obj

    def ten(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 10 or obj.obj.rolling_ball.number == 10:
                    self.current = -1
                    return obj

    def Eleven(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 11 or obj.obj.rolling_ball.number == 11:
                    self.current = -1
                    return obj

    def twelve(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 12 or obj.obj.rolling_ball.number == 12:
                    self.current = -1
                    return obj
                
    def thirteen(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 13 or obj.obj.rolling_ball.number == 13:
                    self.current = -1
                    return obj
                
    def fourteen(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 14 or obj.obj.rolling_ball.number == 14:
                    self.current = -1
                    return obj  
                              
    def fifteen(self):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 15 or obj.obj.rolling_ball.number == 15:
                    self.current = -1
                    return obj
    def numberlogic(self, baller=1):
        if baller == 1:
            Highballs = []
            Highballs.append(self.nine())
            Highballs.append(self.ten())
            Highballs.append(self.Eleven())
            Highballs.append(self.twelve())
            Highballs.append(self.thirteen())
            Highballs.append(self.fourteen())
            Highballs.append(self.fifteen())
            count = 0
            for obj in Highballs:
                if obj == None:
                    count += 1
            return count
                
        else:
            Lowballs = []
            Lowballs.append(self.one())
            Lowballs.append(self.two())
            Lowballs.append(self.three())
            Lowballs.append(self.four())
            Lowballs.append(self.five())
            Lowballs.append(self.six())
            Lowballs.append(self.seven())
            count = 0
            for obj in Lowballs:
                if obj == None:
                    count += 1
            return count
    
    def EndGame(self,baller):
        if self.Eball() == None:
            x = self.numberlogic(baller)
            if x >= 7:
                return 0 #for winner
            else:
                return 1 #for loser
        return 2

###################################################################################
class Database():
    
    def __init__( self, reset=False):
        if reset == True and os.path.exists('phylib.db'):
            os.remove("phylib.db")

        conn = sq.connect("phylib.db")
        self.conn = conn

    def createDB( self ):
        self.OpenSSM()

        self.c.execute("""CREATE TABLE IF NOT EXISTS Ball(
        BALLID  INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL ,
        BALLNO  INTEGER NOT NULL,
        XPOS    REAL NOT NULL,
        YPOS    REAL NOT NULL,
        XVEL    REAL,
        YVEL    REAL                     
            ) """)
        
        self.c.execute("CREATE INDEX INDX_BALLNO ON BALL (BALLNO)")
        self.c.execute("CREATE INDEX INDX_XPOS ON BALL (XPOS)")
        self.c.execute("CREATE INDEX INDX_YPOS ON BALL (YPOS)")
        self.c.execute("CREATE INDEX INDX_XVEL ON BALL (XVEL)")
        self.c.execute("CREATE INDEX INDX_YVEL ON BALL (YVEL)")


        self.c.execute(""" CREATE TABLE IF NOT EXISTS TTable (
        TABLEID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        TIME REAL NOT NULL          
        )  """)
        
        
        self.c.execute(""" CREATE TABLE IF NOT EXISTS BallTable (
        BALLID INTEGER NOT NULL,
        TABLEID INTEGER NOT NULL,
        FOREIGN KEY (BALLID) REFERENCES Ball (BALLID),
        FOREIGN KEY (TABLEID) REFERENCES TTable (TABLEID)
        )  """)

        self.c.execute(""" CREATE TABLE IF NOT EXISTS Shot (
        SHOTID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        PLAYERID INTEGER NOT NULL,
        GAMEID INTEGER NOT NULL,
        FOREIGN KEY (PLAYERID) REFERENCES Player (PLAYERID),
        FOREIGN KEY (GAMEID) REFERENCES Game (GAMEID)                    
        )  """)

        self.c.execute("CREATE INDEX INDX_PLAYERID ON SHOT (PLAYERID)")
        self.c.execute("CREATE INDEX INDX_GAMEID ON SHOT (GAMEID)")
        
        
        self.c.execute(""" CREATE TABLE IF NOT EXISTS TableShot (
        TABLEID INTEGER,
        SHOTID INTEGER, 
        FOREIGN KEY (TABLEID) REFERENCES TTable (TABLEID),
        FOREIGN KEY (SHOTID) REFERENCES Shot (SHOTID)                   
        )  """)

        self.c.execute(""" CREATE TABLE IF NOT EXISTS Game (
        GAMEID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        GAMENAME TEXT  NOT NULL
        )  """)
        
        self.c.execute(""" CREATE TABLE IF NOT EXISTS Player (
        PLAYERID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        GAMEID INTEGER NOT NULL,
        PLAYERNAME TEXT NOT NULL,
        FOREIGN KEY (GAMEID) REFERENCES Game (GAMEID)
        )  """)

        self.c.close()
        self.conn.commit()


    def readTable(self, tableID):
        self.OpenSSM()
        try:
            self.c.execute("""
               SELECT * FROM Ball
               INNER JOIN BallTable ON Ball.BALLID = BallTable.BALLID
               INNER JOIN TTable ON BallTable.TABLEID = TTable.TABLEID
                WHERE BallTable.TABLEID = ?   """, (tableID+1,))
            res = self.c.fetchall()
            if not res:
                return None
            
            table = Table() 
            for row in res:
                if (row[4] is None and row[5] is None) or (row[4] == 0.0 and row[5] == 0.0) :
                    pos = Coordinate(row[2],row[3])
                    sb = StillBall(row[1],pos)
                    table += sb

                else:
                    pos = Coordinate(row[2], row[3])
                    vel = Coordinate(row[4],row[5])
                    rb = RollingBall(row[1],pos,vel,Coordinate(0,0))
                    speed = phylib.phylib_length(rb.obj.rolling_ball.vel)
                    if speed > VEL_EPSILON:
                        xacc = (-1*row[4]) / speed * DRAG
                        yacc = (-1*row[5]) / speed * DRAG
                        acc = Coordinate(xacc, yacc)
                        rb = RollingBall(row[1],pos,vel,acc)       
                    table += rb
            table.time = row[9]
            return table
        
        except sq.Error as err:
            print(f"Error reading table: {err}")
            return None

        finally:
            self.c.close()
            self.conn.commit()
        
        
    def writeTable( self, table):
        self.OpenSSM()

        self.c.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))
        TabID = self.c.lastrowid

        for obj in table:
            if isinstance(obj, StillBall) or isinstance(obj,RollingBall):
                if isinstance(obj,StillBall):
                    self.c.execute(""" INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) 
                            VALUES (?, ?, ?, NULL, NULL)
                        """, (obj.obj.still_ball.number, 
                              obj.obj.still_ball.pos.x, 
                              obj.obj.still_ball.pos.y))
                    Bid = self.c.lastrowid
                    self.c.execute(""" INSERT INTO BALLTable (BALLID, TABLEID) 
                            VALUES (?, ?)""", (Bid, TabID) )


                else:
                    self.c.execute(""" INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) 
                            VALUES (?, ?, ?, ?, ?)
                        """, (obj.obj.rolling_ball.number, 
                              obj.obj.rolling_ball.pos.x, 
                              obj.obj.rolling_ball.pos.y,
                              obj.obj.rolling_ball.vel.x,
                              obj.obj.rolling_ball.vel.y)) 
                    Bid = self.c.lastrowid
                    self.c.execute(""" INSERT INTO BALLTable (BALLID, TABLEID) 
                            VALUES (?, ?)""" ,(Bid, TabID) )


        self.c.close()
        self.conn.commit()
        return TabID-1
    
    def getGame(self, GameID):
        self.OpenSSM()
        self.c.execute("""SELECT g.GAMENAME, p1.PLAYERNAME as Player1Name, p2.PLAYERNAME as Player2Name
                        FROM GAME g
                        JOIN PLAYER p1 ON g.GAMEID = p1.GAMEID
                        JOIN PLAYER p2 ON g.GAMEID = p2.GAMEID
                        WHERE g.GAMEID = ? AND p1.PLAYERID < p2.PLAYERID
                        """, (GameID,))
        result = self.c.fetchone()
        Gname = result[0]
        p1 = result[1]
        p2 = result[2]

        self.c.close()
        self.conn.commit()

        return Gname,p1,p2

    def setGame(self, Gn, p1,p2):
        self.OpenSSM()

        self.c.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (Gn,))
        gID = self.c.lastrowid
        self.c.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (? , ?)", (gID, p1))
        self.c.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (? , ?)", (gID, p2))

        self.c.close()
        self.conn.commit()

    def newShot(self, Gn, pn):
        self.OpenSSM()

        self.c.execute(" SELECT GAMEID FROM Game WHERE Game.GAMENAME = ? ",(Gn,))
        Gid = self.c.fetchone()

        self.c.execute("""
                    SELECT PLAYER.PLAYERID
                    FROM PLAYER
                    INNER JOIN GAME ON PLAYER.GAMEID = GAME.GAMEID
                    WHERE GAME.GAMENAME = ? AND PLAYER.PLAYERNAME = ?
                """, (Gn, pn))
        pID = self.c.fetchone()

        self.c.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)", (pID[0],Gid[0]))
        ShotID = self.c.lastrowid

        self.c.close()
        self.conn.commit()

        return ShotID
    
    def TableShot(self, sID, Tid):
        self.OpenSSM()

        self.c.execute("""INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)""",(Tid,sID))

        self.c.close()
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()
    
    def OpenSSM(self):
        conn = sq.connect('phylib.db')
        self.conn = conn
        self.c = self.conn.cursor()
        
###########################################################################
class Game():
    def __init__( self, gameID=None, gameName=None, player1Name=None,player2Name=None ):
         """
            The constructor can be called in exactly two ways:
            (i) with an integer gameID value, and all other arguments set to None, or
            (ii) with gameID=None, string values for all 3 Name arguments
            if not you get an error bud
         """
         if( isinstance(gameID, int )  and all(value is None for value in [gameName, player1Name, player2Name])  ):
             x = Database()
             self.gameID = gameID
             self.gameName, self.player1Name, self.player2Name = x.getGame(gameID + 1)

         elif(gameID is None and all(isinstance(value,str) for value in [gameName, player1Name, player2Name]) ):
            x = Database()
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            x.setGame(gameName,player1Name,player2Name)

         else:
            raise TypeError("wrong insertion format")

    def shoot( self, gameName, playerName, table, xvel, yvel ):
        x = Database()
        ShotID = x.newShot(gameName,playerName)
        Cb = table.Cue()
        xpos = Cb.obj.still_ball.pos.x
        ypos = Cb.obj.still_ball.pos.y
        Cb.type = phylib.PHYLIB_ROLLING_BALL
        Cb.obj.rolling_ball.number = 0
        Cb.obj.rolling_ball.pos.x = xpos
        Cb.obj.rolling_ball.pos.y = ypos
        Cb.obj.rolling_ball.vel.x = xvel
        Cb.obj.rolling_ball.vel.y = yvel
        Cb.obj.rolling_ball.acc.x = 0.0
        Cb.obj.rolling_ball.acc.y = 0.0
        speed = phylib.phylib_length(Cb.obj.rolling_ball.vel)
        if speed > VEL_EPSILON:
            xacc = (-1*Cb.obj.rolling_ball.vel.x) / speed * DRAG
            yacc = (-1*Cb.obj.rolling_ball.vel.y) / speed * DRAG
            Cb.obj.rolling_ball.acc.x = xacc
            Cb.obj.rolling_ball.acc.y = yacc

        new_tb = table.segment()
        begtime = table.time
        StringVG = table.svg()
        while True:
                new_tb = table.segment()
                 
                if new_tb is None:
                    
                    tID=x.writeTable(table)
                    tb = x.readTable(tID)
                    if tb.Cue() == None:
                        tb += StillBall(0,Coordinate(675, 2025))
                        StringVG += tb.svg()
                        tID=x.writeTable(tb)
                    #x.TableShot(ShotID,tID)
                    return StringVG, tID

                begtime = table.time
                endtime = new_tb.time
                duration = endtime - begtime
                
               
                fps = int(duration // FRAME_RATE)  

                for frame in range(fps):
                    RollTide = frame * FRAME_RATE
                    RolledTable = table.roll(RollTide)
                    RolledTable.time = RollTide + begtime
                    sveg = RolledTable.svg()
                    StringVG += sveg
                    #tID=x.writeTable(RolledTable)
                    #x.TableShot(ShotID,tID) 

                table = new_tb
            
        


            

          
            

            


         

        
        
        
            





        

