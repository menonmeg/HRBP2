import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')

#Set 1 ft^3 workspace up in mm
ax.set(xlim=[-152.4,152.4],ylim=[0,304.8],zlim=[0,304.8])
ax.set_xlabel('X axis (mm)')
ax.set_ylabel('Y axis (mm)')
ax.set_zlabel('Z axis (mm)')

#Paper Coordinates, set these based on 4x4 matrix 

paper_x = [-101.6,101.6,101.6,-101.6,-101.6]
paper_y = [304.8,304.8,304.8,304.8,304.8]
paper_z = [0.0,0.0,279.4,279.4,0.0]


#Plot Paper
line, = ax.plot(paper_x,paper_y,paper_z)


#Plot Pen
pen_x = [-50.8,-50.8]
pen_y = [304.8,152.4]
pen_z = [101.6,101.6]
ax.plot(pen_x,pen_y,pen_z,color='c',linewidth=5)


#Plot Robot Frame
robot_x = [-152.4,152.4,152.4,-152.4,-152.4]
robot_y = [152.4,152.4,152.4,152.4,152.4]
robot_z = [0.0,0.0,304.8,304.8,0.0]
ax.plot(robot_x,robot_y,robot_z,color='r',linewidth=3)

#Square coordinates: Can change this to draw any coordinates you want 
coords = [[-50.8,304.8,101.6],[0,304.8,101.6],[50.8,304.8,101.6],[50.8,304.8,152.4],[50.8,304.8,203.2],[0,304.8,203.2],[-50.8,304.8,203.2],[-50.8,304.8,152.4],[-50.8,304.8,101.6]]


#Generate Square Function
def Gen_Square(length=9, dims=3):

    lineData = np.empty((dims, length))

    lineData[:,0] = coords[0]
    lineData[:,1] = coords[1]
    lineData[:,2] = coords[2]
    lineData[:,3] = coords[3]
    lineData[:,4] = coords[4]
    lineData[:,5] = coords[5]
    lineData[:,6] = coords[6]
    lineData[:,7] = coords[7]
    lineData[:,8] = coords[8]

    return lineData

#Update Line function
def update_lines(num, dataLines, lines):
    for line, data in zip(lines, dataLines):
        # NOTE: there is no .set_data() for 3 dim data...
        line.set_data(data[0:2, :num])
        line.set_3d_properties(data[2, :num])

    return lines

data = [Gen_Square(9,3)]

point, = ax.plot([coords[0][0]],coords[0][1],coords[0][2], 'co')

lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]

#Animate line
line_ani = animation.FuncAnimation(fig, update_lines, 25, fargs=(data, lines),
                                   interval=150, blit=False)
def ani(hold):
    point.set_data([hold[0]],[hold[1]])
    point.set_3d_properties(hold[2])
    return point

def frames():
    for i in coords:
	yield i

#Animate Pen
ani = animation.FuncAnimation(fig, ani, frames=frames, interval=150)

plt.show()
