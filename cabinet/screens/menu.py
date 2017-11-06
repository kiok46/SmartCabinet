'''
Menu Screen.
'''
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from cabinet.helper import get_screen_manager
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


__all__ = ('MenuScreen', 'MenuIconButton')


class MenuIconButton(ButtonBehavior, Image):
    pass


class MenuScreen(FloatLayout):
    '''
    Menu Screen class mainly contains buttons for navigation purpose.
        - WITHDRAW MATERIAL
        - INVENTORY
        - RETURN MATERIAL
        - OTHER OPERATIONS
    '''

    withdraw_material = StringProperty('WITHDRAW MATERIAL')
    '''
    Label text for the withdraw material button.
    Defaults to: WITHDRAW MATERIAL
    '''

    inventory = StringProperty('INVENTORY')
    '''
    Label text for the inventory button.
    Defaults to: INVENTORY
    '''

    return_material = StringProperty('RETURN MATERIAL')
    '''
    Label text for the return material button.
    Defaults to: RETURN MATERIAL
    '''

    other_operations = StringProperty('OTHER OPERATIONS')
    '''
    Label text for the withdraw material button.
    Defaults to: OTHER OPERATIONS
    '''

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)


    def to_withdraw_material_screen(self):
        '''
        To navigate to the withdraw material screen.
        '''
        pass
        #get_screen_manager().current = 'inventory'

    def to_inventory_screen(self):
        '''
        To navigate to the inventory screen.
        '''
        get_screen_manager().current = 'inventory'

    def to_return_material_screen(self):
        '''
        To return to the material screen
        '''
        get_screen_manager().current = 'material'

    def to_other_operations_screen(self):
        '''
        To return to the operations screen.
        '''
        get_screen_manager().current = 'episode'
