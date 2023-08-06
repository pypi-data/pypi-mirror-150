from pyanc350.v4 import Positioner
import numpy as np
import time
from IPython.display import clear_output
import threading
import ipywidgets as widgets

ax = {'x':0,'y':1,'z':2}
#define a dict of axes to make things simpler



def get_input():
    global button
    while True:
        newValue = input('Stop? (Y/N) ')
        time.sleep(1)
        if (newValue == 'Y'):
            button = False
        if (button == False):
            break

def Read_Position(axis_index):
    anc = Positioner()
    clear_output(wait=True)
    print(anc.getPosition(ax[axis_index])*1e6)
    anc.disconnect()

def SingleStageMove(axis_index, real_target, tolerance, go_back):
    global button
    button = True
    thread1 = threading.Thread(target=get_input)
    thread1.start()
    outs = widgets.Output()
    display(outs)
    with outs:
        anc = Positioner()
        clear_output(wait=True)
    target_pos = real_target - go_back
    
    anc.setAxisOutput(ax[axis_index], 1, 0)
    anc.setTargetRange(ax[axis_index], tolerance/1e6)
    anc.setTargetPosition(ax[axis_index], target_pos/1e6)
    time.sleep(0.5)
    target = 0
    while target == 0:
        if (button == False):
            anc.disconnect()
            break
        with outs:
            clear_output(wait=True)
            connected, enabled, moving, target, eotFwd, eotBwd, error = anc.getAxisStatus(ax[axis_index]) #find bitmask of status
            if target == 0:
                print('axis moving, currently at',anc.getPosition(ax[axis_index])*1e6)
            elif target == 1:
                print('axis arrived at',anc.getPosition(ax[axis_index])*1e6)
        time.sleep(0.5)
    
    if (button == True):
        target_pos = real_target
        anc.setAxisOutput(ax[axis_index], 1, 0)
        anc.setTargetRange(ax[axis_index], tolerance/1e6)
        anc.setTargetPosition(ax[axis_index], target_pos/1e6)
        time.sleep(0.5)
        target = 0
        while target == 0:
            if (button == False):
                anc.disconnect()
                break
            with outs:
                clear_output(wait=True)
                connected, enabled, moving, target, eotFwd, eotBwd, error = anc.getAxisStatus(ax[axis_index]) #find bitmask of status
                if target == 0:
                    print('axis moving, currently at',anc.getPosition(ax[axis_index])*1e6)
                elif target == 1:
                    print('axis arrived at',anc.getPosition(ax[axis_index])*1e6)
            time.sleep(0.5)
        anc.disconnect()
        thread1.join()
    
def DoubleStageMove(axis_index_x, real_target_x, tolerance_x, go_back_x, axis_index_y, real_target_y, tolerance_y, go_back_y):
    global button
    button = True
    thread1 = threading.Thread(target=get_input)
    thread1.start()
    outs = widgets.Output()
    display(outs)
    with outs:
        anc = Positioner()
        clear_output(wait=True)
    target_x = real_target_x - go_back_x
    target_y = real_target_y - go_back_y
    anc.setAxisOutput(ax[axis_index_x], 1, 0)
    anc.setTargetRange(ax[axis_index_x], tolerance_x/1e6)
    anc.setTargetPosition(ax[axis_index_x], target_x/1e6)
    anc.setAxisOutput(ax[axis_index_y], 1, 0)
    anc.setTargetRange(ax[axis_index_y], tolerance_y/1e6)
    anc.setTargetPosition(ax[axis_index_y], target_y/1e6)
    time.sleep(0.5)
    target_1 = 0
    target_2 = 0
    while (target_1 == 0) or (target_2 == 0):
        if (button == False):
            anc.disconnect()
            break
        with outs:
            clear_output(wait=True)
            connected, enabled, moving, target_1, eotFwd, eotBwd, error = anc.getAxisStatus(ax[axis_index_x])
            connected, enabled, moving, target_2, eotFwd, eotBwd, error = anc.getAxisStatus(ax[axis_index_y])
            if (target_1 == 0) or (target_2 == 0):
                print('axis moving, currently at (',anc.getPosition(ax[axis_index_x])*1e6,',',anc.getPosition(ax[axis_index_y])*1e6,')')
            elif (target_1 == 1) and (target_2 == 1):
                print('axis arrived at (',anc.getPosition(ax[axis_index_x])*1e6,',',anc.getPosition(ax[axis_index_y])*1e6,')')
        time.sleep(0.5)

    
    if (button == True):
        target_x = real_target_x
        target_y = real_target_y
        anc.setAxisOutput(ax[axis_index_x], 1, 0)
        anc.setTargetRange(ax[axis_index_x], tolerance_x/1e6)
        anc.setTargetPosition(ax[axis_index_x], target_x/1e6)
        anc.setAxisOutput(ax[axis_index_y], 1, 0)
        anc.setTargetRange(ax[axis_index_y], tolerance_y/1e6)
        anc.setTargetPosition(ax[axis_index_y], target_y/1e6)
        time.sleep(0.5)
        target_1 = 0
        target_2 = 0
        while (target_1 == 0) or (target_2 == 0):
            if (button == False):
                anc.disconnect()
                break
            with outs:
                clear_output(wait=True)
                connected, enabled, moving, target_1, eotFwd, eotBwd, error = anc.getAxisStatus(ax[axis_index_x])
                connected, enabled, moving, target_2, eotFwd, eotBwd, error = anc.getAxisStatus(ax[axis_index_y])
                if (target_1 == 0) or (target_2 == 0):
                    print('axis moving, currently at (',anc.getPosition(ax[axis_index_x])*1e6,',',anc.getPosition(ax[axis_index_y])*1e6,')')
                elif (target_1 == 1) and (target_2 == 1):
                    print('axis arrived at (',anc.getPosition(ax[axis_index_x])*1e6,',',anc.getPosition(ax[axis_index_y])*1e6,')')
            time.sleep(0.5)
        anc.disconnect()
        thread1.join()
