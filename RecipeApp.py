from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

class MainScreen(Screen):
    pass

class CaloriesScreen(Screen):
    pass

class categoriesScreen(Screen):
    pass

class loginScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass

class shoppingListScreen(Screen):
    pass

class theScreenManager(ScreenManager):
    pass

root_widget = Builder.load_string('''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

theScreenManager:
    transition: FadeTransition()
    MainScreen:
    CaloriesScreen:
    shoppingListScreen:
    RegisterScreen:

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Name'
            font_size: 50
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size
            
        Button:
            text: 'Calories'
            color: 0.18, .5, .92, 1
            font_size: 30
            on_release: app.root.current = 'calories'
            background_normal: ""
            
        Button:
            text: 'Recipes'
            font_size: 30
            background_normal: ""
            background_color: 0.18, .5, .92, 1
            
        Button:
            text: 'Shopping List'
            color: 0.18, .5, .92, 1
            font_size: 30
            on_release: app.root.current = 'shopping'
            background_normal: ""

<CaloriesScreen>:
    name: 'calories'
    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .3
            Button:
                text: '<'
                size_hint: .1, 1
                font_size: 75
                background_normal: ""
                background_color: 0.18, .5, .92, 1
                on_release: app.root.current = 'main' 

            Label:
                text: 'Calories'
                halign: 'left'
                font_size: 50
                canvas.before:
                    Color:
                        rgb: 0.18, .5, .92
                    Rectangle:
                        pos: self.pos
                        size: self.size
            Widget:
                size_hint: .1, 1
                canvas.before:
                    Color:
                        rgb: 0.18, .5, .92
                    Rectangle:
                        pos: self.pos
                        size: self.size

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .4
            spacing: 50
            canvas.before:
                Color:
                    rgb: 0.8, 0.8, 0.8
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: 'Recipes'
                font_size: 30
                color: 0.18, .5, .92, 1


            Button:
                id: btn
                text: 'Select a recipe...'
                font_size: 30
                on_release: dropdown.open(self)
                height: '48dp'
                pos_hint: { 'top' : 0.75}
                size_hint: .8, .5

            DropDown:

                id: dropdown
                on_parent: self.dismiss()
                on_select: btn.text = '{}'.format(args[1])


                Button:
                    text: 'First recipe'
                    size_hint_y: None
                    height: '48dp'
                    on_release: dropdown.select('First Item')

                Button:
                    text: 'Second recipe'
                    size_hint_y: None
                    height: '48dp'
                    on_release: dropdown.select('Second Item')

                Button:
                    text: 'Third recipe'
                    size_hint_y: None
                    height: '48dp'
                    on_release: dropdown.select('Third Item')


            Button:
                text: '+'
                font_size: 30
                background_normal: ""
                background_color: 0.18, .5, .92, 1
                pos_hint: { 'top' : 0.65}
                size_hint: .1, .3
                #on_release:
            Widget:
                size_hint: .02, 1

        BoxLayout:
            orientation: 'vertical'
            canvas.before:
                Color:
                    rgb: 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            size_hint: 1, 1
            BoxLayout:
                orientation: 'horizontal'
                Label:
                    text: 'Food'
                    font_size: 30
                    color: 0.18, .5, .92, 1
                Label:
                    text: 'Cal'
                    font_size: 30
                    color: 0.18, .5, .92, 1
            BoxLayout:
                orientation: 'horizontal'
                Label:
                    text: 'Simple Cheese Omelette'
                    font_size: 30
                    color: 0.18, .5, .92, 1
                Label:
                    text: '241'
                    font_size: 30
                    color: 0.18, .5, .92, 1
            BoxLayout:
                orientation: 'horizontal'
                Label:
                    text: 'Burger'
                    font_size: 30
                    color: 0.18, .5, .92, 1
                Label:
                    text: '295'
                    font_size: 30
                    color: 0.18, .5, .92, 1
            BoxLayout:
                orientation: 'horizontal'
                Label:
                    text: 'Tomato and caper linguine '
                    font_size: 30
                    color: 0.18, .5, .92, 1
                Label:
                    text: '393'
                    font_size: 30
                    color: 0.18, .5, .92, 1
        BoxLayout:
            orientation: 'vertical'
            canvas.before:
                Color:
                    rgb: 0.8, 0.8, 0.8
                Rectangle:
                    pos: self.pos
                    size: self.size
            size_hint: 1, .3
            BoxLayout:
                orientation: 'horizontal'
                Label:
                    text: 'Total Cal'
                    font_size: 30
                    color: 0.18, .5, .92, 1
                Label:
                    text: '929'
                    font_size: 30
                    color: 0.18, .5, .92, 1
            BoxLayout:
                orientation: 'horizontal'
                padding: 10
                Button:
                    text: 'Clear'
                    font_size: 30
                    background_normal: ""
                    background_color: 0.18, .5, .92,
                    size_hint: .1, 1.3
                    pos_hint: {'top': 1}
                    #on_release:
                Label:
                    text: 'You are under calories'
                    font_size: 25
                    color: 0.18, .5, .92, 1

<shoppingListScreen>:
    name: 'shopping'
    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .3
            Button:
                text: '<'
                size_hint: .1, 1
                font_size: 75
                background_normal: ""
                background_color: 0.18, .5, .92, 1
                on_release: app.root.current = 'main' 

            Label:
                text: 'Login'
                halign: 'left'
                font_size: 50
                canvas.before:
                    Color:
                        rgb: 0.18, .5, .92
                    Rectangle:
                        pos: self.pos
                        size: self.size
            Widget:
                size_hint: .1, 1
                canvas.before:
                    Color:
                        rgb: 0.18, .5, .92
                    Rectangle:
                        pos: self.pos
                        size: self.size
        BoxLayout:
            orientation: 'horizontal'
            BoxLayout:
                size_hint: .2, 1
                canvas.before:
                    Color:
                        rgb: 1, 1, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
            GridLayout:
                cols: 2
                size_hint: 0.8, 1
                pos_hint: {'center_x': 0.5}
                spacing: 20
                padding: 0, 20
                _cell_height: dp(90)
                canvas.before:
                    Color:
                        rgb: 1, 1, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    text: 'Username:'
                    height: self.parent._cell_height
                    font_size: 25
                    color: 0.18, .5, .92, 1
                    size_hint: 0.3, None
                BoxLayout:
                    padding: 0, dp(20)
                    size_hint: 0.5, None
                    height: self.parent._cell_height
                    TextInput:
                        font_size: 20
                        multiline: False
                Label:
                    text: 'Password:'
                    height: self.parent._cell_height
                    font_size: 25
                    color: 0.18, .5, .92, 1
                    size_hint: 0.3, None
                    
                BoxLayout:
                    padding: 0, dp(20)
                    size_hint: 0.5, None
                    height: self.parent._cell_height
                    TextInput:
                        font_size: 20
                        multiline: False
                        password: True
            BoxLayout:
                size_hint: .2, 1
                canvas.before:
                    Color:
                        rgb: 1, 1, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size

        BoxLayout:
            orientation: 'vertical'
            size_hint: 1, .3
            canvas.before:
                Color:
                    rgb: 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
        
            Label:
                text: 'Your username or password are incorrect'
                pos_hint:{'center_x': 0.5}
                font_size: 25
                color: 0.18, .5, .92, 1
                size_hint: 0.3, None
        BoxLayout:
            padding: 0, 20
            canvas.before:
                Color:
                    rgb: 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            orientation: 'vertical'
            size_hint: 1, .4
            Button:
                text: 'Login'
                font_size: 30
                background_normal: ""
                background_color: 0.18, .5, .92, 1
                size_hint: .1, .05
                pos_hint: {'center_x': 0.5}
                #on_release:
        Button:
            text: 'Register'
            font_size: 35
            size_hint: 1, .3
            background_normal: ""
            background_color: 0.18, .5, .92, 1
            on_release: app.root.current = 'register' 
        
        Label:
            text: 'Support'
            color: 0.18, .5, .92, 1
            halign: 'left'
            font_size: 25
            size_hint: 1, .3
            canvas.before:
                Color:
                    rgb: 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

<RegisterScreen>:
    name: 'register'
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgb: 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .2
            Button:
                text: '<'
                size_hint: .1, 1
                font_size: 75
                background_normal: ""
                background_color: 0.18, .5, .92, 1
                on_release: app.root.current = 'main' 

            Label:
                text: 'Register'
                halign: 'left'
                font_size: 50
                canvas.before:
                    Color:
                        rgb: 0.18, .5, .92
                    Rectangle:
                        pos: self.pos
                        size: self.size
            Widget:
                size_hint: .1, 1
                canvas.before:
                    Color:
                        rgb: 0.18, .5, .92
                    Rectangle:
                        pos: self.pos
                        size: self.size
        BoxLayout:
            orientation: 'horizontal'
            BoxLayout:
                size_hint: .2, .9
                canvas.before:
                    Color:
                        rgb: 1, 1, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size

            GridLayout:
                cols: 2
                size_hint: 0.8, 1
                pos_hint: {'center_x': 0.5}
                spacing: 5
                padding: 0, 10
                _cell_height: dp(70)
                canvas.before:
                    Color:
                        rgb: 1, 1, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    text: 'Email:'
                    height: self.parent._cell_height
                    font_size: 15
                    color: 0.18, .5, .92, 1
                    size_hint: 0.3, None
                BoxLayout:
                    padding: 0, dp(20)
                    size_hint: 0.5, None
                    height: self.parent._cell_height
                    TextInput:
                        font_size: 15
                        multiline: False
                Label:
                    text: 'Phone number:'
                    height: self.parent._cell_height
                    font_size: 15
                    color: 0.18, .5, .92, 1
                    size_hint: 0.3, None
                    
                BoxLayout:
                    padding: 0, dp(20)
                    size_hint: 0.5, None
                    height: self.parent._cell_height
                    TextInput:
                        font_size: 15
                        multiline: False
                        password: True

                Label:
                    text: 'Password:'
                    height: self.parent._cell_height
                    font_size: 15
                    color: 0.18, .5, .92, 1
                    size_hint: 0.3, None
                    
                BoxLayout:
                    padding: 0, dp(20)
                    size_hint: 0.5, None
                    height: self.parent._cell_height
                    TextInput:
                        font_size: 15
                        multiline: False

                Label:
                    text: 'Confirm password:'
                    height: self.parent._cell_height
                    font_size: 15
                    color: 0.18, .5, .92, 1
                    size_hint: 0.3, None
                    
                BoxLayout:
                    padding: 0, dp(20)
                    size_hint: 0.5, None
                    height: self.parent._cell_height
                    TextInput:
                        font_size: 15
                        multiline: False
                        password: True
            BoxLayout:
                size_hint: .2, .1
                canvas.before:
                    Color:
                        rgb: 1, 1, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
        BoxLayout:
            padding: 0, 20
            canvas.before:
                Color:
                    rgb: 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            orientation: 'vertical'
            size_hint: 1, .3
            Button:
                text: 'Register'
                font_size: 25
                background_normal: ""
                background_color: 0.18, .5, .92, 1
                size_hint: .13, .18
                pos_hint: {'center_x': 0.5}
                #on_release:

        BoxLayout:
            size_hint: 1, .3
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size
        Label:
            text: 'Support'
            color: 0.18, .5, .92, 1
            halign: 'left'
            font_size: 25
            size_hint: 1, .3
            canvas.before:
                Color:
                    rgb: 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

''')

class RecipeApp(App):
    def build(self):
        return root_widget

if __name__ == "__main__":
    RecipeApp().run()
