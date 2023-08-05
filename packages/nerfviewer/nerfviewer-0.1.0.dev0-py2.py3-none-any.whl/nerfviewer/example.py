#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Dylan Wootton and Josh Pollock.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget, Output
import ipywidgets as widget
from traitlets import Unicode, Dict, Float, List, traitlets, Int
from ._frontend import module_name, module_version
import numpy as np
from IPython.display import display
from scipy.spatial.transform import Slerp
from scipy.spatial.transform import Rotation as R
from scipy.interpolate import interp1d
import imageio
from tqdm import tqdm
from base64 import b64encode

trans_t = lambda t : np.array([
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,t],
    [0,0,0,1],
], dtype=np.float32)

rot_phi = lambda phi : np.array([
    [1,0,0,0],
    [0,np.cos(phi),-np.sin(phi),0],
    [0,np.sin(phi), np.cos(phi),0],
    [0,0,0,1],
], dtype=np.float32)

rot_theta = lambda th : np.array([
    [np.cos(th),0,-np.sin(th),0],
    [0,1,0,0],
    [np.sin(th),0, np.cos(th),0],
    [0,0,0,1],
], dtype=np.float32)

def pose_spherical(theta, phi, radius):
    c2w = trans_t(radius)
    c2w = rot_phi(phi/180.*np.pi) @ c2w
    c2w = rot_theta(theta/180.*np.pi) @ c2w
    c2w = np.array([[-1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]) @ c2w
    return c2w

def lerp_frames(keyframes, num_tweens):
    interp_times = np.linspace(0., len(keyframes) - 1, (num_tweens + 1) * len(keyframes))

    rotationTuples = list(map(lambda kf: [
      kf['coordinates']['theta'],
      kf['coordinates']['phi']
    ], keyframes))

    zooms = list(map(lambda kf: kf['coordinates']['radius'], keyframes))

    slerp = Slerp(range(len(keyframes)), R.from_euler('xy', rotationTuples, degrees=True))
    zoomlerp = interp1d(range(len(keyframes)), zooms)
    
    rotationFrames = slerp(interp_times).as_euler('xyz', degrees=True)[:, :2]
    zoomFrames = zoomlerp(interp_times)
    return [{ 'theta': r[0], 'phi': r[1], 'radius': z } for (r, z) in zip(rotationFrames, zoomFrames)]

def render(nerf_render, inframes, H, W, focal, outfile='video.mp4',):
    outframes = []
    for frame in tqdm(list(inframes)):
        rgb, depth, acc = nerf_render(H, W, focal, frame)
        outframes.append((255*np.clip(rgb,0,1)).astype(np.uint8))

    imageio.mimwrite(outfile, outframes, fps=30, quality=7)

def play(file='video.mp4'):
    mp4 = open(file,'rb').read()
    data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
    return HTML("""
    <video width=400 controls autoplay loop>
          <source src="%s" type="video/mp4">
    </video>
    """ % data_url)

class NerfNav(DOMWidget):
    _model_name = Unicode('ExampleModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('ExampleView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    # Your widget state goes here. Make sure to update the corresponding
    # JavaScript widget state (defaultModelProperties) in widget.ts
    value = Unicode('Jupyter').tag(sync=True)
    color = Unicode('blue').tag(sync=True)
    view = Unicode('navigation').tag(sync=True)
    foo = Unicode('bar').tag(sync=True)

    cameraCoordinates = Dict(per_key_traits={
      "theta": Float(),
      "phi": Float(),
      "radius": Float(),
    }, default_value={'theta': 100, 'phi': -30, 'radius': 4}).tag(sync=True)
    # TODO: need to call render on the initial data to get the intial version here
    imageArray = List(Int()).tag(sync=True)

    keyframes = List(
        Dict(per_key_traits={
        "image":List(Int()),
        "coordinates":Dict(per_key_traits={
            "theta": Float(),
            "phi": Float(),
            "radius": Float(),
        })
    }),default_value=[]).tag(sync=True)
   
    videoNum = Int(0).tag(sync=True)
    playNum = Int(0).tag(sync=True)
    videoString = Unicode().tag(sync=True)

    # out = Output()
    # display(out)

    # @traitlets.observe('cameraPosition')
    # @out.capture()
    # def _observe_cameraPosition(self,change):
    #     # todo: fill in this to call prediction_fn on the new camera position
    #     print(change)
    #     rgb, depth, acc = self.render(self.H, self.W, self.focal, **change['new'])
    #     self.imageArray = np.clip(rgb,0,1).ravel().tolist()
    #     # 
    #     # send to js app, new image to display 

    #@traitlets.observe('keyframes')
    #def _observe_keyframes(self,change):
        #print('keyframes',self.keyframes)
        
        # print(len(self.imageArray), max(self.imageArray))

    @traitlets.observe('cameraCoordinates')
    def _observe_cameraPosition(self,change):
        # print(change)
        rgb, depth, acc = self.render(self.H, self.W, self.focal, change['new'])
        self.imageArray = (255 * np.clip(rgb,0,1)).astype(int).ravel().tolist()
        # print(len(self.imageArray), max(self.imageArray))

    # @traitlets.default('imageArray')
    def init_imageArray(self):
        # print('initializing imageArray...')
        rgb, depth, acc = self.render(self.H, self.W, self.focal, self.cameraCoordinates)
        self.imageArray = (255 * np.clip(rgb,0,1)).astype(int).ravel().tolist()
        # print(len(self.imageArray), max(self.imageArray))

    @traitlets.observe('videoNum')
    def _observe_videoNum(self, _change):
        print('about to render frames',len(self.keyframes))
        print('actual kf',self.keyframes)

        render(self.render, lerp_frames(self.keyframes, 23), self.H, self.W, self.focal)

    # @traitlets.observe('value') # when traitlet "value" changes, run this function
    # def _observe_value(self, change):
    #     print(change)
    #     self.color = self.model('changed')#change['new'].capitalize()

    @traitlets.observe('playNum')
    def play(self, _change):
      file = 'video.mp4'
      mp4 = open(file,'rb').read()
      self.videoString = b64encode(mp4).decode()

    def __init__(self, render, H, W, focal, keyframes=[]):
        """Widget for creating a UI for analysis of nerfs"""
        self.render = render
        self.H = H
        self.W = W
        self.focal = focal
        if len(keyframes) > 0:
            for frame in keyframes:

                coordinates = frame["coordinates"]
                rgb, depth, acc = self.render(self.H, self.W, self.focal, coordinates)
                frame['image'] = imageArray = (255 * np.clip(rgb,0,1)).astype(int).ravel().tolist()
                
            self.keyframes = keyframes




        self.init_imageArray()

        super(NerfNav, self).__init__()

    '''
    ignore: dylan WIP stuff
    out = Output()
    display(out)

    
    @out.capture()
    def on_value_change(self,change):
        print(change)
        self.view = 'changed'#change['new'].capitalize()

    @traitlets.observe('cameraPosition')
    def _observe_cameraPosition(self,change):
        # todo: fill in this to call prediction_fn on the new camera position
        print(change)
        # 
        # send to js app, new image to display 

    @traitlets.observe('value') # when traitlet "value" changes, run this function
    def _observe_value(self, change):
        print(change)
        self.color = self.model('changed')#change['new'].capitalize()
        
    def __init__(self, prediction_fn):
        """Widget for creating a UI for analysis of nerfs"""
        self.model =  prediction_fn 
        
        super(NerfNav, self).__init__()
    '''