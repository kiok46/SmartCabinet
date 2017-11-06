'''
Main Application.
'''

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, DictProperty, ListProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from cabinet.behaviors import *
from cabinet.helper import *
from cabinet.database import *
from cabinet.screens.inventory import InventoryScreen
from cabinet.screens.filter import FilterScreen
from cabinet.screens.menu import MenuScreen
from cabinet.screens.material import MaterialScreen
from cabinet.screens.episode import EpisodeScreen

import threading
import psycopg2
import datetime

'''
Loading the .kv files from cabinet/kv/
'''

from os import listdir
kv_path = './cabinet/kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)


class Manager(BoxLayout):
    '''
    Root widget which is a boxlayout, it contains a screen manager.
    '''

    inventory_screen = ObjectProperty()
    '''
    Instance of inventory screen.
    '''

    filter_screen = ObjectProperty()
    '''
    Instance of the filter screen.
    '''

    active_user = StringProperty('DEBUGGER TESTER USUARIO PRUEBA')
    '''
    Active User Information.
    Defaults to: 'DEBUGGER TESTER USUARIO PRUEBA'
    '''
    disclamer = StringProperty('TODOS LOS DERECHOS RESERVADOS 2016 SM TECHNOLOGIA')
    '''
    disclamer
    Defaults to: 'TODOS LOS DERECHOS RESERVADOS 2016 SM TECHNOLOGIA'
    '''

    servicio_logo = StringProperty('images/servicio.png')
    '''
    Logo.
    '''

    servizo_logo = StringProperty('images/servizo.png')
    '''
    Logo.
    '''

    def on_home(self):
        '''
        Switch to home screen.
        '''
        get_screen_manager().current = 'menu'

    def on_report(self):
        '''
        Handle report.
        '''
        pass

    def on_logout(self):
        '''
        Logout.
        '''
        pass

    def on_help(self):
        '''
        Help
        '''
        pass


class MainApp(App):
    '''
    The Main app class, This class is called in the beginning.
    '''
    date = StringProperty()
    '''
    Reference to Date.
    '''
    time = StringProperty()
    '''
    Reference to time.
    '''
    ip = StringProperty()
    '''
    reference to current IP.
    '''
    database_content = ListProperty()

    '''
    Reference to database content.
    '''

    images = DictProperty({'home': 'images/home.png', 'report': 'images/report.png',
                           'alert': 'images/alert.png', 'wifi_on': 'images/wifi_on.png',
                           'wifi_off': 'images/wifi_off.png', 'help': 'images/help.png',
                           'sai_off': 'images/sai_off.png', 'back': 'images/back.png',
                           'sai_charged': 'images/sai_charged.png', 'sai_plugged': 'images/sai_plugged.png',
                           'logout': 'images/logout.png'})
    '''
    Rerference to all the images in the software.
    '''

    icons = DictProperty({'search': 'icons/search.png', 'move': 'icons/move.png',
                          'up': 'icons/up.png', 'down': 'icons/down.png',
                          'group': 'icons/group.png', 'business': 'icons/help.png',
                          'units': 'icons/units.png', 'trash': 'icons/trash.png',
                          'ok': 'icons/ok.png'})
    '''
    Rerference to all the icons in the software.
    '''

    def build(self):
        '''
        builds the application.
        '''
        Clock.schedule_interval(self.get_time, 1)
        Clock.schedule_once(self.get_date, 0)
        Clock.schedule_once(self.get_ip, 0)
        Window.maximize()
        self.get_database_tables()
        self.title = "Smart Cabinet"
        self.root = Manager()

    def get_date(self, *args):
        '''
        Get the date to be displayed in the main screen.
        '''
        now = datetime.datetime.now()
        date = '{}/{}/{}'.format(now.month, now.day, now.year)
        self.date = date

    def get_time(self, *agrs):
        '''
        Get the time to be displayed in the main screen.
        '''
        now = datetime.datetime.now()
        time = '{}:{}:{}'.format(now.hour, now.minute, now.second)
        self.time = time

    def get_ip(self, *args):
        '''
        Get the current ip.
        '''
        import socket
        self.ip = socket.gethostbyname(socket.gethostname())

    def db_content(self):
        '''
        Return the data from the database
        '''
        return self.database_content

    def refresh_content(self):
        '''
        Refresh the data from the database.
        '''
        self.get_database_tables()
        self.db_content()

    def get_database_tables(self):
        '''
        Extracts data from the database.
        '''
        myConnection = psycopg2.connect(host=hostname, user=username,
                                        password=password, dbname=database,
                                        port=port )
        self.database_content = get_table_list(myConnection)
        myConnection.close()


if __name__ == '__main__':
    app = MainApp()
    app.run()
