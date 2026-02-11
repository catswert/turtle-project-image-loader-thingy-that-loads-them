import turtle as trtl
import csv #csv junk
import os #ditto

#this code takes like 10 seconds to load becasue it must make 157,170 stamps to make one image


W, H = 315, 498
S = 2
PIXELS = W * H #find total pixels in an image


#code to load the csv file data
BASE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE, "all_frames.csv")

with open(CSV_PATH, newline="") as f:
    data = [row[0].strip() for row in csv.reader(f) if row] #data list that contains hex code colors from csv
#end of csv load code

FRAME_COUNT = len(data) // PIXELS #finds total number of frames if trying to load gif image

wn = trtl.Screen() #make turtle code starts
wn.setup(width=W * S, height=H * S) #make image frame be size of image times size of pixel
wn.tracer(0, 0)  # manual refresh (more stable + faster)

renderer = trtl.Turtle() #start turtle
renderer.hideturtle() #make turtle invisible
renderer.penup() #lift pen
renderer.speed(0) #max speed
renderer.shape("square") #make square pixels
renderer.shapesize(S / 20, S / 20, 1) # pixel size scaler

x_left = -(W * S) / 2 #left edge
y_top  =  (H * S) / 2 #top edge

frame = 0 
stamp_ids = []  # store stamp ids so we can delete them safely

def draw_frame(): #method that makes each frame (rember def is like method in java)
    global frame, stamp_ids #make these global variavles

    # delete previous stamps (more reliable than clearstamps in some builds)
    for sid in stamp_ids: #stamp delete loop
        try: #try used for stable, if it always did it might get confused and try to kill a stapm stwice, but that would be bad
            renderer.clearstamp(sid)
        except Exception: #if it doesnt work jsut ignore it
            pass
    stamp_ids = [] #reset tge list each frame

    base = frame * PIXELS #find the starting pixel in case its a gif so it has pixels for much frames

    for p in range(PIXELS): #loop to iterate each pixel
        col = p % W # find the column and
        row = p // W # find row

        x = x_left + col * S + S / 2 
        y = y_top  - row * S - S / 2 

        renderer.goto(x, y) #move to tge next spot
        renderer.color(data[base + p]) #get the pixel color based on the csv
        stamp_ids.append(renderer.stamp()) 

    wn.update() #redo screen

    frame = (frame + 1) % FRAME_COUNT #this lets us loop frames

# IMPORTANT: start drawing AFTER Tk is ready or we lag and crash to death
wn.ontimer(draw_frame, 1) #this is like a thing that makes the code not  go ceraze and die
wn.mainloop()
