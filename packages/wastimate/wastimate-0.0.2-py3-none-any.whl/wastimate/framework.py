# -*- coding: utf-8 -*-
"""
Created on Mon May 29 13:46:05 2023

@author: hando
"""

import numpy as np
import scipy.stats as sc

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
    def __init__(self, Nodes, Links, Settings):
        self.Nodes = Nodes
        self.Links = Links
        self.Settings = Settings
        
        self.GlobalStateHistory = []
        
        # Formulate the system.
        self.InitialState = []
        
        # Order the objects according to an index (state order), and generate three of the necessary states.
        NodeDict = dict()
        for idx, node in enumerate(Nodes):
            node.reset()
            self.InitialState.append(node.NodeState)
            NodeDict[node] = idx
        
        # Pregenerate null lists for all.
        self.StateLinkFixed = [[0 for _ in range(len(Nodes))] for _ in range(len(Nodes))]
        self.StateLinkProp  = [[0 for _ in range(len(Nodes))] for _ in range(len(Nodes))]
        self.StateLinkRel   = [[1 for _ in range(len(Nodes))] for _ in range(len(Nodes))]

        for link in Links:
            link.timestep = self.Settings.timestep; link.reset()
            
            if link.LinkType == "Fixed":
                self.StateLinkFixed[NodeDict[link.HomeObj]][NodeDict[link.AwayObj]] = link.LinkState
            else:
                self.StateLinkProp[NodeDict[link.HomeObj]][NodeDict[link.AwayObj]] = link.LinkState
            
            self.StateLinkRel[NodeDict[link.HomeObj]][NodeDict[link.AwayObj]] = link.VRFState

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


    def reset(self):
        # Formulate the system.
        self.InitialState = []
        
        # Order the objects according to an index (state order), and generate three of the necessary states.
        NodeDict = dict()
        for idx, node in enumerate(self.Nodes):
            node.reset()
            self.InitialState.append(node.NodeState)
            NodeDict[node] = idx
        
        # Pregenerate null lists for all.
        self.StateLinkFixed = [[0 for _ in range(len(self.Nodes))] for _ in range(len(self.Nodes))]
        self.StateLinkProp  = [[0 for _ in range(len(self.Nodes))] for _ in range(len(self.Nodes))]
        self.StateLinkRel   = [[1 for _ in range(len(self.Nodes))] for _ in range(len(self.Nodes))]

        for link in self.Links:
            link.timestep = self.Settings.timestep; link.reset()
            
            if link.LinkType == "Fixed":
                self.StateLinkFixed[NodeDict[link.HomeObj]][NodeDict[link.AwayObj]] = link.LinkState
            else:
                self.StateLinkProp[NodeDict[link.HomeObj]][NodeDict[link.AwayObj]] = link.LinkState
            
            self.StateLinkRel[NodeDict[link.HomeObj]][NodeDict[link.AwayObj]] = link.VRFState

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


    def run(self):
        State          = self.InitialState[:]
        StateLinkFixed = self.StateLinkFixed
        StateLinkProp  = self.StateLinkProp
        StateLinkRel   = self.StateLinkRel
        
        StateHistory = [State[:]]

        for timestep in range(self.Settings.timestep):
            NewState = State[:]
        
            for idxState, s in enumerate(State):
                
                if s == 0:
                    continue
            
                for idxLink, link in enumerate(StateLinkFixed[idxState]):
                    
                    compensator = 0
                    
                    if NewState[idxState] < link[timestep]:
                        compensator = State[idxState] - link[timestep]
        
                    NewState[idxState] -= (link[timestep] + compensator) * StateLinkRel[idxState][idxState][timestep]
                    NewState[idxLink]  += (link[timestep] + compensator) * StateLinkRel[idxState][idxLink][timestep]
                    
                for idxLink, link in enumerate(StateLinkProp[idxState]):
                    
                    compensator = 0
                    if NewState[idxState] < link[timestep] * NewState[idxState]:
                        compensator = State[idxState] - link[timestep]  * State[idxState]
        
                    NewState[idxState] -= (link[timestep] * State[idxState] + compensator) * StateLinkRel[idxState][idxState][timestep]
                    NewState[idxLink]  += (link[timestep] * State[idxState] + compensator) * StateLinkRel[idxState][idxLink][timestep]
            
            State = NewState[:]
            StateHistory.append(State[:])
        
        self.GlobalStateHistory.append(StateHistory)


    def simulate(self, vocal=False):
        for num_of_batches in range(self.Settings.batches):
            self.run()
            self.reset()
            
        self.GlobalStateHistory = np.array(self.GlobalStateHistory)

# Generate gazilion different scenarios. Later on combine the timesteps to display a distribution of values.


#Node1 = Node(sc.uniform(loc=1, scale=2))
#Node2 = Node(sc.uniform(loc=0, scale=2))

#Link12 = Link(Node1, Node2, sc.uniform(loc=0.15, scale=0.25), LinkType="Var")

#settings = Settings()
#settings.timestep = 10
#settings.batches = 100

#verse = Universe([Node1, Node2], [Link12], settings)

#verse.simulate()

#import matplotlib.pyplot as plt
#for i in range(len(verse.GlobalStateHistory)):
#   
#    plt.plot(verse.GlobalStateHistory[i][:,0])



