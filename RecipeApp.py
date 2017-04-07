import sqlite3 as sql
import uuid   
import hashlib

from kivy.uix.checkbox import CheckBox 
from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
import pickle

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

class MainScreen(Screen):
    pass

class CaloriesScreen(Screen):
    totalCalories = 0
    
    def formatScreen(self, theRecipeID, name):
        con = sql.connect('realWorldProject.db')
        cur = con.cursor()
        cur.execute('''SELECT calories FROM recipes WHERE recipeID =?; ''', (int(theRecipeID),))
        calories = int(cur.fetchone()[0])
        self.updateTotalCal(calories)
        self.ids.grid.add_widget(FoodItem(food=name, calories=str(calories)))

    def updateTotalCal(self, cal):
        CaloriesScreen.totalCalories += cal
        self.ids.calories.text = str(CaloriesScreen.totalCalories)
        if CaloriesScreen.totalCalories < 1000:
            self.ids.warning.text = "You are under calories."
        elif CaloriesScreen.totalCalories > 2500:
            self.ids.warning.text = "You are over calories."
        else:
            self.ids.warning.text = ""

    def clearList(self):
        self.ids.grid.clear_widgets()
        CaloriesScreen.totalCalories = 0
        self.ids.calories.text = str(CaloriesScreen.totalCalories)
        self.ids.warning.text = ""
      
class FoodItem(BoxLayout):
    food = StringProperty('')
    calories = StringProperty('')

class LoginScreen(Screen):

    def loginUser(self):
        con = sql.connect('realWorldProject.db')
        cur = con.cursor()
        theEmail = self.ids.loginemail.text
        thePassword = self.ids.loginpassword.text

        for row in cur.execute('''SELECT email FROM userDetails WHERE email = ?;''', (theEmail,)):
            email = row
            break
        else:
            self.ids.warningmsg.text = "Your username or password are incorrect"
            return None

        cur.execute('''SELECT password FROM userDetails WHERE email = ?; ''', (theEmail,))
        dbHash = cur.fetchone()[0]
        doPasswordsMatch = self.check_password(dbHash, thePassword)

        if doPasswordsMatch == True:
            root_widget.current = 'shopping'
            pass
        else:
            self.ids.warningmsg.text = "Your username or password are incorrect"


    def check_password(self, hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
        
class RegisterScreen(Screen):

    def getNewId(self):
        con = sql.connect('realWorldProject.db')
        cur = con.cursor()
        cur.execute('''SELECT Count(*) FROM userDetails''')
        theCount = int(cur.fetchone() [0])
        return int(theCount + 1)

    def RegisterUser(self):
        con = sql.connect('realWorldProject.db')
        cur = con.cursor()
        password = self.ids.password.text
        hashedPassword = self.hash_password(password)
        userDetails = [self.getNewId(), hashedPassword, self.ids.email.text, int(self.ids.phone.text)]
        cur.execute('''INSERT INTO userDetails (userID, password, email, phone_number) VALUES (?, ?, ?, ?);''', userDetails)
        con.commit()
        con.close()
        self.ids.success.text = "Successfully registered!"
        self.clearInput()
        
    def clearInput(self):
        self.ids.password.text = ""
        self.ids.email.text = ""
        self.ids.phone.text = ""
        self.ids.confirm.text = ""

    def hash_password(self, password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

class ShoppingScreen(Screen):

    def calculateAvg(self, divisor):
        con = sql.connect('realWorldProject.db')
        cur = con.cursor()
        cur.execute('''SELECT calories FROM recipes WHERE recipeID = 1''')
        theCalories = int(cur.fetchone() [0])
        theavgcalories = str(theCalories // divisor)
        self.ids.avgcalories.text = theavgcalories
        
        

class CategoriesScreen(Screen):
    pass

class BreakfastScreen(Screen):
    pass

class AddRecipe(Screen):
    pass

class SimpleCheeseOmelette(Screen):
    pass

class theScreenManager(ScreenManager):
    pass

root_widget = Builder.load_string('''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import Factory kivy.factory.Factory

theScreenManager:
    transition: FadeTransition()
    MainScreen:
    RegisterScreen:
    ShoppingScreen:
    LoginScreen:
    CategoriesScreen:
    BreakfastScreen:
    CaloriesScreen:
    SimpleCheeseOmelette:
    AddRecipe:

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Health Zone'
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
            on_release: app.root.current = 'categories'
            
            
        Button:
            text: 'Shopping List'
            color: 0.18, .5, .92, 1
            font_size: 30
            on_release: app.root.current = 'login'
            background_normal: ""

<CaloriesScreen>:
    name: 'calories'
    BoxLayout:
        orientation: 'vertical'
        dropdown1: dropdown1.__self__
    
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
                font_size: 15
                on_release: dropdown1.open(self)
                height: '48dp'
                pos_hint: { 'top' : 0.75}
                size_hint: .8, .5

            DropDown:
                id: dropdown1
                on_parent: self.dismiss()
                on_select: btn.text = '{}'.format(args[1])

                Button:
                    text: 'Simple Cheese Omelette'
                    font_size: 15
                    size_hint_y: None
                    height: '48dp'
                    on_release: root.formatScreen(1, 'Simple Cheese Omelette')

                Button:
                    text: 'Vegetarian Lasagne'
                    font_size: 15
                    size_hint_y: None
                    height: '48dp'
                    on_release: root.formatScreen(5, 'Vegetarian Lasagne')

                Button:
                    text: 'Tomato and Caper Linguine'
                    font_size: 15
                    size_hint_y: None
                    height: '48dp'
                    on_release: root.formatScreen(3, 'Tomato and linguine')


            
            Widget:
                size_hint: .02, 1

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .2
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text:'Recipe'
                color: (1, 1, 1, 1)
                font_size: 30
            Label:
                text:'Calories'
                color: (1, 1, 1, 1)
                font_size: 30
        BoxLayout:
            canvas.before:
                Color:
                    rgb: 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            ScrollView:
                scroll_timeout: 250
                scroll_distance: 20
                do_scroll_y: True
                do_scroll_x: False
                
                GridLayout:
                    id: grid
                    height: self.minimum_height
                    cols: 1
                    spacing: 45
                    padding: 25
                    size_hint_y: None
                    canvas.before:
                        Color:
                            rgb: 1, 1, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size
        BoxLayout:
            orientation: 'vertical'
            size_hint: 1, .5
            canvas.before:
                Color:
                    rgb: 0.8, 0.8, 0.8
                Rectangle:
                    pos: self.pos
                    size: self.size
            BoxLayout:
            BoxLayout:
                orientation: 'horizontal'
                Label:
                    text:'Total calories'
                    color: (0.18, .5, .92, 1)
                    font_size: 30
                Label:
                    id: calories
                    text:'0'
                    color: (0.18, .5, .92, 1)
                    font_size: 30

            BoxLayout:
                orientation: 'horizontal'
                Label:
                    id: warning
                    text: ''
                    color: (0.18, .5, .92, 1)
                    font_size: 30
            BoxLayout:
                orientation: 'horizontal'
                Widget:
                    size_hint: .1, .9
                Button:
                    text: 'Clear'
                    font_size: 25
                    background_normal: ""
                    background_color: 0.18, .5, .92, 1
                    on_release: root.clearList()
                    size_hint: .1, .9
                Widget:
            BoxLayout:
                orientation: 'horizontal'
                
        
<FoodItem>:
    Label:
        text: root.food
        color: (0.18, .5, .92, 1)
        font_size: 30
    Label:
        text: root.calories
        color: (0.18, .5, .92, 1)
        font_size: 30


<LoginScreen>:
    name: 'login'
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
                    text: 'Email:'
                    height: self.parent._cell_height
                    font_size: 25
                    color: 0.18, .5, .92, 1
                    size_hint: 0.3, None
                BoxLayout:
                    padding: 0, dp(20)
                    size_hint: 0.5, None
                    height: self.parent._cell_height
                    TextInput:
                        id: loginemail
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
                        id: loginpassword
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
                id: warningmsg
                text: ''
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
                on_release: root.loginUser()
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
<ShoppingScreen>:
    name: 'shopping'
    dropdown: dropdown.__self__
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
                text: 'Shopping List'
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
            size_hint: 1, .2
            spacing: 50
            canvas.before:
                Color:
                    rgb: 0.8, 0.8, 0.8
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: 'Duration'
                font_size: 30
                color: 0.18, .5, .92, 1

            Button:
                id: btn
                text: 'Select a duration of time...'
                font_size: 15
                on_release: dropdown.open(self)
                height: '48dp'
                pos_hint: { 'top' : 0.75}
                size_hint: .8, .5

            DropDown:
                id: dropdown
                on_parent: self.dismiss()
                on_select: btn.text = '{}'.format(args[1])

                Button:
                    text: '1 week'
                    font_size: 15
                    size_hint_y: None
                    height: '48dp'
                    on_release: root.calculateAvg(7)

                Button:
                    text: '2 weeks'
                    font_size: 15
                    size_hint_y: None
                    height: '48dp'
                    on_release: root.calculateAvg(14)

                Button:
                    text: '3 weeks'
                    font_size: 15
                    size_hint_y: None
                    height: '48dp'
                    on_release: root.calculateAvg(21)
            Widget:
                size_hint: .02, 1

        Label:
            size_hint: 1, .2
            text: 'Simple Cheese Omelette'
            font_size: 50
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size


        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .12
            canvas.before:
                Color:
                    rgb: 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Widget:
                size_hint: .3, 1

            Label:
                text: 'Ingredient'
                font_size: 30
                color: 0.18, .5, .92, 1

            Label:
                text: 'Quantity'
                font_size: 30
                color: 0.18, .5, .92, 1

            Widget:
                #size_hint: .3, 1

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .12
            canvas.before:
                Color:
                    rgb: 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Widget:
                size_hint: .3, 1

            Label:
                text: 'Large free-range egg'
                font_size: 30
                color: 0.18, .5, .92, 1

            Label:
                text: '1'
                font_size: 30
                color: 0.18, .5, .92, 1

            CheckBox:
                active: True

            Widget:
                size_hint: .3, 1

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .12
            canvas.before:
                Color:
                    rgb: 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Widget:
                size_hint: .3, 1

            Label:
                text: 'Olive oil'
                font_size: 30
                color: 0.18, .5, .92, 1

            Label:
                text: '1'
                font_size: 30
                color: 0.18, .5, .92, 1

            CheckBox:
                active: True

            Widget:
                size_hint: .3, 1

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .12
            canvas.before:
                Color:
                    rgb: 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Widget:
                size_hint: .3, 1

            Label:
                text: 'Cheddar Cheese 100g'
                font_size: 30
                color: 0.18, .5, .92, 1

            Label:
                text: '1'
                font_size: 30
                color: 0.18, .5, .92, 1

            CheckBox:
                active: True

            Widget:
                size_hint: .3, 1
           
        BoxLayout:
            orientation: 'vertical'
            size_hint: 1, .4
            canvas.before:
                Color:
                    rgb: 0.8, 0.8, 0.8
                Rectangle:
                    pos: self.pos
                    size: self.size

            BoxLayout:
                orientation: 'horizontal'

                Label:
                    text: 'Total Calories'
                    font_size: 30
                    color: 0.18, .5, .92, 1

                Label:
                    text: '241'
                    font_size: 30
                    color: 0.18, .5, .92, 1

            BoxLayout:
                orientation: 'horizontal'

                Label:
                    text: 'Average/day'
                    font_size: 30
                    color: 0.18, .5, .92, 1

                Label:
                    id: avgcalories
                    text: '0'
                    font_size: 30
                    color: 0.18, .5, .92, 1

            BoxLayout:
                orientation: 'horizontal'
                Widget:
                    size_hint: .1, 1

                Button:
                    text: 'Clear'
                    size_hint: .1, .7
                    font_size: 25
                    background_normal: ""
                    background_color: 0.18, .5, .92, 1
                    #on_release: app.root.current = 'main'
                Widget:
                    size_hint: .8, 1

            Widget:
                size_hint: 1, .1

                
            

         

            
       
                
##                GridLayout:
##                    id: grid
##                    height: self.minimum_height
##                    cols: 1
##                    spacing: 45
##                    padding: 25
##                    size_hint_y: None
##                    

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
                on_release: app.root.current = 'login' 

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
                        id: email
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
                        id: phone
                        font_size: 15
                        multiline: False

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
                        id: password
                        font_size: 15
                        multiline: False
                        password: True

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
                        id: confirm
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
                on_release: root.RegisterUser()

        BoxLayout:
            size_hint: 1, .3
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                id: success
                text: ''
                pos_hint:{'center_x': 0.5}
                font_size: 25
                color: 1, 1, 1, 1
                
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

<CategoriesScreen>:
    name: 'categories'
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
                text: 'Categories'
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
            Button:
                background_normal: ""
                background_color: 1, 1, 1, 1
                Image:
                    source: 'Vegetarian.png'
                    size: 210, 210
                    allow_stretch: True
                    y: self.parent.y + self.parent.height - 200
                    x: self.parent.x + 50
                Label:
                    text: "Vegetarian"
                    y: self.parent.y + self.parent.height - 275
                    x: self.parent.x + 135
                    font_size: 30
                    color: 0.18, .5, .92, 1
                    
            
            Button:
                background_normal: ""
                background_color: 1, 1, 1, 1
                on_release: app.root.current = 'breakfast' 
                Image:
                    source: 'Breakfast.png'
                    size: 250, 250
                    allow_stretch: True
                    y: self.parent.y + self.parent.height - 175
                    x: self.parent.x + 60
                Label:
                    text: "Breakfast"
                    font_size: 30
                    y: self.parent.y + self.parent.height - 275
                    x: self.parent.x + 140
                    color: 0.18, .5, .92, 1

        BoxLayout: 
            orientation: 'horizontal'
            Button:
                background_normal: ""
                background_color: 1, 1, 1, 1
                Image:
                    source: 'Lunch.png'
                    size: 175, 1175
                    allow_stretch: True
                    y: self.parent.y + self.parent.height - 690
                    x: self.parent.x + 90
                Label:
                    text: "Lunch"
                    font_size: 30
                    y: self.parent.y + self.parent.height - 270
                    x: self.parent.x + 130
                    color: 0.18, .5, .92, 1
            
            Button:
                background_normal: ""
                background_color: 1, 1, 1, 1
                on_release: app.root.current = 'addrecipe' 
                Label:
                    text: "Add own recipe"
                    y: self.parent.y + self.parent.height - 170
                    x: self.parent.x + 150
                    font_size: 50
                    color: 0.18, .5, .92, 1
            
<BreakfastScreen>:
    name: 'breakfast'
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
                text: 'Breakfast'
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
            Button:
                background_normal: ""
                background_color: 1, 1, 1, 1
                on_release: app.root.current = 'omelette' 
                Image:
                    source: 'Breakfast.png'
                    size: 210, 210
                    allow_stretch: True
                    y: self.parent.y + self.parent.height - 175
                    x: self.parent.x + 75
                Label:
                    text: "Simple Cheese Omelette"
                    font_size: 30
                    y: self.parent.y + self.parent.height - 275
                    x: self.parent.x + 140
                    color: 0.18, .5, .92, 1

            Button:
                background_normal: ""
                background_color: 1, 1, 1, 1
                on_release: app.root.current = 'breakfast' 
                Image:
                    source: 'placeholdercircle.png'
                    size: 175, 175
                    allow_stretch: True
                    y: self.parent.y + self.parent.height - 195
                    x: self.parent.x + 90
                

        BoxLayout: 
            orientation: 'horizontal'
            Button:
                background_normal: ""
                background_color: 1, 1, 1, 1
                Image:
                    source: 'placeholdercircle.png'
                    size: 175, 1175
                    allow_stretch: True
                    y: self.parent.y + self.parent.height - 690
                    x: self.parent.x + 100

            Button:
                background_normal: ""
                background_color: 1, 1, 1, 1
                Image:
                    source: 'placeholdercircle.png'
                    size: 175, 1175
                    allow_stretch: True
                    y: self.parent.y + self.parent.height - 690
                    x: self.parent.x + 90
                
<SimpleCheeseOmelette>:
    name: 'omelette'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .5
            Button:
                text: '<'
                size_hint: .1, 1
                color: 0.18, .5, .92, 1
                font_size: 75
                background_normal: ""
                background_color: 1, 1, 1, 1
                on_release: app.root.current = 'main' 

            Label:
                text: 'Simple Cheese Omelette'
                color: 0.18, .5, .92, 1
                halign: 'left'
                font_size: 50
                canvas.before:
                    Color:
                        rgb: 1, 1, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
            Widget:
                size_hint: .1, 1
                canvas.before:
                    Color:
                        rgb: 1, 1, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .15
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "Calories: 241"
                font_size: 15
                color: 1, 1, 1, 1

            Label:
                text: "Sugars: 0.1 grams"
                font_size: 15
                color: 1, 1, 1, 1

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .15
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "Fat: 18.1 grams"
                font_size: 15
                color: 1, 1, 1, 1

            Label:
                text: "Salt: 1.31 grams"
                font_size: 15
                color: 1, 1, 1, 1

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .15
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "Saturate: 19.6 grams"
                font_size: 15
                color: 1, 1, 1, 1

            Label:
                text: "Fibre: 0.1 grams"
                font_size: 15
                color: 1, 1, 1, 1

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .15
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "No carbs"
                font_size: 15
                color: 1, 1, 1, 1

            Widget:

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .15
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "Ingredients"
                font_size: 30
                color: 1, 1, 1, 1

            Widget:

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .15
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "2 large free-range eggs"
                font_size: 15
                color: 1, 1, 1, 1

            Widget:

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .15
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "Olive oil"
                font_size: 15
                color: 1, 1, 1, 1

            Widget:

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .15
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "10g Cheddar Cheese"
                font_size: 15
                color: 1, 1, 1, 1

            Widget:

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .15
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size
            Widget: 
            Label:
                text: "Method"
                font_size: 30
                color: 1, 1, 1, 1

            Widget:

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .2
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "1. Crack the eggs into a mixing bowl, season with a pinch of sea salt and black pepper, then beat well with a fork until fully combined."
                
                font_size: 10
                color: 1, 1, 1, 1


        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .2
            canvas.before:
                Color:
                    rgb: 0.18, .5, .92
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "2. Place a small non-stick frying pan on a low heat to warm up."
                font_size: 10
                color: 1, 1, 1, 1

        Button:
            text: 'Add to shopping list'
            size_hint: 1, .3
            color: 0.18, .5, .92, 1
            font_size: 30
            background_normal: ""
            background_color: 1, 1, 1, 1
            #on_release: app.root.current = 'main'

        



        

        

        
            

            
        

                

            
        
        

<AddRecipe>:
    name: 'addrecipe'
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
                text: 'Add your own recipe'
                halign: 'left'
                font_size: 50
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
                    text: 'Name:'
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
                    text: 'Method:'
                    height: self.parent._cell_height
                    font_size: 25
                    color: 0.18, .5, .92, 1
                    size_hint: 0.3, None
                    
                BoxLayout:
                    padding: 0, dp(20)
                    size_hint: 0.5, None
                    height: 250
                    TextInput:
                        font_size: 10
                        multiline: False
            BoxLayout:
                size_hint: .2, 1
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
