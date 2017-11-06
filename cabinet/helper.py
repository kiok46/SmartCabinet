'''
Helper file.

This file is the life line of the software.
'''

from kivy.app import App


def get_running_app():
	'''
	To get the main application's instance.
	'''
	return App.get_running_app()


def get_root_widget():
	'''
	To get the instance of the application's root widget.
	'''
	return App.get_running_app().root


def get_screen_manager():
	'''
    To get the instance of the screen manager.
	'''
	return get_running_app().root.ids['screen_manager']


def get_filter_screen():
	'''
	To get filter screen's instance from the screen manager.
	'''
	return App.get_running_app().root.filter_screen


def get_inventory_screen():
	'''
	To get the inventory screen's instnce form the screen manager.
	'''
	return App.get_running_app().root.inventory_screen
