
from kivymd.app import MDApp 
import requests
import json
from kivy.core.window import Window
from kivy.uix.recycleview import RecycleView 
from kivymd.uix.pickers import MDDatePicker
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import TwoLineListItem
from kivy.properties import ListProperty, StringProperty
from kivy.utils import get_color_from_hex
from kivy.animation import Animation

class MyItem(TwoLineListItem):
    pass
    
class ScrnMngr(ScreenManager):
    def __init__(self, **kwargs):
        super(ScrnMngr, self).__init__(**kwargs)
        self.caller = ''
        self.present_folder = StringProperty("None")
        self.present_folder = "None"
        Window.bind(on_keyboard=self._key_handler)
   
    
    def _key_handler(self, instance, key, *args):
        if key == 27:
            self.set_previous_screen()
            return True
    def set_previous_screen(self):
        if self.current != 'profile':
            self.transition.direction = 'right'
            self.current = self.previous()

    def change_theme(self):
        if app.theme_cls.theme_style == 'Light':
            app.theme_cls.theme_style = 'Dark'
        else:
            app.theme_cls.theme_style = 'Light'
            
    def back_to_home(self):
        self.current = 'profile'
        
    def search_folder(self, text):
        rv = app.root.ids.rv
        url = 'https://hospital-database-2525d-default-rtdb.firebaseio.com/.json'
        
        data = requests.get(url)
        data = data.json()
        
        rv.data = []
        for k,l in data.items():
            for i,j in l.items():
                if text in str(i):
                    rv.data.append(
                        {
                            'text': str(i), 
                            'secondary_text': str(k),
                            'icon': "account",
                            "callback": lambda x: x,                              
                            
                        }
                    )
    
    def upload(self):
        name = str(app.root.ids.name.text)
        age = str(app.root.ids.age.text)
        sex = str(app.root.ids.sex.text)
        occupation = str(app.root.ids.occupation.text)
        maritalStatus = str(app.root.ids.maritalStatus.text)
        address = str(app.root.ids.address.text)
        tribe = str(app.root.ids.tribe.text)
        height = str(app.root.ids.height.text)
        weight = str(app.root.ids.weight.text)
        BMI = str(app.root.ids.BMI.text)
        bloodPressure= str(app.root.ids.BP.text)
        LMP = str(app.root.ids.LMP.text)
        EDD = str(app.root.ids.EDD.text)
        gynaeHistory = str(app.root.ids.gynaeHistory.text)
        medicalHistory = str(app.root.ids.medicalHistory.text)
        rv = app.root.ids.rv
        
        json_data = {
            'name': name,
            'age': age,
            'sex': sex,
            'occupation': occupation,
            'maritalStatus': maritalStatus,
            'address': address,
            'tribe': tribe,
            'height': height,
            'weight': weight,
            'BMI': BMI,
            'bloodPressure': bloodPressure,
            'LMP': LMP,
            'EDD': EDD,
            'gynaeHistory': gynaeHistory,
            'medicalHistory': medicalHistory
        }
            
       
        data = {name: json_data}
        
        url = 'https://hospital-database-2525d-default-rtdb.firebaseio.com/.json'
        requests.post(url=url, json=data)
        
        rv.data.append({'text': str(name), 'icon': 'account'})
        self.current = 'profile'
    
      
    def on_save(self, instance, value, date_range):
        
        print(instance, value, date_range)
        object = instance
        app.root.ids.EDD.text = f"{value.day}/{value.month}/{value.year}"
    def on_save1(self, instance, value, date_range):
        
        print(instance, value, date_range)
        object = instance
        app.root.ids.LMP.text = f"{value.day}/{value.month}/{value.year}"

    def on_cancel(self, instance, value):
        pass

    def show_datePicker(self,instance):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    def show_datePicker1(self,instance):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save1, on_cancel=self.on_cancel)
        date_dialog.open()

                
class HospitalDatabaseApp(MDApp): 
    title = 'Hospital Database'
    textColor = ListProperty((0,0,1))
    overlay_color = get_color_from_hex("#6042e4")
    
    def on_start(self):
        url = 'https://hospital-database-2525d-default-rtdb.firebaseio.com/.json'
        json_data = {
            "name": "dibe",
            "age": "14"
        }
        payload = {"name": "dibe"}

        json_data = {"diamond":json_data}
        requests.post(url, json_data)

        data = requests.get(url)
        data = data.json()
        app.folders = data
                
        for i,j in app.folders.items():
            for k,l in j.items():
                item = TwoLineListItem(text = str(k))
                item.secondary_text = str(i)
                self.root.ids.selection_list.add_widget(item)

    
    def build(self): 
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Green'
        self.textColor = [0,0,0,1]
        
        self.folders = {}
        
    def set_selection_mode(self, instance_selection_list, mode):
        if mode:
            md_bg_color = self.overlay_color
            left_action_items = [
                [
                    "close",
                    lambda x: self.root.ids.selection_list.unselected_all(),
                ]
            ]
            right_action_items = [["trash-can"]]
        else:
            md_bg_color = (0, 0, 0, 1)            
            left_action_items = []
            right_action_items = []
            
            self.root.ids.toolbar.title = self.title

        Animation(d=0.2).start(self.root.ids.toolbar)
        self.root.ids.toolbar.left_action_items = left_action_items
        self.root.ids.toolbar.right_action_items = right_action_items

    def on_selected(self, instance_selection_list, instance_selection_item):
        self.root.ids.toolbar.title = str(
            len(instance_selection_list.get_selected_list_items())
        )

    def on_unselected(self, instance_selection_list, instance_selection_item):
        if instance_selection_list.get_selected_list_items():
            self.root.ids.toolbar.title = str(
                len(instance_selection_list.get_selected_list_items())
            )


if __name__ == '__main__':
    app = HospitalDatabaseApp()
    app.run()

