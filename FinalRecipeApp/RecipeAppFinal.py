import sqlite3 as sql
import uuid   # uuid is used to generate a random number to avoid dic attack
import hashlib # calling the hashing 

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
    totalCalories = 0 # create a class attribute totalCalories
    
    def formatScreen(self, theRecipeID, name):
        """ Function for populating the scrollview with items and reformatting widgets """
        con = sql.connect('realWorldProject.db') # connect to the database
        cur = con.cursor()
        cur.execute('''SELECT calories FROM recipes WHERE recipeID =?; ''', (int(theRecipeID),)) # Select the calories from the record with the recipe ID passed as a parameter
        calories = int(cur.fetchone()[0])
        self.updateTotalCal(calories) # call the updateTotalCal method
        self.ids.grid.add_widget(FoodItem(food=name, calories=str(calories))) # Add a new FoodItem widget to the scrollview

    def updateTotalCal(self, cal):
        """ Updates the totalCalories class attribute and other widgets on the screen """
        CaloriesScreen.totalCalories += cal # Add the calories of the selected recipe to the totalCalories attribute
        self.ids.calories.text = str(CaloriesScreen.totalCalories)
        if CaloriesScreen.totalCalories < 1000:
            self.ids.warning.text = "You are under calories." # if the total calories is under 1000 alert the user
        elif CaloriesScreen.totalCalories > 2500:
            self.ids.warning.text = "You are over calories." # if the total calories is above 2500 alert the user
        else:
            self.ids.warning.text = "" # else there is no warning to display to the user

    def clearList(self):
        """ Clears the scrollview of all widgets """
        self.ids.grid.clear_widgets() # clear the grid of widgets 
        CaloriesScreen.totalCalories = 0 # reset the totalCalories attribute to 0 
        self.ids.calories.text = str(CaloriesScreen.totalCalories)
        self.ids.warning.text = ""
      
class FoodItem(BoxLayout):
    # Inherit the BoxLayout class and create a unique widget called FoodItem with two labels
    food = StringProperty('')
    calories = StringProperty('')

class LoginScreen(Screen):

    def loginUser(self):
        """ Check whether a user account exists and whether the input password is correct """
        con = sql.connect('realWorldProject.db') # connect to the database
        cur = con.cursor()
        theEmail = self.ids.loginemail.text # variable theEmail equals the contents of the loginemail textfield
        thePassword = self.ids.loginpassword.text # variable thePassword equals the contents of the loginpassword textfield

        for row in cur.execute('''SELECT email FROM userDetails WHERE email = ?;''', (theEmail,)):
            # iterate through the query which selects the email field from the userDetails table where the email is equal to theEmail parameter
            email = row
            break
        else:
            self.ids.warningmsg.text = "Your username or password are incorrect" # if no matches throw the user an error message
            return None # return none and break out of function

        cur.execute('''SELECT password FROM userDetails WHERE email = ?; ''', (theEmail,)) # get the password tied to the record where the email = theEmail parameter
        dbHash = cur.fetchone()[0]
        doPasswordsMatch = self.check_password(dbHash, thePassword) # check whether the textfield input password matches the hashed password for that user account

        if doPasswordsMatch == True:
            root_widget.current = 'shopping' # if the passwords match load the shopping screen 
            pass
        else:
            self.ids.warningmsg.text = "Your username or password are incorrect" # else inform the user there was an error


    def check_password(self, hashed_password, user_password): #funcation to check if password being entered is the same or not
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
        
class RegisterScreen(Screen):

    def getNewId(self):
        """ Count all the records in the database and increment by 1 to generate a new user ID """
        con = sql.connect('realWorldProject.db')
        cur = con.cursor()
        cur.execute('''SELECT Count(*) FROM userDetails''') # count all records from the userDetails table 
        theCount = int(cur.fetchone() [0])
        return int(theCount + 1) # return the answer incremented by 1 to the callee

    def RegisterUser(self):
        """ Register a new user and input their details into the database """
        con = sql.connect('realWorldProject.db')
        cur = con.cursor()
        password = self.ids.password.text # take password from the password textfield 
        hashedPassword = self.hash_password(password) # hash the password 
        userDetails = [self.getNewId(), hashedPassword, self.ids.email.text, int(self.ids.phone.text)] # take all contents of textfields and the hashed password and put them in a list
        cur.execute('''INSERT INTO userDetails (userID, password, email, phone_number) VALUES (?, ?, ?, ?);''', userDetails) # insert all the details into the database
        con.commit()
        con.close()
        self.ids.success.text = "Successfully registered!" #indicate to the user they were successfully registered
        self.clearInput() # 
        
    def clearInput(self):
        """ Clear all the textfields on the screen ready for a new registration """
        self.ids.password.text = ""
        self.ids.email.text = ""
        self.ids.phone.text = ""
        self.ids.confirm.text = ""

    def hash_password(self, password): #creating funcation to hash passwords
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex #salt is a random sequence added to the password string before using the hash function, uuid4 make a random uuid 
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt



class IngredQty(BoxLayout):
    """ A custom implementation of the BoxLayout which consists of 2 labels """
    pass

class Ingredient(BoxLayout):
    """ A custom implementation of the BoxLayout which constructs an ingredient widget with two labels and a checkbox """
    ingredient = StringProperty('')
    quantity = StringProperty('')

    def activate(self):
        print("test")

class ShoppingScreen(Screen):
    recipes = [] # stores all recipes added to the shopping list by the user 
    totalCalories = 0 # holds the value for the total calories of all the recipes combined 
    averageCalories = 0 # the average calories each day depending on what duration of time the user selects
    
    def addRecipe(self):
        """ Adds a recipe to the scrollview pane """
        con = sql.connect('realWorldProject.db') # connects to the DB
        cur = con.cursor()
        for recipe in ShoppingScreen.recipes: # iterates through all entries in the recipes list
            
            cur.execute('''SELECT recipeName FROM recipes WHERE recipeID = ?;''', (recipe,)) # select the recipeName based on the recipe parameter
            recipeName = str(cur.fetchone()[0])
            self.ids.grid.add_widget(RecipeLabel(recipeName=recipeName)) # create a recipe label based on what's returned via the query
            self.ids.grid.add_widget(IngredQty()) # adds two labels underneath the recipe label 

            cur.execute('''SELECT calories FROM recipes WHERE recipeID = ?''', (recipe,)) # retrieves the calories of the selected recipe
            thecalories = int(cur.fetchone()[0])
            ShoppingScreen.totalCalories += thecalories # totalCalories class attribute is incremented with the calories of the recipe selected


            
            ingredients = cur.execute('''SELECT * FROM ingredients WHERE recipeID = ?;''', (recipe,))
            for row in ingredients: # retrieves all ingredients for the selected recipe and populates the scrollview with them
                self.ids.grid.add_widget(Ingredient(ingredient=row[1], quantity = row[2]))
            ShoppingScreen.recipes.remove(recipe) # removes the recipe from the recipes list as it has been added to the screen now 

        self.ids.totalcalories.text = str(ShoppingScreen.totalCalories) # updates the totalCalories text 

    def clearList(self):
        """ Clears the scrollview of all the recipes """
        self.ids.grid.clear_widgets()
        ShoppingScreen.totalCalories = 0
        self.ids.totalcalories.text = str(ShoppingScreen.totalCalories)
        ShoppingScreen.avergageCalories = 0
        self.ids.avgcalories.text = str(avg)

    def calculateAvg(self, divisor):
        """ Calculates the average amount of calories per day based on the divisor passed when called via the dropdown menu """
        avg = ShoppingScreen.totalCalories // divisor
        self.ids.avgcalories.text = str(avg)
            
     

class RecipeLabel(BoxLayout):
    """ A custom implementation of the BoxLayout widget """
    recipeName = StringProperty('')      
        

class CategoriesScreen(Screen):
    pass

class BreakfastScreen(Screen):
    pass

class AddRecipe(Screen):
    pass

class SimpleCheeseOmelette(Screen):

    def addToShopping(self, theId):
        """ Adds a 1 to indicate a simple cheese omelette to the ShoppingScreen's recipes list """
        ShoppingScreen.recipes.append(1)

class theScreenManager(ScreenManager):
    """ Manages the different screens of the application """
    pass

# The KV language formats screens/widgets/frames much like CSS formats HTML
# The below text within the load_string function is all KV language for customizing widget details such as size, color and position

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
            size_hint: 1, .4
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
                    spacing: 30
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
                    text: ''
                    id: totalcalories
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
                    on_release: root.clearList()
                Widget:
                    size_hint: .8, 1
                Button:
                    text: 'Sync'
                    size_hint: .1, .7
                    font_size: 25
                    background_normal: ""
                    background_color: 0.18, .5, .92, 1
                    on_release: root.addRecipe()
                Widget:
                    size_hint: .1, 1

            Widget:
                size_hint: 1, .1
                    

<RecipeLabel>:
    size_hint_y: None
    height: 30
    Label:
        text: root.recipeName
        color: (1, 1, 1, 1)
        font_size: 25
        canvas.before:
            Color:
                rgb: 0.18, .5, .92
            Rectangle:
                pos: self.pos
                size: self.size
        

<IngredQty>:
    Label:
        text: "Ingredient"
        color: (0.18, .5, .92, 1)
        font_size: 25
    Label:
        text: 'Quantity'  
        color: (0.18, .5, .92, 1)
        font_size: 25
    Widget:

<Ingredient>:
    checkbox: checkbox.__self__
    name: 'ingredient'
    size_hint_y: None
    height: 25
    Label:
        text: root.ingredient
        color: (0.18, .5, .92, 1)
        font_size: 15
    Label:
        text: root.quantity
        color: (0.18, .5, .92, 1)
        font_size: 15
    CheckBox:
        id: checkbox
        active: True
        on_active: root.activate()
        color: (0.18, .5, .92, 1)
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
            on_release: root.addToShopping(1)

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
