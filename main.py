from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from filesharer import FileSharer
import time
from kivy.core.clipboard import Clipboard
import webbrowser


Builder.load_file("frontend.kv")


class CameraScreen(Screen):

    def start(self):
        """Starts camera and changes button to say stop"""
        self.ids.camera.play = True
        self.ids.start_stop.text = "Stop Camera"
        self.ids.camera.opacity = 1

    def stop(self):
        """Stops camera and changes button to say start"""
        self.ids.camera.play = False
        self.ids.start_stop.text = "Start Camera"
        self.ids.camera.texture = None
        self.ids.camera.opacity = 0

    def capture(self):
        """Captures a picture and saves this as a file named as
         the current date and time, changes the screen to image Screen"""
        current_time = time.strftime('%Y%m%d-%H%M%S')
        filename = f"{current_time}.png"
        self.ids.camera.export_to_png(filename)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = filename


class ImageScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.link_message = 'Create a link first'

    def create_link(self):
        file_path = self.manager.current_screen.ids.img.source
        self.img_url = FileSharer(file_path).share()
        self.ids.link.text = self.img_url
        self.ids.copy_link.text = 'Copy Link'
        self.ids.open_link.text = "Open Link"
        self.ids.create_link.text = "Created!"

    def copy_link(self):
        try:
            Clipboard.copy(self.img_url)
            self.ids.copy_link.text = 'Copied!'
        except:
            self.ids.link.text = self.link_message

    def open_link(self):
        try:
            webbrowser.open(self.img_url)
            self.ids.open_link.text = 'Opened!'
        except:
            self.ids.link.text = self.link_message


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):

        return RootWidget()


MainApp().run()





