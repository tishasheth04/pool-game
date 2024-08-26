import phylib;
import os
import sqlite3
import math

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;
FRAME_INTERVAL = 0.01;


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


    # add an svg method here

    def svg (self):
        stillBallString = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
        return stillBallString;


################################################################################

class RollingBall(phylib.phylib_object):

    def __init__(self, number, pos, vel, acc):
    
        phylib.phylib_object.__init__(self,
                                    phylib.PHYLIB_ROLLING_BALL, 
                                    number, 
                                    pos, vel, acc, 
                                    0.0, 0.0);
        self.__class__ = RollingBall;
    
    def svg (self):
        rollingBallString = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])
        return rollingBallString;

###############################################################################

class Hole(phylib.phylib_object):

    def __init__(self, pos):
        phylib.phylib_object.__init(self, phylib.PHYLIB_HOLE, 0, pos, None, None, 0.0, 0.0);
        self.__class__ = Hole;

    def svg (self):
        holeString = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS, BALL_COLOURS[8])
        return holeString;

###############################################################################

class HCushion(phylib.phylib_object):

    def __init__(self, y):
        phylib.phylib_object.__init(self, phylib.PHYLIB_HCUSHION, None, None, None, None, 0.0, y);
        self.__class__ = HCushion;
    
    def svg(self):
        if(self.obj.hcushion.y == 0): #check this?
            hCushionString = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (-25)
        elif(self.obj.hcushion.y > 0): #check this
            hCushionString = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (2700)
        return hCushionString;

###############################################################################

class VCushion(phylib.phylib_object):

    def __init__(self, x):
        phylib.phylib_object.__init(self, phylib.PHYLIB_VCUSHION, None, None, None, None, x, 0.0);
        self.__class__ = VCushion;
    
    def svg(self):
        if(self.obj.vcushion.x == 0): #on the left so its negative
            vCushionString = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (-25)
        elif(self.obj.vcushion.x > 0): #on the right so its positive
            vCushionString = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (1350)
        return vCushionString;

###############################################################################

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

    def svg (self):
        #return "HELLo"
        resultedString = HEADER

        for object in self:
           if object is not None:
            resultedString += object.svg()
        resultedString += FOOTER
        return resultedString
    
    # This function was provided by the professor.

    def roll(self, t):
        new = Table();
        for ball in self:
            if isinstance(ball, RollingBall):
                new_ball = RollingBall(ball.obj.rolling_ball.number, Coordinate(0,0),Coordinate(0,0), Coordinate(0,0));
                phylib.phylib_roll(new_ball, ball, t);
                new+=new_ball;
            if isinstance(ball, StillBall):
                new_ball = StillBall(ball.obj.still_ball.number,
                                     Coordinate(ball.obj.still_ball.pos.x,
                                     (ball.obj.still_ball.pos.y)));
                new+=new_ball;
        return new;

    def findCueBall(self):
        # Method to find and return the cue ball in the table
        for ball in self:
            if(isinstance(ball, StillBall) and ball.obj.still_ball.number == 0):
                return ball
        return None


class Database():

    def __init__( self, reset=False ):
        if reset == True:
            if os.path.exists( 'phylib.db' ): 
                os.remove( 'phylib.db' );
        self.conn = sqlite3.connect( 'phylib.db' ); #connect the database
    
    def close( self ):
        if(self.conn): #close and commit
            self.conn.commit();
            self.conn.close();
            

    def pp( listoftuples ): #pp function from lab 3
        if len(listoftuples)==0:
            print( repr( listoftuples ) );
            return;
        columns = len(listoftuples[0]);
        widths = [ max( [ len(str(item[col])) for item in listoftuples ] ) \
                                    for col in range( columns ) ];
        fmt = " | ".join( ["%%-%ds"%width for width in widths] );
        for row in listoftuples:
            print( fmt % row );

    def printDB(self): # helper function I made to print specific parts of the database
        self.cur = self.conn.cursor();

        print("BALL:")
        self.cur = self.conn.execute("""SELECT * FROM Ball;""")
        result = self.cur.fetchall();
        print(result)
        print("TTABLE:")
        self.cur = self.conn.execute("""SELECT * FROM TTable;""")
        result = self.cur.fetchall();
        print(result)
        print("BALLTABLE:")
        self.cur = self.conn.execute("""SELECT * FROM BallTable;""")
        result = self.cur.fetchall();
        print(result)

        self.conn.commit();
        self.cur.close();

    def createDB( self ):
        
        self.cur = self.conn.cursor(); # open the cursor

        #Ball
        self.cur = self.conn.execute("""CREATE TABLE IF NOT EXISTS Ball(
            BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            BALLNO INTEGER NOT NULL,
            XPOS FLOAT NOT NULL,
            YPOS FLOAT NOT NULL,
            XVEL FLOAT,
            YVEL FLOAT
            );""")

        #TTable
        self.cur = self.conn.execute("""CREATE TABLE IF NOT EXISTS TTable(
            TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            TIME FLOAT NOT NULL
            );""")

        #BallTable
        self.cur = self.conn.execute( """CREATE TABLE IF NOT EXISTS BallTable (
           BALLID  INTEGER NOT NULL,
           TABLEID INTEGER NOT NULL,
           FOREIGN KEY (BALLID) REFERENCES Ball ON UPDATE CASCADE,
           FOREIGN KEY (TABLEID) REFERENCES TTable );""");

        # cur = conn.execute("""CREATE TABLE IF NOT EXISTS BALLTABLE AS
        #     SELECT * FROM BALL
        #     INNER JOIN TTABLE ON BALL.BALLID = TTABLE.TABLEID;
        #     )""")
        
        #Game
        self.cur = self.conn.execute("""CREATE TABLE IF NOT EXISTS Game(
            GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            GAMENAME VARCHAR(64) NOT NULL
            );""")

        #Player
        self.cur = self.conn.execute("""CREATE TABLE IF NOT EXISTS Player(
            PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            GAMEID INTEGER NOT NULL,
            PLAYERNAME VARCHAR(64) NOT NULL,
            FOREIGN KEY (GAMEID) REFERENCES Game
            );""")

        #Shot
        self.cur = self.conn.execute("""CREATE TABLE IF NOT EXISTS Shot(
            SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            PLAYERID INTEGER NOT NULL,
            GAMEID INTEGER NOT NULL,
            FOREIGN KEY (PLAYERID) REFERENCES Player,
            FOREIGN KEY (GAMEID) REFERENCES Game
            );""")

        #TableShot
        self.cur = self.conn.execute( """CREATE TABLE IF NOT EXISTS TableShot (
           TABLEID  INTEGER NOT NULL,
           SHOTID INTEGER NOT NULL,
           FOREIGN KEY (TABLEID) REFERENCES TTable,
           FOREIGN KEY (SHOTID) REFERENCES Shot );""");
        
        # cur = conn.execute("""CREATE TABLE IF NOT EXISTS TABLESHOT AS
        #     SELECT * FROM TTABLE
        #     INNER JOIN SHOT ON TTABLE.TABLEID = SHOT.SHOTID;
        #     )""")

        #self.printDB()
  
        #commit and close the cursor
        self.conn.commit();
        self.cur.close();

    def readTable(self, tableId):
        
        self.cur = self.conn.cursor(); #open the cursor

        tableId += 1 # increment the tableID
        self.cur.execute("SELECT * FROM BallTable WHERE TABLEID = ?", (tableId,))
        fetched = self.cur.fetchone()
        if fetched == None: #check the TABLEID exists
            self.conn.commit();
            self.cur.close();
            #print("fetched is none!")
            return None

        newTable = Table(); # make a new table
        selectedID = tableId

        # cur = conn.execute(f"""SELECT TABLEID FROM BALLTABLE
        #     WHERE TABLEID='{tableId}';""")
        # selectedID = cur.fetchall();
        # selectedID = selectedID[0][0]
        
        # join Ball with BallTable where the tableIDs match
        self.cur.execute("""SELECT Ball.* FROM Ball
            INNER JOIN BallTable ON Ball.BALLID = BallTable.BALLID
            WHERE BallTable.TABLEID=?;""", (tableId,))
        fetched = self.cur.fetchall();
        #print(fetched);
        #print(len(fetched))

        # for loop that loops through each tuple in the list
        for i in range(len(fetched)):
            if fetched[i][4] is None and fetched[i][5] is None: #still ball case
                # sets all the info
                ballID = fetched[i][0]
                ballNo = fetched[i][1]
                xPos = fetched[i][2]
                yPos = fetched[i][3]
                xVel = 0
                yVel = 0
                sPos = Coordinate(xPos, yPos) # makes the coordinate, still ball 
                sBall = StillBall(ballNo, sPos)
                newTable += sBall # adds it to the table
            else: #fetched[i][4] > 0 or fetched[i][5] > 0
                # sets all the info
                ballID = fetched[i][0]
                ballNo = fetched[i][1]
                xPos = fetched[i][2]
                yPos = fetched[i][3]
                xVel = fetched[i][4]
                yVel = fetched[i][5]
                rPos = Coordinate(xPos, yPos) # make the position and velocity
                rVel = Coordinate(xVel, yVel)

                # calculate the acceleration like in A2
                rAcc = Coordinate(0.0, 0.0)
                rSpeed = phylib.phylib_length(rVel)

                if (rSpeed > VEL_EPSILON):
                    rAcc.x = ((xVel * -1.0) / rSpeed) * DRAG
                    rAcc.y = ((yVel * -1.0) / rSpeed) * DRAG

                rBall = RollingBall(ballNo, rPos, rVel, rAcc)
                newTable += rBall # add the new rolling ball to the table

        self.cur.execute("""SELECT TIME FROM TTable
                               WHERE TABLEID = ?""", (tableId,))
        time = self.cur.fetchone()
        newTable.time = time[0] # fetch and add the time to the table
        
        self.conn.commit(); # commit and close the cursor
        self.cur.close();
        return newTable
        
    def writeTable(self, table):
        self.cur = self.conn.cursor() # open the cursor
        #print(type(table.time))
        tableId = 0 # this may need to be set to something else
        counter = 1
        xPos = 0
        yPos = 0 # declaring the variables
        xVel = 0
        yVel = 0
        ballID = 0; # this may need to be set to something else too
        ballStr = ""
        ball_data = (None)

        # add the table (and auto increment tableID)
        tableStr = f"""INSERT INTO TTable (TIME)
            VALUES ({table.time});"""
        self.cur = self.conn.execute(tableStr)

        # grab said tableID
        tableStr = f"""SELECT TABLEID FROM TTable
                    WHERE TIME={table.time};"""
        self.cur = self.conn.execute(tableStr)

        getID = self.cur.fetchone();
        #print(len(getID))
        tableId = getID[0]

        # for loop that loops through the table and looks for still and rolling balls to write
        for ball in table:
            #object.type == phylib.PHYLIB_ROLLING_BALL
            if isinstance( ball, RollingBall ):
                # get all the info
                ballNum = ball.obj.rolling_ball.number
                xPos = ball.obj.rolling_ball.pos.x
                #print("xPos for a rolling ball")
                #print(type(xPos))
                yPos = ball.obj.rolling_ball.pos.y
                xVel = ball.obj.rolling_ball.vel.x
                yVel = ball.obj.rolling_ball.vel.y
                ballStr = """INSERT INTO Ball ( BALLNO, XPOS, YPOS, XVEL, YVEL)
                    VALUES (?, ?, ?, ?, ?);"""
                #{ballNum}, {xPos}, {yPos}, {xVel}, {yVel}

                # insert said info into ball, also auto incrementing
                self.cur = self.conn.execute("""INSERT INTO Ball ( BALLNO, XPOS, YPOS, XVEL, YVEL)
                    VALUES (?, ?, ?, ?, ?);""", (ballNum, xPos, yPos, xVel, yVel))
                #ball_data = (ballNum, xPos, yPos, xVel, yVel, counter)
                #self.cur = self.conn.execute("""INSERT INTO Ball ( BALLNO, XPOS, YPOS, XVEL, YVEL)
                    #VALUES (?, ?, ?, ?, ?);""", (ballNum, xPos, yPos, xVel, yVel))
                
                # get the most recent ballID and insert it into ballTable with tableID
                self.cur = self.conn.execute("""SELECT BALLID FROM Ball
                    ORDER BY BALLID DESC""")
                ballID = self.cur.fetchone()
                ballID = ballID[0]
                self.cur = self.conn.execute("""INSERT INTO BallTable (BALLID, TABLEID)
                    VALUES (?, ?);""", (ballID, tableId))

            elif isinstance( ball, StillBall ):
                # get the info for a still ball
                ballNum = ball.obj.still_ball.number
                xPos = ball.obj.still_ball.pos.x
                #print("xPos for a still ball")
                #print(xPos)
                yPos = ball.obj.still_ball.pos.y
                xVel = 0
                yVel = 0
                ballStr = """INSERT INTO Ball ( BALLNO, XPOS, YPOS)
                    VALUES (?, ?, ?);"""
                #{ballNum}, {xPos}, {yPos}, {xVel}, {yVel}

                # insert said info into ball, also auto incrementing
                self.cur = self.conn.execute("""INSERT INTO Ball ( BALLNO, XPOS, YPOS)
                    VALUES (?, ?, ?);""", (ballNum, xPos, yPos))

                #ball_data = (ballNum, xPos, yPos, xVel, yVel, counter)
                # ballStr = f"""INSERT INTO Ball ( BALLNO, XPOS, YPOS, XVEL, YVEL)
                #     VALUES ({ballNum}, {xPos}, {yPos}, {xVel}, {yVel});"""
                # self.cur = self.conn.execute(ballStr)
                

                # get the most recent ballID and insert it into ballTable with tableID
                self.cur = self.conn.execute("""SELECT BALLID FROM Ball
                    ORDER BY BALLID DESC""")
                ballID = self.cur.fetchone()
                ballID = ballID[0]
                self.cur = self.conn.execute("""INSERT INTO BallTable (BALLID, TABLEID)
                    VALUES (?, ?);""", (ballID, tableId))

        # commit and close the cursor
        self.conn.commit();
        self.cur.close();
        tableId = tableId - 1 # decrement tableID
        return tableId

    def getGame( self, gameID ):
        self.cur = self.conn.cursor() # open the cursor
        # get playerID, name, and gameName with a join
        self.cur = self.conn.execute(f"""SELECT Player.PLAYERID, Player.PLAYERNAME, Game.GAMENAME FROM Player
            JOIN Game ON Player.GAMEID = Game.GAMEID
            WHERE Game.GAMEID={gameID};""")
        gameStatus = self.cur.fetchall()
        return gameStatus

    def setGame( self, gameName, player1Name, player2Name ):
        self.cur = self.conn.cursor() # open the cursor

        #insert gamename (and auto increment ID)
        gameStr = f"""INSERT INTO Game (GAMENAME)
            VALUES ({gameName});"""
        self.cur = self.conn.execute(f"""INSERT INTO Game (GAMENAME)
            VALUES (?);""", (gameName,))
        
        # get the ID just inserted
        gameStr = f"""SELECT GAMEID FROM Game
            WHERE GAMENAME={gameName}"""
        self.cur = self.conn.execute("""SELECT GAMEID FROM Game
            WHERE GAMENAME=?""", (gameName,))
        gameID = self.cur.fetchone()
        gameID = gameID[0]

        #playerStr = f"""INSERT INTO Player (GAMEID, PLAYERNAME)
            #VALUES ({gameID}, {player1Name});"""
        #insert in the two player names with correct IDs and auto increment 
        self.cur = self.conn.execute("""INSERT INTO Player (GAMEID, PLAYERNAME)
            VALUES (?, ?);""", (gameID, player1Name,))
        self.cur = self.conn.execute("""INSERT INTO Player (GAMEID, PLAYERNAME)
            VALUES (?, ?);""", (gameID, player2Name,))
        
        self.conn.commit() # commit and close the cursor
        self.cur.close()

    def newShot(self, playerName):
        self.cur = self.conn.cursor() # open the cursor
        # get the gameID based on player name
        self.cur = self.conn.execute("""SELECT GAMEID FROM Player
            WHERE PLAYERNAME=?""", (playerName,))
        gameID = self.cur.fetchone()
        gameID = gameID[0]

        # get the playerID based on player name
        self.cur = self.conn.execute("""SELECT PLAYERID FROM Player
            WHERE PLAYERNAME=?""", (playerName,))
        playerID = self.cur.fetchone()
        playerID = playerID[0]

        # insert the shot and grab the shotID to return it to shoot function
        self.cur = self.conn.execute("""INSERT INTO Shot (GAMEID, PLAYERID)
            VALUES (?, ?);""", (gameID, playerID,))
        self.cur = self.conn.execute("""SELECT SHOTID FROM Shot
            ORDER BY SHOTID DESC""")
        shotID = self.cur.fetchone()
        shotID = shotID[0]

        self.conn.commit() # commit and close the cursor
        self.cur.close()

        return shotID

    def newTableShot(self, tableID, shotID):
        self.cur = self.conn.cursor() # open the cursor and insert IDs into tableShot
        self.cur.execute("""INSERT INTO TableShot (TABLEID, SHOTID) 
            VALUES (?, ?)""", (tableID, shotID))

        self.conn.commit()
        self.cur.close()

################################################################################
# something goes into this
class Game():
    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None, table=None):
        database = Database(reset=True)
        database.createDB() # reset the database and make a new one
        if gameID is not None and gameName is None and player1Name is None and player2Name is None:
            gameID += 1 # increment gameID if only gameID is passed in
            gameStuff = database.getGame(gameID) # call getGame

            # set player names and game name based on lower playerID values
            if gameStuff[0][0] < gameStuff[1][0]:
                self.player1Name = gameStuff[0][1]
                self.player2Name = gameStuff[1][1]
            elif gameStuff[0][0] > gameStuff[1][0]:
                self.player1Name = gameStuff[1][1]
                self.player2Name = gameStuff[0][1]
            self.gameName = gameStuff[0][2]

        elif gameID is None and gameName is not None and player1Name is not None and player2Name is not None:
            #set the names immediately when given
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name

            #database.writeTable(table)

            # call setGame to insert everything into the databases
            database.setGame(gameName, player1Name, player2Name)
        else:
            raise TypeError("""Everything must be set to None except gameID\n
                OR Only gameID must be set to None""")
    
    def calcTotalFrames(self, beforeTable, afterTable):
        # floor method for calculating frames in shoot
        totalFrames = math.floor((afterTable.time - beforeTable.time)/FRAME_INTERVAL)
        return totalFrames

    def shoot( self, gameName, playerName, table, xvel, yvel ):
        db = Database(reset=False) # open the database and open the cursor
        cur = db.conn.cursor()

        # call new shot
        shotID = db.newShot(playerName)

        # find the cueball
        foundCueBall = table.findCueBall()

        # initialize position and acceleration
        xPos = 0
        yPos = 0
        xAcc = 0
        yAcc = 0
        xPos = foundCueBall.obj.still_ball.pos.x;
        yPos = foundCueBall.obj.still_ball.pos.y;
        
        # change the type and set number to 0
        foundCueBall.type = phylib.PHYLIB_ROLLING_BALL
        foundCueBall.obj.rolling_ball.number = 0

        totaltotalFrames = 0;

        # get the velocity and the speed
        rVel = Coordinate(xvel, yvel)
        rSpeed = phylib.phylib_length(rVel)

        # recalculate acceleration like in A2
        if (rSpeed > VEL_EPSILON):
            xAcc = ((xvel * -1.0) / rSpeed) * DRAG
            yAcc = ((yvel * -1.0) / rSpeed) * DRAG

        # set all the new values
        foundCueBall.obj.rolling_ball.pos.x = xPos;
        foundCueBall.obj.rolling_ball.pos.y = yPos;
        foundCueBall.obj.rolling_ball.vel.x = xvel;
        foundCueBall.obj.rolling_ball.vel.y = yvel;
        
        foundCueBall.obj.rolling_ball.acc.x = xAcc
        foundCueBall.obj.rolling_ball.acc.y = yAcc
       
        # make a before and after table, and a total time
        beforeTable = table
        afterTable = table
        totalTime = 0.0

        tableList = []

        # while loop that breaks if the table after segment is None
        while (True):
            afterTable = afterTable.segment()
            if afterTable is None:
                break;

            # call total frames method
            totalFrames = self.calcTotalFrames(beforeTable, afterTable)
            totaltotalFrames += totalFrames
            print(totalFrames)
            for frameNum in range(totalFrames): # loop over total frames
                rollValue = frameNum*FRAME_INTERVAL # multiply current frame by frame interval
                newTable = beforeTable.roll(rollValue) # call roll on the state before segment
                # set the temporary table time to total time + what roll returns
                newTable.time = totalTime + rollValue
                tableID = db.writeTable(newTable) # write the table
                #db.newTableShot(tableID, shotID)
                cur = db.conn.execute("""INSERT INTO TableShot (TABLEID, SHOTID) 
                    VALUES (?, ?)""", (tableID+1, shotID)) # insert into TableShot
                #tableList += newTable
                

            beforeTable = afterTable # reinstate the before table to the new segment location
            totalTime = afterTable.time # set time

        # commit and close the connection
        db.conn.commit()
        cur.close()

        return totaltotalFrames;

    def gameRead(self, table, i):
        
        db = Database(reset=False) # open the database and open the cursor
        cur = db.conn.cursor()

        table = db.readTable(i)

        db.conn.commit()
        cur.close()
        return table


# class Database():

#     # This is a constructor function. It checks to see if reset is true. If it is, it removes the file first.
#     # Then, it creates a new phylib.db file and connects the cursor

#     def __init__(self, reset=False):

#         if (reset == True):
#             os.remove('phylib.db')
#         self.conn = sqlite3.connect( 'phylib.db' );
#         self.cur = self.conn.cursor()

#     # def close(self):
#     #     self.cur.close();
#     #     self.conn.commit();
#     #     self.conn.close();
        
#     # The main premise of this function is to create the various tables specified in the assignment details. 
#     # First, I connect the connection to the phylib.db file. Next I connect the cursor. Through that, I use the self.conn.execute
#     # command to create the table in a sql format. Finally, I close the cursor and commit the connection.

#     def createDB(self):
#         self.conn = sqlite3.connect( 'phylib.db' );
#         self.cur = self.conn.cursor()
#         self.cur = self.conn.execute( """CREATE TABLE IF NOT EXISTS Ball ( 
#              		BALLID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#              		BALLNO   INTEGER NOT NULL,
#              		XPOS     FLOAT NOT NULL,
#              		YPOS     FLOAT NOT NULL,
#                     XVEL     FLOAT,
#                     YVEL     FLOAT);""" );

#         self.cur = self.conn.execute( """CREATE TABLE IF NOT EXISTS TTable (
#                     TABLEID  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                     TIME     FLOAT NOT NULL);""" );

#         self.cur = self.conn.execute( """CREATE TABLE IF NOT EXISTS BallTable (
#              		BALLID   INTEGER NOT NULL,
#              		TABLEID  INTEGER NOT NULL,
#              		FOREIGN KEY (BALLID) REFERENCES Ball, 
#                     FOREIGN KEY (TABLEID) REFERENCES TTable);""" );

#         self.cur = self.conn.execute( """CREATE TABLE IF NOT EXISTS Shot (
#                     SHOTID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                     PLAYERID INTEGER NOT NULL,
#                     GAMEID   INTEGER NOT NULL, 
#                     FOREIGN KEY (PLAYERID) REFERENCES Player, 
#                     FOREIGN KEY (GAMEID) REFERENCES Game);""" );

#         self.cur = self.conn.execute( """CREATE TABLE IF NOT EXISTS TableShot ( 
#              		TABLEID   INTEGER NOT NULL,
#              		SHOTID    INTEGER NOT NULL,
#              		FOREIGN KEY (TABLEID) REFERENCES TTable, 
#                     FOREIGN KEY (SHOTID) REFERENCES Shot);""" );

#         self.cur = self.conn.execute( """CREATE TABLE IF NOT EXISTS Game (
#                     GAMEID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                     GAMENAME VARCHAR(64) NOT NULL);""" );

#         self.cur = self.conn.execute( """CREATE TABLE IF NOT EXISTS Player (
#                     PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                     GAMEID   INTEGER NOT NULL,
#                     PLAYERNAME VARCHAR(64) NOT NULL,
#              		FOREIGN KEY (GAMEID) REFERENCES Game);""" ); 
#         self.cur.close();
#         self.conn.commit();
#         #self.conn.close();                                   
#         #self.close(cur, conn)

#     #This function's main premise is to read the tables from sql. 
#     #Firstly, I create a new table object. Next, i connect a cursor to the connection
#     #Following the instructions, i made sure to increment tableID by 1 to make sure
#     # the python and SQL code match.
#     # Next, I select the ball attributes using the tableID.
#     # I check if the ballsInfo is None, and if it is, I return None back to the 
#     # calling program. 
#     # Furthemore, I have a for loop going that runs for each ball in the Table
#     # and grabs each row value. Depending on the velocities of each ball, I assign them as either
#     # Still or Rolling. If it is rolling, I make sure to do certain calculations (acc). I close the cursor and commit
#     # the connection. Finally,for each
#     # condition (still or rolling) I make sure to add the ball to the table.
#     # I return the table it self.

#     def readTable(self, tableID):
#         table = Table();
#         cur = self.conn.cursor()
#         tableID = tableID +1
#         # print("table id")
#         # print (tableID)

#         #check = SELECT 1 FROM BallTable WHERE TABLEID=tableID
#         #if(check == False):
#             #return None
#         #print(table)
#         cur = self.conn.execute("""SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL, TTable.TIME
#             FROM Ball
#             JOIN BallTable ON Ball.BALLID = BallTable.BALLID
#             JOIN TTable ON BallTable.TABLEID = TTable.TABLEID
#             WHERE BallTable.TABLEID = ?""", (tableID,))
#         #cur = self.conn.execute("""SELECT TIME FROM TTable WHERE TTable.TABLEID = ?""", (tableID));
#         #time = cur.fetchone()
#         # print("TIMEEEEE")
#         # print(time)
       
#         ballsInfo = cur.fetchall()
#         # cur = self.conn.execute("""SELECT TIME FROM TTable""");
#         # time = cur.fetchone()[0]

#         # print("ball info")
#         # print(ballsInfo)
        
#         if not ballsInfo:
#           return None

#         #ballsInfo = self.cur.fetchall()
#         #print("BALLSIFO")
#         #print(ballsInfo)
#         #balls = []
#         #table = Table();
#         for ballInfo in ballsInfo:
#         #    print("in for loop")
#            ballId, ballNo, xPos, yPos, xVel, yVel, time = ballInfo
#            #table.time = time

#         #    print("ball id")
#         #    print(ballId)
#         #    print("ball no")
#         #    print(ballNo)
#         #    print("xpos")
#         #    print(xPos)
#         #    print("ypos")
#         #    print(yPos)
#         #    print("xVel")
#         #    print(xVel)
#         #    print("yVel")
#         #    print(yVel)
#            pos = Coordinate(xPos, yPos)
#            #print(xVel)
#            #print(yVel)
#            #vel = Coordinate(xVel, yVel)
            
#            if (xVel is None) and (yVel is None):
#                 # print("in still ball")
#                 #POS = Coordinate(XPOS, YPOS) 
#                 ball = StillBall(ballNo, pos)
#                 table+=ball
#            else:
#                 # print("in rolling ball")
#                 #acc = rBallSpeed = phylib.phylib_length(rBallVel)
#                 #POS2 = Coordinate(XPOS,YPOS)
#                 #print("XVEL")
#                 #print(XVEL)
#                 #print("YVEL")
#                 #print(YVEL)
#                 #vel = Coordinate(XVEL,YVEL)
#                 ACC = Coordinate(0.0, 0.0)
                

#                 vel = Coordinate(xVel, yVel)
#                 #print("hi")

#                 acc = phylib.phylib_length(vel)
                

#                 ball = RollingBall(ballNo,pos,vel,ACC) #MAYBE CGANCE THIS
                
#                 if (acc > VEL_EPSILON):
                    
#                     ACC.x = ((vel.x * -1.0) / acc) * DRAG
                    
#                     ACC.y = ((vel.y * -1.0) / acc) * DRAG
#                 #ACC = Coordinate(xAcc,yAcc)
#                 #print("hi")
#                 table+= ball
#         table.time = time
#         cur.close();
#         self.conn.commit();
#         #self.conn.close();
#         return table


#     # In this function, we are writing to the table. First, I create a cursor that connects with the connection. Then,
#     # I have a insert statement that inserts the time into the TTable. Next, I make the tableId (autoId) equal to the lastrowid.
#     # After that, I have a for loop running for each ball in the table. I check the instance of the ball and according to what matches, 
#     # I do specific things. If the ball is an instance of StillBall, I insert into the ball the ball attributes. I make the ball id equal
#     # to the lastrowid. If the instance is a RollingBall, I do the same thing, where I insert inot the Ball Table and make the ballid equal to the
#     # lastrowId. Based on those values, for both instances, I insert information into the BallTable as well. Finally, I close the cursor, commit
#     # the connection and return table id - 1 to match python/SQL codes.

#     def writeTable(self,table):
#         cur = self.conn.cursor()

#          #Select statement for a time from TTable 
#          #find autoid after
#         cur = self.conn.execute("""INSERT INTO TTable (TIME) VALUES (?);""", (table.time,))
        
#         autoId = cur.lastrowid
#         # print("Auto id: ")
#         # print(autoId)
#         for ball in table:
#             if isinstance(ball,StillBall):
#                 cur = self.conn.execute("""INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?,?,?,?,?);""",
#                 (ball.obj.still_ball.number, ball.obj.still_ball.pos.x,ball.obj.still_ball.pos.y, None, None));
#                 ballId = cur.lastrowid
#                 # print("ball id")
#                 # print(ballId)
#                 cur = self.conn.execute("""INSERT INTO BallTable (BALLID, TABLEID) VALUES (?,?);""",(ballId, autoId));
#             if isinstance(ball,RollingBall):
#                 cur = self.conn.execute("""INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?,?,?,?,?);""",
#                 (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x,ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y));
#                 ballId = cur.lastrowid
#                 # print("ball id")
#                 # print(ballId)
#                 cur = self.conn.execute("""INSERT INTO BallTable (BALLID, TABLEID) VALUES (?,?);""",(ballId, autoId));

         
#         #autoId = self.cur.lastrowid - 1
        
#         #close()
#         cur.close();
#         self.conn.commit();
#         #self.conn.close();

#         return autoId - 1

#     # This is the close function, it closes the cursor, commits the connection and closes it.

#     def close(self):
#         self.cur.close();
#         self.conn.commit();
#         self.conn.close();

# class Game():
    
#     # This is the constructor for the Game Class. Firstly, it creates a Database, and creates a cursor for the connection. 
#     # Next, I check the parameters that were passed into the method. If the gameID is not None but everything else is, I make the 
#     # gameID increment by 1. Next, I select the rows from the game table based on the game id it self and fetch all. I also make the playerNames
#     # equal to their appropriate attributes. If the gameId is none but everything else passed into the parameter is not none, I insert values into the 
#     # appropriate tables. Else, I state that there is a TyepError. Finally, I close the cursor and commit the connection.

#     def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
#         #self.conn = sqlite3.connect( 'phylib.db' );
#         self.db = Database(reset=False);
#         cur = self.db.conn.cursor()
#         self.gameID = gameID
#         #result = []
#         if gameID is not None and gameName is None and player1Name is None and player2Name is None:
#             self.gameID = gameID + 1
            
#             cur = self.db.conn.execute("""SELECT Game.GAMEID, Game.GAMENAME, Player.PLAYERID, Player.PLAYERNAME FROM Game
#                 JOIN Player PLAYER ON Game.GAMEID = Player.GAMEID WHERE Game.GAMEID = ? ORDER BY Player.PLAYERID""", (self.gameID,))
#             result = cur.fetchall()
#             player1Name = result[0][3]
#             # print("Player 1 name")
#             # print(player1Name)
#             player2Name = result[1][3]
#         elif gameID is None and gameName is not None and player1Name is not None and player2Name is not None:
#             # print("hi")
#             self.gameID = gameID
#             self.gameName = gameName
#             self.player1Name = player1Name
#             self.player2Name = player2Name

#             cur = self.db.conn.execute("""INSERT INTO Game (GAMENAME) VALUES (?)""", (self.gameName,))
#             self.gameID = cur.lastrowid
#             # print("game id")
#             # print(self.gameID)
#             cur = self.db.conn.execute("""INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?,?)""", (self.gameID, player1Name))
#             cur = self.db.conn.execute("""INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?,?)""", (self.gameID, player2Name))
#         else:
#             raise TypeError("Arguments are not correct.")
#         cur.close()
#         self.db.conn.commit()
#         #self.conn.close()
        
#     #     else:


#     # The main premise of this shoot function is to shoot. To achieve this, I first create a cursor and connect it to the connection.
#     # Next, I retrieve the playerId based on the playername we have received in the method parameters. Next, I select the gameId based on 
#     # the game name that was received. Then, I insert the player id and the gameid into the shot function and make shot id equal to the lastrowid.
#     # For my last select statment I select the ball attirbutes when the ball no is 0 (referencing the cue ball). 
#     # In terms of calculation, I make the pos coordinate equal to the xPos and yPos of the cue ball, I make vel = to the method
#     # parameter values and acc is set to 0. Then, I call the rolling ball constructor and pass those values in.
#     # Then, I make those values equal to what was specified in the assignment instructions and i calculate the cueBall accelartion.
#     # Finally, I add the cue ball to the table. I have a while loop that runs till the table is not None.
#     # In the while loop, I create a variable called startTime which is equal to table.time. This value will be used later.
#     # Next, I create a newTable which is the value that is being returned when table.segment is being called.
#     # If the newTable is none, the loop breaks. I create another variable called endTime which is equal to the new table's time. 
#     # Furthermore, another variable is created called newTable time which is determined by subtracting start time from end time, and divided by
#     # the frame interval and rounded down. Based on that, newTime value, a for loop runs. In that for loop, I multiply the index with the frame interval constant
#     # and i call the roll function which was provided in the assignment details. In this for loop I also calculate the new table time by doing some arithemtic 
#     # and write the new table by calling the writeTable function. Finally, I retrieve specific values and insert them into the TableShot function and close the cursor
#     # and commit the connection.
    
#     def shoot(self, gameName, playerName, table, xvel, yvel):

#         #db = Database(reset=False);
#         cur = self.db.conn.cursor()
#         #self.table = table

#         #dataB = Database()
#         #select statement (player id) from Player where Player.PLAYERNAME = playerName DONE
#         cur = self.db.conn.execute("""SELECT Player.PLAYERID FROM Player WHERE Player.PLAYERNAME = ?""", (playerName,))
#         playerId = cur.fetchall()[0][0]

#         cur = self.db.conn.execute("""SELECT Game.GAMEID FROM Game WHERE Game.GAMENAME = ?""", (gameName,))
#         gameId = cur.fetchall()[0][0]

#         cur = self.db.conn.execute("""INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?,?)""",(playerId, gameId))
#         shotId = cur.lastrowid

#         # cur = self.db.conn.execute("""SELECT Shot.SHOTID FROM Shot WHERE Shot.GAMEID = ?""", (gameId,))

#         cur = self.db.conn.execute("""SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL FROM Ball WHERE Ball.BALLNO = 0""")
#         ballsInfo = cur.fetchone()

#         vel = Coordinate(xvel, yvel)
#         for ball in table:
#             #print(ball)
#             #if(isinstance(ball, (StillBall,RollingBall))):
#             if(isinstance(ball,StillBall)):
#                 if(ball.obj.still_ball.number == 0):
#                     #print("HLLO STILL")
#                     #vel = Coordinate(xvel, yvel)
#                     pos = Coordinate(ball.obj.still_ball.pos.x,ball.obj.still_ball.pos.y)
#                     #vel = Coordinate(xvel, yvel)
#                     ball.type = 1
#                     # acc = Coordinate(0.0, 0.0)
#                     # cueBall = RollingBall(0, pos, vel, acc)
#                     ball.obj.type = phylib.PHYLIB_ROLLING_BALL
#                     ball.obj.rolling_ball.number = 0
#                     ball.obj.rolling_ball.pos = pos
#                     ball.obj.rolling_ball.vel = vel
#                     rollingBallSpeed = phylib.phylib_length(vel)
                                
#                     if (rollingBallSpeed > VEL_EPSILON):
#                         ball.obj.rolling_ball.acc.x = ((vel.x * -1.0) / rollingBallSpeed) * DRAG
#                         ball.obj.rolling_ball.acc.y = ((vel.y * -1.0) / rollingBallSpeed) * DRAG
#                     #print("IN STILL")
#                     #newBall = ball
#             elif(isinstance(ball,RollingBall)):
#                 if(ball.obj.rolling_ball.number == 0):
#                     #print("HELLO ROLLING")
#                             #vel = Coordinate(xvel, yvel)
#                         # ball.type = 1
#                             # acc = Coordinate(0.0, 0.0)
#                             # cueBall = RollingBall(0, pos, vel, acc)
#                             # cueBall.obj.type = phylib.PHYLIB_ROLLING_BALL
#                     ball.obj.rolling_ball.number = 0
#                     ball.obj.rolling_ball.vel = vel
#                     rollingBallSpeed = phylib.phylib_length(vel)
                                
#                     if (rollingBallSpeed > VEL_EPSILON):
#                         ball.obj.rolling_ball.acc.x = ((vel.x * -1.0) / rollingBallSpeed) * DRAG
#                         ball.obj.rolling_ball.acc.y = ((vel.y * -1.0) / rollingBallSpeed) * DRAG
#                     #newBall = ball
#         #print("AFTER CHANGE")
#         #print(newBall)

#         #cueBall = RollingBall(0, pos, vel, acc)
#         #table += cueBall
#         #newTable = Table()
#         #startTime = table.time
#         #startTime = table.time
#         while table is not None:
#             startTime = table.time
#             #print("frameeeee")
#             #print(FRAME_INTERVAL)
#             # print(table)
#             newTable = table.segment()
#             #startTime = table.time
#             #startTime = table.time
#             #print("NEW TABLE")
#             #print(newTable)
#             #print("INNNNNNNNNNNNN WHILEEEEEEEEEEEEEEEE")
#             if newTable is None:
#                 #print("INNN IFFFFFFF")
#                 break
#             #table = table.segment()
#             endTime = newTable.time
#             #print("END TIMEEEEE") #end time is 0.001
#             #print(endTime)
#             newTime = round((endTime - startTime) / FRAME_INTERVAL) #rounds to 0, causing it to not go into for loop
#             #print("NEW TIMEMEMEMEMME")
#             #print(newTime)
#             for num in range(newTime):
#                 #print("INNNNNNNNN FOOOOOOOORRRRRRRRRRRRRRRRRRRRRRRRR")
#                 #print(num)
#                 # startTime = table.time
#                 passValue = num * FRAME_INTERVAL
#                 newTable2 = table.roll(passValue)
#                 newTable2.time = startTime + passValue
#                 tableId = self.db.writeTable(newTable2)
#                 # cur = self.db.conn.execute("""SELECT TTable.TABLEID FROM TTable WHERE TTable.TIME = ?""", (newTable.time,)) 
#                 # table = cur.fetchone()[0]
#                 cur = self.db.conn.execute("""INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?,?);""", (tableId, shotId))
#                 #print("INNNNNNNNN FOOOOOOOORRRRRRRRRRRRRRRRRRRRRRRRR")
#             table = newTable
#         cur.close()
#         self.db.conn.commit()
