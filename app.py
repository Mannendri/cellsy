#Kivy Imports
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.garden.matplotlib import FigureCanvasKivyAgg

#Image Analysis Imports
from PIL import Image as pil_Image
import matplotlib.pyplot as plt
import numpy as np

global images
images = []

class HomeScreen(Widget):

    def import_btn_pressed(self):
        filechooser = self.ids.filechooser
        filechooser.size_hint_y = 1
    
    def image_selected(self, filename):
        try:
            global images
            for file in filename:
                images.append(file)
        except:
            pass
    
    def confirm_import_btn_pressed(self):
        filechooser = self.ids.filechooser
        filechooser.size_hint_y = None
        filechooser.height = 0
        for filename in images:
            image = Image(source = filename
            )
            image_widget = self.ids.image_widget
            image_widget.add_widget(image)
        filechooser.selection = []

    def stack_images_2_color_channels(self):
        global images
        #----Read the images----#
        myosin = pil_Image.open(images[-1])
        membrane = pil_Image.open(images[0])

        #----Convert to NumPy arrays----#
        myosin = np.array(myosin)
        membrane = np.array(membrane)
        x = membrane.shape[0]
        y = membrane.shape[1]

        stacked_images = np.zeros((x,y,3),dtype="uint8")
        stacked_images[:,:,0] = membrane
        stacked_images[:,:,1] = myosin

        img_RGB = pil_Image.fromarray(stacked_images, 'RGB' )
        plt.imshow(img_RGB, cmap="Reds")
        image_widget = self.ids.image_widget
        image_widget.add_widget(FigureCanvasKivyAgg(plt.gcf()))
    
    def stack_images_checkbox_click(self, instance, value):
        if value:
            self.stack_images_2_color_channels()
        else:
            pass

class CellsyApp(App):
    def build(self):
        return HomeScreen()

if __name__ == "__main__":
    CellsyApp().run()