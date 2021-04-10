from pynput import keyboard
from pynput.mouse    import Listener  as MouseListener
import sched, time
import sys
from tkinter import *

class dynaList(object):
	"""docstring for ClassName"""
	def __init__(self, start):
		self.list = []
		self.list += [startTime]

	def __repr__(self):
		return str(self.list)

	def add(self, item):
		newList = [item]
		# print(newList)
		for i in range(len(self.list)):
			if(i < 9):
				newList += [self.list[i]]
		self.list = newList

	def getLen(self):
		return len(self.list)

	def getDiff(self):
		return self.list[0] - self.list[-1]
		
startTime = time.monotonic()
count = 0
lastKey = 0
active = False
lastActions = dynaList(startTime)

root = Tk()
root.title("APM Tracker")
draw = Canvas(root, 
            width=400, 
            height=100)
draw.pack(side=TOP)
message = draw.create_text(10, 
            100/2,
            text="num=start/stop",
            anchor="w", font="Courier 20 bold")
draw.configure(bg='#00b140')

def on_click(x, y, button, pressed):
	if(pressed):
		global active
		if(active):
		    global count
		    global lastActions
		    lastActions.add(time.monotonic())
		    count += 1
		    print("Average APM: " + str(int(count/((time.monotonic()-startTime)/60))))
		    print("APM: "+str(int((lastActions.getLen()/lastActions.getDiff())*(60/lastActions.getDiff()))))
		    draw.itemconfig(message,text="Average APM:" + str(int(count/((time.monotonic()-startTime)/60)))+\
		    "\nCurrent APM:" + str(int((lastActions.getLen()/lastActions.getDiff())*60)))
		    print("Actions: " + str(count) +" Time: " + str(int(time.monotonic()-startTime)))

def on_release(key):
    if key == keyboard.Key.num_lock:
        # Stop listener
        global active
        global count
        global startTime
        global lastKey
        global root
        global draw
        global message
        if(active == True):
        	active = False
        	print("Tracking stopped")
        	if(int(time.monotonic()-startTime) % 60 > 10):
	        	draw.itemconfig(message,text="Final APM:" + str(int(count/((time.monotonic()-startTime)/60))) \
	        		+ "\nFinal Time: " + str(int((time.monotonic()-startTime) / 60)) + ":" + str(int(time.monotonic()-startTime) % 60) )
        	else:
	        	draw.itemconfig(message,text="Final APM:" + str(int(count/((time.monotonic()-startTime)/60))) \
	        		+ "\nFinal Time:" + str(int((time.monotonic()-startTime) / 60)) + ":0" + str(int(time.monotonic()-startTime) % 60) )
        	print("Average APM: " + str(int(count/((time.monotonic()-startTime)/60))))
        else: 
        	active = True
        	startTime = time.monotonic()
        	count = 0
        	print("Tracking started")
        	draw.itemconfig(message,text="Average APM:" + str(0) + "\nCurrent APM:0")
    if(key!=lastKey):
	    if(active and time.monotonic()-startTime != 0):
		    lastKey = key
		    lastActions.add(time.monotonic())
		    count += 1
		    print("Average APM: " + str(int(count/((time.monotonic()-startTime)/60))))
		    print("APM: "+str(int((lastActions.getLen()/lastActions.getDiff())*(60/lastActions.getDiff()))))
		    draw.itemconfig(message,text="Average APM:" + str(int(count/((time.monotonic()-startTime)/60)))+\
		    "\nCurrent APM:" + str(int((lastActions.getLen()/lastActions.getDiff())*60)))
		    print("Actions: " + str(count) +" Time: " + str(int(time.monotonic()-startTime)))

with keyboard.Listener(on_release=on_release) as k_listener, \
        MouseListener(on_click=on_click) as m_listener:
    root.mainloop()
    # s.run()
    k_listener.join()
    m_listener.join()  
