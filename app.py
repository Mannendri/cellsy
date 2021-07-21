import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image

class HomeScreen(Widget):
    def import_image(self):
        filechooser = self.ids.filechooser
        filechooser.size_hint_y = 1
        filechooser.height = 200

        img = self.ids.img
        img.size_hint_y = 1
        img.height = 200
        print("Import Image")
    
    def selected(self, filename):
        try:
            self.ids.img.source = filename[0]
            print(filename[0])
        except:
            pass

class CellsyApp(App):
    def build(self):
        return HomeScreen()

if __name__ == "__main__":
    CellsyApp().run()