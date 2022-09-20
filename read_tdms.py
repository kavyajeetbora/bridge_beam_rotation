from nptdms import TdmsFile
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from shapely.geometry import LineString
from shapely import affinity
import numpy as np

def read_tdms_data(filename, side="AMR"):
    
    '''
    Reading the data from a tdms file format to a pandas.DataFrame
    '''

    data_dict = {}
    with TdmsFile.open(filename) as tdms_file:
        group = tdms_file["Log"]
        
        for i in range(1,5):
            data_dict[f'B{i}'] = group[f"{side}-INC-BU{i}-01"][:]
        
    return DataFrame(data_dict)


class AnimateBridge2D:
    
    def __init__(self, beam_length, angles, origin=(0,0)):
        
        self.len = beam_length
        self.angles = angles
        self.fig, self.ax = plt.subplots(figsize=(5,5))
        self.origin = origin
        self.beams = [self.make_beam() for _ in range(4)]
        self.colors = ["red", "blue", "green", "orange"]
    
    def make_beam(self):
        b0 = LineString([self.origin, (self.len, 0)])
        return b0
    
    def init(self):
    
        x0, y0 = np.array(self.beams[0].coords.xy)
        beam_plot = self.ax.plot(x0,y0, color='blue')

        self.ax.set_xlabel("x")
        self.ax.set_label("y")
        self.ax.grid()

    def update(self, i):
        self.ax.cla()
        i = int(i)
        current_angles = self.angles[i,:] ## Current angle
        
        for j, curr_ang in enumerate(current_angles):   
            b1 = affinity.rotate(self.beams[j], angle=curr_ang, origin=self.origin)
            x1,y1 = np.array(b1.coords.xy)
            self.ax.plot(x1, y1, color=self.colors[j], label=f"Beam {j+1}: {curr_ang:.4f}")
            self.ax.legend(title="Beam rotations:", fancybox=True, loc="upper left")
            self.ax.set_ylim(0,self.len)
            self.ax.set_xlim(0,self.len)
            self.ax.axis("off")
                        
        return self.ax 
    
    def animate(self, interval=300, frames=None):
        if frames is None:
            frames = np.arange(len(self.angles))
            
        ani = animation.FuncAnimation(self.fig, self.update, frames=frames, init_func=self.init, interval=interval)
        plt.close()
        return ani

class AnimateStats:
    
    def __init__(self, angles):

        self.angles = angles
        self.fig, self.ax = plt.subplots(figsize=(15,6))
        self.colors = ["red", "blue", "green", "orange"]
        
    def init(self):
        pass

    def update(self, i):
        self.ax.cla()
        i = int(i)
        current_angles = self.angles[i,:] ## Current angle
        bp = 0.01 ## Bar plot constant
        norm_angles = current_angles-current_angles.min() + bp
        min_a, max_a = norm_angles.min(), norm_angles.max()
        
        self.ax.bar(["B1", "B2", "B3", "B4"], norm_angles, color=self.colors, width=0.5)        
        
        rects = self.ax.patches
        for i,(norm_ang, ang, rect) in enumerate(zip(norm_angles, current_angles, rects)):
            height = rect.get_height()
            self.ax.text(x=i,y=height*1.05, s=f"{ang:.4f}", horizontalalignment='center', fontsize=12)
        self.ax.set_xlabel("beam rotation")
        self.ax.set_label("angle")
        self.ax.set_yticks([], [])
        
        for side in ["left", "right", "top"]:   
            self.ax.spines[side].set_visible(False)
                        
        return self.fig 
    
    def animate(self, interval=300, frames=None):
        if frames is None:
            frames = np.arange(len(self.angles))
            
        ani = animation.FuncAnimation(self.fig, self.update, frames=frames, init_func=self.init, interval=interval)
        plt.close()
        return ani


