import tkinter as tk
from PIL import ImageTk,Image
from typing import List

class GifPlayer:
    def __init__(self, root, label,width, height):
        self.frames = 0
        self.loop_frame = 0

        self.root = root
        self.label = label
        self.width = width
        self.height = height

    def Play(self, gif, loopBool, loopFrame = None):
        self.image_Objects = self.__getFrames(gif)
        
        if loopBool:
            self.__loopAnimation()
            if loopFrame != None: 
                self.loop_frame = loopFrame
            else:
                self.loop_frame = 0
        else:
            self.__playAnimation()
            
    def Stop(self):
        if 'loop' in globals():
                self.root.after_cancel(loop)

    def __playAnimation(self, current_frame = 0):
        global loop

        image = self.image_Objects[current_frame]
            
        self.label.configure(image=image)
        current_frame = (current_frame + 1) % self.frames

        if current_frame == 0:
             self.Stop()
             return

        loop = self.root.after(50, self.__loopAnimation, current_frame)
        
    def __loopAnimation(self, current_frame = 0):
            global loop

            image = self.image_Objects[current_frame]
    
            self.label.configure(image=image)
            next_frame = (current_frame + 1) % self.frames
            current_frame = self.loop_frame if next_frame == 0 else next_frame
    
            loop = self.root.after(50, self.__loopAnimation, current_frame)

    def __getFrames(self,gif):
                info = Image.open(gif)
                self.frames = info.n_frames
        
                photoimage_objects = []
                for i in range(self.frames):
                    info.seek(i)
                    
                    frame = Image.new("RGBA", info.size, (0, 0, 0, 0))
                    frame.paste(info.convert("RGBA"), (0, 0), info.convert("RGBA"))
                    
                    if self.width > 1 and self.height > 1:
                        frame = frame.resize((self.width, self.height), Image.Resampling.LANCZOS)
                    
                    photoimage_objects.append(ImageTk.PhotoImage(frame))
                    
    
                return photoimage_objects