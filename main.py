from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from datetime import datetime
from pathlib import Path
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from hoverable import HoverBehavior
import json, glob
import random

Builder.load_file('design.kv')


# Window.clearcolor = (.5, .3, .5, 1)

class LoginScreen(Screen):
    def sign_up(self):
        print("Sign up button pressed")
        self.manager.current = "sign_up_screen"
    def login(self, u_name, p_word):
        with open("users.json") as file:
            users = json.load(file)
        if u_name in users and users[u_name]['password'] == p_word:
            self.manager.current = "how_are_you_feeling"
        else:
            self.ids.login_wrong.text = "Wrong username or password!"  
    def forgot_password(self):
        print("forgot password yayyy!")
        self.manager.current = "forgot_password_screen"    


class RootWidget(ScreenManager):
    pass


# class FullImage(Image):
#     pass


class SignUpScreen(Screen):
    def add_user(self, u_name, p_word):
        with open("users.json") as file:
            users = json.load(file)

        users[u_name] = {'username': u_name, 'password': p_word,
        'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"

class ForgotPasswordScreen(Screen):
    print("Email yay!")


class SignUpScreenSuccess(Screen):
    def go_to_login_screen(self):
        self.manager.current = "Login_screen"


class HowAreYouFeeling(Screen):
    def logout(self):
        self.manager.current = "Login_screen"
    def get_quote(self, feels):
        feels = feels.lower()
        available_feelings = glob.glob("quotes/*txt")
        
        available_feelings = [Path(filename).stem for filename in available_feelings]
        print(available_feelings)

        if feels in available_feelings:
            with open(f"quotes/{feels}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling."

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()
    

if __name__ == "__main__":
    MainApp().run()