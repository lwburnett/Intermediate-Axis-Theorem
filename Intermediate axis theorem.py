"""Import libraries"""
from visual import * #visual library
from visual.graph import * #graphing library
import math #math library

"""Scene specifications"""
scene.width = 700
scene.height = 500
scene.range = 6

"""Create book object"""

book = box(pos=(-3,0,0), size=(2.0,3.5,1.0), omega=vector(2.0,0.001,0.001), mass=5.0, color=color.yellow)

"""Define parameters and constants"""

lambda1 = (book.mass/12)*(book.size.y*book.size.y+book.size.z*book.size.z)  #calculating the moments of inertia
lambda2 = (book.mass/12)*(book.size.x*book.size.x+book.size.z*book.size.z)
lambda3 = (book.mass/12)*(book.size.x*book.size.x+book.size.y*book.size.y)

t = 0
dt = .001
k = 1000 #will be used as our rate in the while loop

"""Create axis objects"""

xaxis = arrow(pos=(-3,0,0), axis=(2,0,0), shaftwidth=.1, color=color.red, opacity=.5)
yaxis = arrow(pos=(-3,0,0), axis=(0,2.75,0), shaftwidth=.1, color=color.green, opacity=.5)
zaxis = arrow(pos=(-3,0,0), axis=(0,0,1.5), shaftwidth=.1, color=color.blue, opacity=.5)

axis_List = []    #putting the axis in a list for simplicity
axis_List.append(xaxis)
axis_List.append(yaxis)
axis_List.append(zaxis)

"""Create vector objects"""

xvec = arrow(pos=(2,0,0), length=(lambda1*book.omega.x)/3, axis=(1,0,0), shaftwidth=.1, color=color.red, opacity=.7)  
yvec = arrow(pos=(2+xvec.length,0,0), length=(lambda1*book.omega.y)/3, axis=(0,1,0), shaftwidth=.1, color=color.green, opacity=.7)
zvec = arrow(pos=(2+xvec.length,yvec.length,0), length=(lambda1*book.omega.z)/3, axis=(0,0,1), shaftwidth=.1, color=color.blue, opacity=.7)

totvec = arrow(pos=(2,0,0), length=sqrt(xvec.length*xvec.length+yvec.length*yvec.length+zvec.length*zvec.length), axis=norm((xvec.length,yvec.length,zvec.length)), shaftwidth=.2, color=color.yellow)

vector_List = [] #putting vectors in list for simplicity
vector_List.append(xvec)
vector_List.append(yvec)
vector_List.append(zvec)
vector_List.append(totvec)

"""Create plot"""

p_x = gcurve(color=color.red)
p_y = gcurve(color=color.green)
p_z = gcurve(color=color.blue)
p_tot = gcurve(color=color.yellow)

plot_List = [] #putting plot curves in list for simplicity
plot_List.append(p_x)
plot_List.append(p_y)
plot_List.append(p_z)
plot_List.append(p_tot)

"""Define functions"""

def find_omega_dot(w):  #function for finding omegadot using Euler's equations
    w1_dot = (lambda2-lambda3)*w.y*w.z/lambda1
    w2_dot = (lambda3-lambda1)*w.z*w.x/lambda2
    w3_dot = (lambda1-lambda2)*w.x*w.y/lambda3
    w_dot = vector(w1_dot, w2_dot, w3_dot)
    return(w_dot)
    
def update_omega(w,wdot): #updating angular momentum
    w.x = w.x + dt*wdot.x
    w.y = w.y + dt*wdot.y
    w.z = w.z + dt*wdot.z

def rotate_book(obj):   #rotating the book in the graphics
    obj.rotate(angle=mag(obj.omega)*dt, axis=norm(obj.omega), origin=obj.pos)

def update_axis(List,w): #rotating the vectors and adjusting length to be proportional to angular momentum
        for i in range(len(List)):
            List[i].rotate(angle=mag(w)*dt, axis=norm(w), origin=List[i].pos)

def update_vectors(List):
    for i in range(len(List)-1):
        List[i].length = abs((lambda1*book.omega[i])/3.) #The graphics freak out if I get rid of this absolute value
        if i>0:
            List[i].pos.x = 2+List[0].length
            if i>1:
                List[i].pos.y = List[1].length
    List[3].axis = norm((List[0].length, List[1].length, List[2].length))
    List[3].length = sqrt(List[0].length*List[0].length+List[1].length*List[1].length+List[2].length*List[2].length)

def update_plot(pList, w, time):
    pList[0].plot(pos=(time, w.x*lambda1))
    pList[1].plot(pos=(time, w.y*lambda2))
    pList[2].plot(pos=(time, w.z*lambda3))
    pList[3].plot(pos=(time, sqrt(w.x*w.x*lambda1*lambda1+w.y*w.y*lambda2*lambda2+w.z*w.z*lambda3*lambda3)))

##def change_rate(time,val):
##    if 6.5 < time < 6.65:
##        if val > 40:
##            val -= 20
##    if 6.65 <= time:
##        if val < 1000:
##            val += 40
            

"""While loop"""

while true:
    rate(k)
    omega_dot = find_omega_dot(book.omega)
    update_omega(book.omega, omega_dot)
    rotate_book(book)
    update_axis(axis_List, book.omega)
    update_vectors(vector_List)
    update_plot(plot_List, book.omega, t)
##    change_rate(t, k)
    t += dt
