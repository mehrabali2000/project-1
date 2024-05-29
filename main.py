from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.properties import StringProperty


store=JsonStore("data.json")


class Custombtn(Button):
    key_name=StringProperty()

class Interface(ScreenManager):
    
    
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.fetching_data)
        
    def truncate_string(self,str_input,max_length):
        str_end="..."
        length=len(str_input)
        if length>max_length:
            return str_input[:max_length-len(str_end)]+str_end
        else:
            return str_input
        
    def deleting(self,obj_btn):
        id=obj_btn.key_name
        self.ids.gridlayout.remove_widget(self.ids[id])
        store.delete(id)
        
            
    def fetching_data(self,dt):
        try:
            keys=store.keys()
            for key in keys:
                layout=BoxLayout(spacing="10sp",size_hint_y =None,height="80dp")
                self.ids[key]=layout
                title=Custombtn(background_color=[1,1,0,1],font_name="demiItalic.ttf",key_name=key,text=self.truncate_string(key,15))
        
                
                delete=Custombtn(background_color=[1,0.5,0,1],font_name="demiItalic.ttf",key_name=key,on_press=self.deleting,text='delete',size_hint= (None, None),size=("80dp","80dp"))
                title.bind(on_press=self.detail_screen)
                layout.add_widget(title)
                layout.add_widget(delete)
                
                self.ids.gridlayout.add_widget(layout)
                
        except:
            pass
    
    
    def back_btn(self):
        self.current="Main Screen"
        
        store.put(self.ids.Notice_title.text,data=self.ids.input_data.text)
    
    def detail_screen(self,btn_obj):
        self.ids.Notice_title.text=btn_obj.key_name
        self.ids.input_data.text=store.get(btn_obj.key_name)["data"]
        self.current="Details Screen"
        
    
    
    def addItem(self,obj):
        self.popup.dismiss()
        layout=BoxLayout(spacing="10sp",size_hint_y =None,height="80dp")
        keys=store.keys()
            
        title=Custombtn(background_color=[1,1,0,1],font_name="demiItalic.ttf",key_name=self.txt.text,text=self.truncate_string(self.txt.text,15))
            
        
        delete=Custombtn(background_color=[1,0.5,0,1],font_name="demiItalic.ttf",on_press=self.deleting,key_name=self.txt.text,text='delete',size_hint= (None, None),size=("80dp","80dp"))
        self.ids[self.txt.text]=layout
        title.bind(on_press=self.detail_screen)
        layout.add_widget(title)
        layout.add_widget(delete)
        
        store.put(self.txt.text,data="")
        
        self.ids.gridlayout.add_widget(layout)
        
    def show_popup(self):
        
        layout=BoxLayout(orientation= 'vertical',padding="16dp",spacing="16dp")
        
        self.popup=Popup(background_color=[0.5,1,0.5,1],title="Notice Title",size_hint= (.8,None),height= "180dp",content=layout)
        self.popup.open()
        
        btn=Button(border=[5,5,5,5],font_name="demiItalic.ttf",text='Submit',background_color=[0.2,0.5,1,1])
        btn.bind(on_press=self.addItem)
        self.txt=TextInput(multiline=False)
        
        layout.add_widget(self.txt)
        layout.add_widget(btn)
            
        

class TodoApp(App):
    pass

TodoApp().run()
