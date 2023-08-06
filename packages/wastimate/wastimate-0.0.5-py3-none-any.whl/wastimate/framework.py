# -*- coding: utf-8 -*-
"""
Created on Mon May 29 13:46:05 2023

@author: hando
"""

import numpy as np
import scipy.stats as sc
import matplotlib as mpl
import matplotlib.pyplot as plt

class Node:
    def __init__(self, Distribution, timestep=1):
        # Generate some initial list of values.
        self.NodeDist = Distribution
        self.timestep = timestep
        self.NodeState = self.NodeDist.rvs(self.timestep)[0]
        
    def reset(self):
        self.NodeState = self.NodeDist.rvs(self.timestep)[0]


class Link:
    def __init__(self, HomeObj, AwayObj, Distribution, VRF=sc.uniform(loc=1, scale=0), LinkType="Fixed", timestep=10):
        self.HomeObj  = HomeObj
        self.AwayObj  = AwayObj
        self.VRF      = VRF
        self.Dist     = Distribution
        self.LinkType = LinkType
        
        self.timestep  = timestep
        self.LinkState = self.Dist.rvs(self.timestep)
        self.VRFState  = self.VRF.rvs(self.timestep)
        
    def reset(self):
        self.LinkState = self.Dist.rvs(self.timestep)
        self.VRFState  = self.VRF.rvs(self.timestep)


class Settings:
    def __init__(self):
        self.timestep = 10 # how long to run a simulation
        self.batches  = 10 # how many simulations to run

class Universe:
    def __init__(self, Nodes=[], Links=[], Settings=Settings()):
        self.Nodes = Nodes
        self.Links = Links
        self.Settings = Settings
        
        self.GlobalStateHistory = []
        self.GlobalStateDistribution = []
        
        # Formulate the system.
        self.InitialState = []
        self.SimTime = 0


    def reset(self):
        # Formulate the system.
        self.InitialState = []
        
        # Order the objects according to an index (state order), and generate three of the necessary states.
        self.NodeDict = dict()
        for idx, node in enumerate(self.Nodes):
            node.reset()
            self.InitialState.append(node.NodeState)
            self.NodeDict[node] = idx
        
        # Pregenerate null lists for all.
        self.StateLinkFixed = [[0 for _ in range(len(self.Nodes))] for _ in range(len(self.Nodes))]
        self.StateLinkProp  = [[0 for _ in range(len(self.Nodes))] for _ in range(len(self.Nodes))]
        self.StateLinkRel   = [[1 for _ in range(len(self.Nodes))] for _ in range(len(self.Nodes))]

        for link in self.Links:
            link.timestep = self.Settings.timestep; link.reset()
            
            if link.LinkType == "fixed":
                self.StateLinkFixed[self.NodeDict[link.HomeObj]][self.NodeDict[link.AwayObj]] = link.LinkState
            else:
                self.StateLinkProp[self.NodeDict[link.HomeObj]][self.NodeDict[link.AwayObj]] = link.LinkState

            self.StateLinkRel[self.NodeDict[link.HomeObj]][self.NodeDict[link.AwayObj]] = link.VRFState

        # Convert rest of the connections to list of zeroes.
        for idx_list, nested_list in enumerate(self.StateLinkFixed):
            for idx_element, element in enumerate(nested_list):
                if isinstance(element, int):
                    self.StateLinkFixed[idx_list][idx_element] = [0] * self.Settings.timestep
                    
        for idx_list, nested_list in enumerate(self.StateLinkProp):
            for idx_element, element in enumerate(nested_list):
                if isinstance(element, int):
                    self.StateLinkProp[idx_list][idx_element] = [0] * self.Settings.timestep
                    
        for idx_list, nested_list in enumerate(self.StateLinkRel):
            for idx_element, element in enumerate(nested_list):
                if isinstance(element, int):
                    self.StateLinkRel[idx_list][idx_element] = [1] * self.Settings.timestep
        
        self.StateLinkFixed = np.array(self.StateLinkFixed)
        self.StateLinkProp = np.array(self.StateLinkProp)
        self.StateLinkRel = np.array(self.StateLinkRel)
        
    
    def __add__(self, Obj):
        if isinstance(Obj, Node):
            if Obj not in self.Nodes:
                self.Nodes.append(Obj)
        
        if isinstance(Obj, Link):
            if Obj not in self.Links:
                self.Links.append(Obj)
        
        if isinstance(Obj, Settings):
            if Obj != self.Settings:
                self.Settings = Obj
        
        return self

    
    def __sub__(self, Obj):
        if isinstance(Obj, Node):
            self.Nodes.remove(Obj)
        
        if isinstance(Obj, Link):
            self.Links.remove(Obj)
        
        if isinstance(Obj, Settings):
            if Obj != self.Settings:
                self.Settings = Settings()
        
        return self  


    def run(self, PreviousState=[]):
        if len(PreviousState) ==  0:
            State          = self.InitialState[:]
            StateLinkFixed = self.StateLinkFixed
            StateLinkProp  = self.StateLinkProp
            StateLinkRel   = self.StateLinkRel
            StateHistory = [State[:]]
        else:
            State          = list(PreviousState[-1])
            StateLinkFixed = self.StateLinkFixed
            StateLinkProp  = self.StateLinkProp
            StateLinkRel   = self.StateLinkRel
            StateHistory = list(PreviousState)

        for timestep in range(self.Settings.timestep):
            NewState = State[:]
        
            for idxState, s in enumerate(State):
                
                if s == 0:
                    continue
            
                for idxLink, link in enumerate(StateLinkFixed[idxState]):
                    
                    compensator = 0
                    if NewState[idxState] < link[timestep]:
                        compensator = NewState[idxState] - link[timestep]
        
                    NewState[idxState] -= (link[timestep] + compensator) * StateLinkRel[idxState][idxState][timestep]
                    NewState[idxLink]  += (link[timestep] + compensator) * StateLinkRel[idxState][idxLink][timestep]
                    
                for idxLink, link in enumerate(StateLinkProp[idxState]):
                    
                    compensator = 0
                    if NewState[idxState] < link[timestep] * State[idxState]:
                        compensator = NewState[idxState] - link[timestep]  * NewState[idxState]
        
                    NewState[idxState] -= (link[timestep] * NewState[idxState] + compensator) * StateLinkRel[idxState][idxState][timestep]
                    NewState[idxLink]  += (link[timestep] * NewState[idxState] + compensator) * StateLinkRel[idxState][idxLink][timestep]
            
            State = NewState[:]
            StateHistory.append(State[:])
        
        self.GlobalStateHistory.append(StateHistory)


    def simulate(self, timestep=False):
        if timestep != False:
            temp_timestep = self.Settings.timestep
            self.Settings.timestep = timestep
        
        if len(self.GlobalStateHistory) == 0:
            for num_of_batches in range(self.Settings.batches):
                self.reset()
                self.run()
        else:
            TempStateHistory  = self.GlobalStateHistory[:,:,:]
            self.GlobalStateHistory = []
            for batch_number in range(self.Settings.batches):
                self.reset()
                self.run(TempStateHistory[batch_number,:,:])
            
        self.GlobalStateHistory = np.array(self.GlobalStateHistory)
        self.SimTime += self.Settings.timestep
        
        if timestep != False:
            self.Settings.timestep = temp_timestep
    
    def get_timeseries(self, Obj, batch)  -> "array containing the timeseries":
        return self.GlobalStateHistory[batch,:,self.NodeDict[Obj]]
    
    def get_batch(self, Obj, timestep)  -> "array containing the batch":
        return self.GlobalStateHistory[:,timestep,self.NodeDict[Obj]]


    def Plot(self, Obj, bin_number=100, filename="", colormap="jet", scale="lin"):
        
        image = []
        data = np.transpose(self.GlobalStateHistory[:,:,self.NodeDict[Obj]])
        min_value = np.min(data)
        max_value = np.max(data)
        
            
        for row in data:
            tmax = self.SimTime
                
            hist, bin_edges = np.histogram(row, bins=bin_number, range=(min_value, max_value))
            image.append(hist)
            
        image = np.transpose(image)
                
        fig, ax = plt.subplots(figsize=(10,6))
        if scale == "log":
            im = ax.imshow(image, norm=mpl.colors.LogNorm(), aspect="auto", origin="lower",
                      cmap=colormap, interpolation='antialiased', extent=[0, tmax, min_value, max_value])
        else:
            im = ax.imshow(image, aspect="auto", origin="lower",
                      cmap=colormap, interpolation='antialiased', extent=[0, tmax, min_value, max_value])
            
        plt.xlabel("Time", fontsize=12)
        plt.ylabel("Simulated Value", fontsize=12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        
        cbar = plt.colorbar(im)
        cbar.ax.tick_params(labelsize=12)
        cbar.set_label('Number of Occurences', fontsize=12)
        
        if filename != "":
            plt.savefig(f'{filename}.png')
        else:
            plt.show()


if __name__ == "__main__":

    Node1 = Node(sc.uniform(loc=3, scale=2))
    Node2 = Node(sc.uniform(loc=0, scale=0))
    Node3 = Node(sc.uniform(loc=0, scale=0))

    Link12 = Link(Node1, Node2, sc.uniform(loc=0.05, scale=0.07), LinkType="fixed")
    Link23 = Link(Node2, Node3, sc.uniform(loc=0.03, scale=0.05), LinkType="var")
    Link31 = Link(Node3, Node1, sc.uniform(loc=0.04, scale=0.01), LinkType="var")

    settings = Settings()
    settings.batches = 1000

    verse = Universe() + Node1 + Node2 + Node3 + Link12 + Link23 + Link31 + settings
    verse.simulate(100)
    
    verse.Plot(Node3, scale="log")