'''
Inventory Screen.
'''

from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, DictProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Color, Ellipse, Line, Rectangle
from cabinet.helper import *
from cabinet.popup import DetailPopup
from kivy.uix.label import Label
from datetime import datetime
from cabinet.labels import InfoLabelMedium2

import psycopg2
import pickle
from cabinet.database import *


__all__ = ('InventoryScreen', 'InventoryWidget', 'SummaryBox')


class SummaryBox(BoxLayout):
    '''
    SummaryBox class: contains basic information of inventory,
    '''

    product_line = StringProperty()
    '''
    Reference to product_line in summary box.
    defaults to: ''
    '''
    product_info_line = StringProperty()
    '''
    Reference to product_info_line in summary box.
    defaults to: ''
    '''

    product_list_desc = StringProperty('LISTADO DE PRODUCTOS EN PUNTO DE CONSUMO')
    '''
    Reference to product_list_desc in summary box.
    defaults to: 'LISTADO DE PRODUCTOS EN PUNTO DE CONSUMO'
    '''

    product_list = StringProperty()
    '''
    Reference to product_list in summary box.
    defaults to: ''
    '''

    total_products_desc = StringProperty('NUMERO TOTAL DE PRODUCTOS')
    '''
    Reference to total_products_desc in summary box.
    defaults to: 'NUMERO TOTAL DE PRODUCTOS'
    '''

    total_products = StringProperty()
    '''
    Reference to total_products in summary box.
    defaults to: ''
    '''

    next_to_expire_desc = StringProperty('PROXIMOS A CADUCAR')
    '''
    Reference to next_to_expire_desc in summary box.
    defaults to: 'PROXIMOS A CADUCAR'
    '''

    next_to_expire = StringProperty()
    '''
    Reference to next_to_expire in summary box.
    defaults to: ''
    '''

    expired_desc = StringProperty('CADUCADOS')
    '''
    Reference to expired_desc in summary box.
    defaults to: 'CADUCADOS'
    '''

    expired = StringProperty()
    '''
    Reference to expired in summary box.
    defaults to: ''
    '''

    unknown_desc = StringProperty('DESCONOCIDOS')
    '''
    Reference to unknown_desc in summary box.
    defaults to: 'DESCONOCIDOS')
    '''

    unknown = StringProperty()
    '''
    Reference to unknown in summary box.
    defaults to: ''
    '''

    pending_desc = StringProperty('PENDIENTES')
    '''
    Reference to pending_desc in summary box.
    defaults to: 'PENDIENTES'
    '''

    pending = StringProperty()
    '''
    Reference to pending in summary box.
    defaults to: ''
    '''

    def __init__(self, **kwargs):
        super(SummaryBox, self).__init__(**kwargs)
        self.get_data()
        self.initiate_widgets(**kwargs)

    def get_data(self):
        '''
        Method to refresh the data from the database.
        '''
        self.database_content = get_running_app().db_content()

    def initiate_widgets(self, **kwargs):
        '''
        Add label widgets to the summary box.
        '''
        product_en_true_counter = 0
        line_details_id_counter = 0
        expired_counter = 0
        near2expire_counter = 0
        self.content_length = len(self.database_content)
        for i in range(0, self.content_length):
            '''
            This loop calculates the values for summary box.
            '''
            if self.database_content[i][2] == True:
                product_en_true_counter+=1
            if self.database_content[i][3] == None:
                line_details_id_counter += 1
            if self.database_content[i][1] <= self.database_content[i][1]:
                expired_counter += 1
            if self.database_content[i][1] == self.database_content[i][1]:
                near2expire_counter += 1

        self.product_list = str(self.database_content[0][9])
        self.total_products = str(product_en_true_counter)
        self.unknown = str(line_details_id_counter)
        self.pending = str(self.content_length-product_en_true_counter)
        self.expired = str(expired_counter)
        self.next_to_expire  =str(near2expire_counter)

        self.product_line = self.product_list_desc + ':' + self.product_list
        self.product_info_line = self.total_products_desc + ':' + self.total_products + ' - ' +\
                                 self.next_to_expire_desc + ':' + self.next_to_expire + ' - ' +\
                                 self.expired_desc + ':' + self.expired + ' - ' +\
                                 self.unknown_desc + ':' + self.unknown + ' - ' +\
                                 self.pending_desc + ':' + self.pending


class InventoryWidget(BoxLayout):

    indicator_image = StringProperty('images/alert.png')
    '''
    Reference to indicator_image in summary box.
    defaults to: 'images/alert.png'
    '''

    description = StringProperty('PLACA DE TITAIO P/OSTEOTOMIA TRIBIA PROXIMAL')
    '''
    Reference to description in summary box.
    defaults to: 'PLACA DE TITAIO P/OSTEOTOMIA TRIBIA PROXIMAL'
    '''

    location = StringProperty('EN UBICACION1')
    '''
    Reference to location in summary box.
    defaults to: 'EN UBICACION1'
    '''

    provider_ref = StringProperty('68174')
    '''
    Reference to provider_ref in summary box.
    defaults to: '68174'
    '''

    supplier = StringProperty('SUMISTRADOR')
    '''
    Reference to supplier in summary box.
    defaults to: 'SUMISTRADOR'
    '''

    provider_name = StringProperty('BIOMET')
    '''
    Reference to provider_name in summary box.
    defaults to: 'BIOMET'
    '''

    tag_short_list = StringProperty('TERNA')
    '''
    Reference to tag_short_list in summary box.
    defaults to: 'TERNA'
    '''

    order_code = StringProperty('8376349034')
    '''
    Reference to order_code in summary box.
    defaults to: '8376349034'
    '''

    expiry_date = StringProperty('CADUCIDAD')
    '''
    Reference to expiry_date in summary box.
    defaults to: 'CADUCIDAD'
    '''

    expiry_date_details = StringProperty('27/09/2014')
    '''
    Reference to expiry_date_details in summary box.
    defaults to: '27/09/2014'
    '''

    l_ns = StringProperty("LOTE/N'SERIE")
    '''
    Reference to l_ns in summary box.
    defaults to: "LOTE/N'SERIE"
    '''

    line_details_lo = StringProperty('KD72325')
    '''
    Reference to line_details_lo in summary box.
    defaults to: 'KD72325'
    '''

    line_details_serialnumber = StringProperty('...')
    '''
    Reference to line_details_serialnumber in summary box.
    defaults to: '...'
    '''

    in_date = StringProperty('ENTRADA')
    '''
    Reference to in_date in summary box.
    defaults to: 'ENTRADA'
    '''

    tag_created_date = StringProperty('...')
    '''
    Reference to tag_created_date in summary box.
    defaults to: '...'
    '''

    line_quantity = StringProperty('61')
    '''
    Reference to line_quantity in summary box.
    defaults to: '61'
    '''

    provider_details_1 = StringProperty()
    '''
    Reference to provider_details_1 in summary box.
    defaults to: ''
    '''

    provider_details_2 = StringProperty()
    '''
    Reference to provider_details_2 in summary box.
    defaults to: ''
    '''

    provider_details_3 = StringProperty()
    '''
    Reference to provider_details_3 in summary box.
    defaults to: ''
    '''

    def __init__(self, **kwargs):
        super(InventoryWidget, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        self.register_event_type('on_double_tap')

        self.description = kwargs.get('description')
        self.provider_name = kwargs.get('provider_name')
        self.location = kwargs.get('location')
        self.provider_ref = kwargs.get('provider_ref')
        self.line_quantity = str(kwargs.get('quantity'))
        self.line_details_lo = str(kwargs.get('line_detail_id'))
        self.line_details_serialnumber = str(kwargs.get('line_serial_no'))
        self.tag_created_date = str(kwargs.get('created_date'))
        self.expiry_date_details = str(kwargs.get('expire_date'))
        self.order_code = str(kwargs.get('order_code'))

        self.tag_created_date = (str(self.tag_created_date)).split(' ')[0]
        #print self.expiry_date_details
        self.created = datetime.strptime(self.tag_created_date, "%Y-%m-%d")
        self.expired = datetime.strptime(self.expiry_date_details, "%Y-%m-%d")

        if self.created < self.expired:
            self.indicator_image = 'icons/expired.png'
            self.expiry_date_details = "[color=f22a44ff]{}[/color]".format(str(kwargs.get('expire_date')))
            self.expiry_date = "[color=f22a44ff]CADUCIDAD[/color]"
        elif self.created == self.expired:
            self.indicator_image = 'icons/near2expire.png'
            self.expiry_date_details = "[color=fbeb01ff]{}[/color]".format(str(kwargs.get('expire_date')))
            self.expiry_date = "[color=fbeb01ff]CADUCIDAD[/color]"
        else:
            self.indicator_image = 'icons/notexpired.png'
            self.expiry_date_details = "[color=5bb436ff]{}[/color]".format(str(kwargs.get('expire_date')))
            self.expiry_date = "[color=5bb436ff]CADUCIDAD[/color]"

    touched=0
    def on_touch_down(self, touch):
        '''
        This implements the second touch and double tap property of the
        inventory widget.

        If the inventory widget is touched twice then it should open a detail popup.
        If the inventory widget is double tapped then it should open a detail popup.
        '''
        if self.collide_point(touch.x, touch.y):
            self.touched+=1
            if self.touched >= 2:
                self.touched=0
                self.dispatch('on_double_tap')
            elif touch.is_double_tap:
                self.dispatch('on_double_tap')
            with self.canvas.before:
                Color(rgba = (250/255., 247/255., 233/255., 1)),
                Rectangle(pos=self.pos, size=(self.size))
        else:
            self.touched=0
        super(InventoryWidget, self).on_touch_down(touch)

    def on_double_tap(self):
        '''
        Opens the detail popup.
        '''
        pop = DetailPopup(details={'CADUCIDAD': self.expired,
                                   "N' SERIE": self.line_details_serialnumber,
                                   'ENTRADA': self.created},
                          quantity=self.line_quantity)
        pop.open()


class InventoryScreen(BoxLayout):
    '''
    Inventory Screen class.
    '''
    prev_selection = ObjectProperty()

    def search(self):
        '''
        Called when the search button is pressed/release.
        '''
        get_screen_manager().current = 'filter'

    def move(self):
        '''
        Called when the move button is pressed/release.
        '''
        print (self.ids['selectable_grid'])

    def move_up(self):
        '''
        Called when the move_up button is pressed/release.
        '''
        temp = self.ids['selectable_grid'].get_selectable_nodes()
        prev_temp = self.ids['selectable_grid'].prev_selection
        print (temp.index(prev_temp))

        self.ids['selectable_grid'].select_node(l)
        #if self.ids['selectable_grid'].prev_selection in temp:
        #self.ids['selectable_grid'].select_node(temp[3])

    def move_down(self):
        '''
        Called when the move_down button is pressed/release.
        '''
        print (self.ids)

    def show_list(self):
        '''
        Called when the show_list button is pressed/release.
        '''
        print (self.ids)
