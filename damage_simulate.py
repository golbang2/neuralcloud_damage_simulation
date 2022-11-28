# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 00:48:59 2022

@author: atgol
"""

import numpy as np

class Hubble:
    def __init__(self,target = 1, duration = 30):
        self.atk = 582
        self.speed = 120
        self.power = 529
        self.crit_p = 0.1
        self.crit_m = 1.5
        
        self.psv_attackcount = 0
        self.psv_stack = 0
        self.next_attack = 1/(self.speed*0.01)
        self.active_cooldown = 10
        self.next_active = 4
        
        self.elapsed = 0
        self.dmg = 0
        self.target = target
        self.done = 0
        self.duration = duration
        
    def attack(self):
        self.elapsed = self.next_attack
        
        self.psv_attackcount+=1
        if self.psv_attackcount==3:
            self.psv_attackcount=0
            self.psv_stack = np.min((5,self.psv_stack+1))
        
        dmg = int(self.atk * (1+self.psv_stack*0.06))
        if np.random.random()<self.crit_p:
            dmg = int(dmg * self.crit_m)
        
        self.next_attack = self.elapsed + 1/(self.speed*0.01)
        self.dmg += dmg
        
        return dmg
        
    def skill(self):
        self.elapsed = self.next_active
        main_target = self.power * 4
        sub_target = (self.target - 1) * self.power * 4 * 0.3
        self.next_active = self.elapsed + 10
        dmg = int(main_target + sub_target)
        self.dmg += dmg
        return dmg
    
    def action(self):
        if self.next_active<self.next_attack:
            self.skill()
        else:
            self.attack()
        
        if self.elapsed>=self.duration:
            self.done = 1

class Chanzhi:
    def __init__(self,target = 1, duration = 30):
        self.atk = 581
        self.speed = 130
        self.power = 485
        self.crit_p = 0.1
        self.crit_m = 1.5
        
        self.psv_stack = 0
        self.next_attack = 1/(self.speed*0.01)
        self.active_cooldown = 12
        self.next_active = 5
        
        self.elapsed = 0
        self.dmg = 0
        self.target = target
        self.done = 0
        self.buff = 0
        self.duration = duration
        
    def attack(self):
        self.elapsed = self.next_attack
        self.psv_stack +=1
        dmg = self.atk
        if np.random.random()<self.crit_p:
            dmg = int(dmg * self.crit_m)
        
        self.next_attack = self.elapsed + 1/(self.speed*0.01)
        self.dmg += dmg
        self.next_active-=1/(self.speed*0.01)
        return dmg
    
    def skill(self):
        self.buff = 6
    
    def buff_attack(self):
        self.elapsed = self.next_attack
        self.psv_stack += self.target
        dmg = int(self.atk * 1.2) * self.target
        self.next_attack = self.elapsed + 1/(self.speed*0.01) 
        self.buff -= 1/(self.speed*0.01) 
        self.next_active = self.active_cooldown
        if self.buff<0:
            self.close_skill()
        self.dmg += dmg
        return dmg
        
    def close_skill(self):
        dmg = self.atk * 0.4 * self.psv_stack
        self.psv_stack = 0
        self.dmg += dmg
        self.next_active = self.active_cooldown
        return dmg
    
    def action(self):
        if self.next_active<0:
            self.skill()
        if self.buff>0:
            self.buff_attack()
        else:
            self.attack()
            
        if self.elapsed>=self.duration:
            self.done = 1
        

if __name__=='__main__':
    duration = 30
    target = 1
    iteration = 1000
    dmg = 0
    
    for i in range(iteration):
        #doll = Hubble(target = target, duration = duration)
        doll=Chanzhi(target = target,duration = duration)
        while not doll.done:
            doll.action()
        dmg += doll.dmg/duration
    print(dmg/iteration)
    