#Kivy Imports
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.garden.matplotlib import FigureCanvasKivyAgg

#Image Analysis Imports
from PIL import Image as pil_Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class HomeScreen(Widget):
    global images
    global image_id
    images = []
    image_id = 1
    
    #---------------IMPORT CONTROLS------------------#
    def hide_widget(self,wid, dohide=True):
        if hasattr(wid, 'saved_attrs'):
            if not dohide:
                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
                del wid.saved_attrs
                return False
        elif dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True
            return True
    
    def __init__(self) -> None:
        super().__init__()
        filechooser = self.ids.filechooser
        self.hide_widget(filechooser,True)
        confirm_import_btn = self.ids.confirm_import_btn
        self.hide_widget(confirm_import_btn, True)

    def import_btn_pressed(self):
        #Hide image controls, images, and output
        image_controls_widget = self.ids.image_controls_widget
        image_widget = self.ids.image_widget
        output_widget = self.ids.output_widget
        self.hide_widget(image_controls_widget, True)
        self.hide_widget(image_widget, True)
        self.hide_widget(output_widget, True)

        filechooser = self.ids.filechooser
        self.hide_widget(filechooser,False)
    
    def image_selected(self, filenames):
        global images
        for file in filenames:
            if file not in images:
                images.append(file)
        confirm_import_btn = self.ids.confirm_import_btn
        self.hide_widget(confirm_import_btn,False)

    def delete_image(self,id):
        #-----NEED TO FIX-----NEED TO FIX-----NEED TO FIX-----NEED TO FIX-----NEED TO FIX
        print(id)
        image_widget = self.ids.image_widget
        for widget in image_widget.children:
            if isinstance(widget, GridLayout) and widget.id == id:
                image_widget.remove_widget(widget)

    def confirm_import_btn_pressed(self):
        # Show image controls, images, and output; hide the filechooser
        image_controls_widget = self.ids.image_controls_widget
        image_widget = self.ids.image_widget
        output_widget = self.ids.output_widget
        filechooser = self.ids.filechooser
        self.hide_widget(image_controls_widget, False)
        self.hide_widget(image_widget, False)
        self.hide_widget(output_widget, False)
        self.hide_widget(filechooser,True)

        global images
        global image_id
        
        for filename in images:
            if filename not in filechooser.selection:
                images.remove(filename)

        for filename in images:
            image_grid = GridLayout(cols=1)
            image_grid.id = image_id

            image = Image(source = filename)

            delete_btn = Button(
                text = "Delete",
                size_hint_y = None,
                height = 75
            )
            delete_btn.bind(on_press=lambda x: self.delete_image(image_grid.id))

            image_grid.add_widget(image)
            image_grid.add_widget(delete_btn)

            image_widget = self.ids.image_widget
            image_widget.add_widget(image_grid)
            image_id+=1

            print(image_grid.id)

        filechooser.selection = []
        confirm_import_btn = self.ids.confirm_import_btn
        self.hide_widget(confirm_import_btn)


    #---------------IMAGE CONTROLS------------------#
    def clear_output(self):
        output_widget = self.ids.output_widget
        for widget in output_widget.children:
            if isinstance(widget, Label): continue
            output_widget.remove_widget(widget)

    def stack(self):
        #Fixes:
        #and I need to specifically use the path of the image file to determine
        #which is which

        global images
        membrane = None
        myosin = None
        if len(images)==0:
            return True
        #----Read the images----#
        # for image in images:
        #     print(image)
        #     if "membrane" in image.lower():
        #         membrane = pil_Image.open(image)
        #     elif "myosin" in image.lower():
        #         myosin = pil_Image.open(image)
        membrane = pil_Image.open(images[0])
        myosin = pil_Image.open(images[1])

        #----Convert to NumPy arrays----#
        print(membrane)
        myosin = np.array(myosin)
        membrane = np.array(membrane)
        x = membrane.shape[0]
        y = membrane.shape[1]

        stacked_images = np.zeros((x,y,3),dtype="uint8")
        stacked_images[:,:,0] = membrane
        stacked_images[:,:,1] = myosin

        img_RGB = pil_Image.fromarray(stacked_images, 'RGB' )
        plt.imshow(img_RGB, cmap="Reds")
        output_widget = self.ids.output_widget
        output_widget.add_widget(FigureCanvasKivyAgg(plt.gcf()))
    
    def stack_checkbox_click(self, instance, value):
        global images
        if value:
            if len(images)>=2:
                self.stack()
            else:
                pass
        else:
            self.clear_output()
    
    def binarize(self):
        global images
        image = images[0]

        image = pil_Image.open(image)
        image = np.array(image)
        x = image.shape[0]
        y = image.shape[1]

        #----Manual Thresholding----#
        threshold_val = 100 #Range 0-255
        binary_image = image > threshold_val #Extract only the pixels whose magnitude is greater than the threshold value

        stacked_image2 = np.zeros((x,y,3),dtype="uint8") #Same as before
        stacked_image2[:,:,0] = binary_image * 255 #Fill in the all channels with binary image ... multiply by 255 to make it bright white
        stacked_image2[:,:,1] = binary_image * 255 
        stacked_image2[:,:,2] = binary_image * 255

        img_RGB2 = pil_Image.fromarray(stacked_image2, 'RGB')
        plt.imshow(stacked_image2) #Black and white image... white or black pixels
        output_widget = self.ids.output_widget
        output_widget.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def binarize_checkbox_click(self, instance, value):
        global images
        if value:
            if len(images)>0:
                self.binarize()
            else:
                pass
        else:
            self.clear_output()

    def trace(self):
        global images
        image = images[0]

        def trace_cell_outline(image):
            membrane = pil_Image.open(image)
            membrane = np.array(membrane)
            x = membrane.shape[0]
            y = membrane.shape[1]
            #----Tracing Cell Outline----#
            #Tracing done in MATLAB, data stored in csv files on drive. Import csv files
            path_cell_outline = "/Users/mannendriolivares/Desktop/ENG/cell_outline.csv"
            cell_outline = pd.read_csv(path_cell_outline) #Converts to Pandas dataframe... not great for image processing 
            cell_outline = cell_outline.to_numpy() #Converts Pandas dataframe to numpy array

            #Needed because size of csv is 479 by 640 and size of image is 480 by 640
            empty_row = np.zeros((1,y),dtype="uint8") #Literaly an empyty row
            cell_outline = np.vstack([empty_row, cell_outline])

            #----Cell Outline With Trace----#
            membrane_without_trace = np.zeros((x,y,3),dtype="uint8") #Same as before ... New Image
            membrane_without_trace[:,:,0] = membrane #Red Channel is the membrane image

            membrane_with_trace = np.zeros((x,y,3),dtype="uint8") #Same as before ... New Image
            membrane_with_trace[:,:,2] = cell_outline * 255 #Fill in the all channels with binary cell outline ... multiply by 255 to make it bright red
            membrane_with_trace[:,:,0] = membrane #Fill in the all channels with binary cell outline ... multiply by 255 to make it bright red

            membrane_net = np.hstack([membrane_without_trace, membrane_with_trace]) #Horizontally combine images

            plt.figure(figsize = (10,10),dpi = 200)
            plt.imshow(membrane_net) 
            plt.axis('off')
            output_widget = self.ids.output_widget
            output_widget.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        def trace_myosin(image):
            myosin = pil_Image.open(image)
            myosin = np.array(myosin)
            x = myosin.shape[0]
            y = myosin.shape[1]
            #----Tracing Myosin Network----#
            #Tracing done in MATLAB, data stored in csv files on drive. Import csv files
            path_myosin_network = "/Users/mannendriolivares/Desktop/ENG/myosin_network.csv"
            myosin_network = pd.read_csv(path_myosin_network) #Converts to Pandas dataframe... not great for image processing 
            myosin_network = myosin_network.to_numpy() #Converts Pandas dataframe to numpy array

            #Needed because size of csv is 479 by 640 and size of image is 480 by 640
            empty_row = np.zeros((1,y),dtype="uint8") #Literaly an empyty row
            myosin_network = np.vstack([empty_row, myosin_network])

            #----Myosin Network with Trace----#
            myosin_without_trace = np.zeros((x,y,3),dtype="uint8") #Same as before ... New Image
            myosin_without_trace[:,:,1] = myosin #Green Channel is the myosin image

            myosin_with_trace = np.zeros((x,y,3),dtype="uint8") #Same as before ... New Image
            myosin_with_trace[:,:,0] = myosin_network * 255 #Fill in the all channels with binary cell outline ... multiply by 255 to make it bright red
            myosin_with_trace[:,:,1] = myosin #Fill in the all channels with binary cell outline ... multiply by 255 to make it bright red

            myosin_net = np.hstack([myosin_without_trace, myosin_with_trace]) #Horizontally combine images

            plt.figure(figsize = (10,10),dpi = 200)
            plt.imshow(myosin_net)
            plt.axis('off')
            output_widget = self.ids.output_widget
            output_widget.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        if "membrane" in image.lower():
            trace_cell_outline(image)
        else:
            trace_myosin(image)

    def trace_checkbox_click(self, instance, value):
        global images
        if value:
            if len(images)>0:
                self.trace()
            else:
                pass
        else:
            self.clear_output()

    def trace_stack(self):
        #----Tracing Myosin Network and Cell Outlines----#
        #Tracing done in MATLAB, data stored in csv files on drive. Import csv files
        path_cell_outline = "/Users/mannendriolivares/Desktop/ENG/cell_outline.csv" #File paths for two csv files on drive
        path_myosin_network = "/Users/mannendriolivares/Desktop/ENG/myosin_network.csv"

        cell_outline = pd.read_csv(path_cell_outline) #Converts to Pandas dataframe... not great for image processing 
        myosin_network = pd.read_csv(path_myosin_network)

        cell_outline = cell_outline.to_numpy() #Converts Pandas dataframe to numpy array
        myosin_network = myosin_network.to_numpy()

        x = cell_outline.shape[0]
        y = cell_outline.shape[1]

        #Needed because size of csv is 479 by 640 and size of image is 480 by 640.
        empty_row = np.zeros((1,y),dtype="uint8") #Literally an empyty row
        cell_outline = np.vstack([empty_row, cell_outline]) # Adding a blank row above all other data to make it 480 by 640
        myosin_network = np.vstack([empty_row, myosin_network])

        #----Trace of Myosin Network and cell Outline----#
        x = cell_outline.shape[0]
        y = cell_outline.shape[1]

        traced_networks = np.zeros((x,y,3),dtype="uint8") #Same as before ... New Image
        traced_networks[:,:,0] = cell_outline * 255 #Fill in red channel with binary cell outline ... multiply by 255 to make it bright red
        traced_networks[:,:,1] = myosin_network * 255 #Fill in green with binary myosin network ... multiply by 255 to make it bright green

        plt.figure(figsize = (5,10),dpi = 200) #Makes the below figure larger with higher resolution
        plt.imshow(traced_networks)
        plt.axis('off')
        output_widget = self.ids.output_widget
        output_widget.add_widget(FigureCanvasKivyAgg(plt.gcf()))
    
    def trace_stack_checkbox_click(self, instance, value):
        global images
        if value:
            myosin_in_input = False
            membrane_in_input = False
            for image in images:
                if "membrane" in image.lower():
                    membrane_in_input = True
                if "myosin" in image.lower():
                    myosin_in_input = True
            if membrane_in_input and myosin_in_input:
                self.trace_stack()
            else:
                pass
        else:
            self.clear_output()

    

class CellsyApp(App):
    def build(self):
        Window.clearcolor = (190/255,155/255,242/255,1)
        return HomeScreen()

if __name__ == "__main__":
    CellsyApp().run()