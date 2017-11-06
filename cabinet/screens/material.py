'''
Material Screen.
'''

from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, DictProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Color, Ellipse, Line, Rectangle
from cabinet.helper import *
from cabinet.layouts import GreyInfoBox
from cabinet.popup import DetailPopup
from kivy.uix.label import Label
from datetime import datetime
from cabinet.labels import InfoLabelMedium2

import psycopg2
import pickle
from cabinet.database import *


__all__ = ('MaterialScreen', 'MaterialWidget', 'MaterialSelectableGrid',
           'MaterialPaging')


class MaterialPaging(GreyInfoBox):
    pass


class MaterialSelectableGrid(BoxLayout):
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

    list_desc = StringProperty('LISTADO DE PACIENTES PREVISTOS EN QUIROFANO')
    '''
    Reference to list_desc in summary box.
    defaults to: LISTADO DE PACIENTES PREVISTOS EN QUIROFANO
    '''

    desc_number = StringProperty('1')
    '''
    Reference to disc_number in summary box.
    defaults to: '1'
    '''

    selective_products_desc = StringProperty('NUMERO TOTAL DE PRODUCTOS SELECIONABLES')
    '''
    Reference to total_products_desc in summary box.
    defaults to: NUMERO TOTAL DE PRODUCTOS SELECIONABLES
    '''

    selective_products_no = StringProperty('2')
    '''
    Reference to selective_products_no in summary box.
    defaults to: '2'
    '''

    need_to_deliver_desc = StringProperty('PROXIMOS A CADUCAR')
    '''
    Reference to need_to_deliver_desc in summary box.
    defaults to: 'PROXIMOS A CADUCAR'
    '''

    need_to_deliver_no = StringProperty('0')
    '''
    Reference to need_to_deliver_no in summary box.
    defaults to: '0'
    '''

    def __init__(self, **kwargs):
        super(MaterialSelectableGrid, self).__init__(**kwargs) 
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

        self.product_line = self.list_desc + ':' + self.list_desc
        self.product_info_line = self.selective_products_desc + ':' + self.selective_products_no + ' - ' +\
                                 self.selective_products_desc + ':' + self.selective_products_no + ' - ' +\
                                 self.need_to_deliver_desc + ':' + self.need_to_deliver_no


class MaterialWidget(BoxLayout):

    indicator_label = StringProperty('1')
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
        super(MaterialWidget, self).__init__(**kwargs)
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
            self.indicator_label = 'red'
        elif self.created == self.expired:
            self.indicator_label = 'yello'
        else:
            self.indicator_label = 'green'

        #self.provider_details_1 = "{}  -  {}".format(self.provider_name, self.location)
        #self.provider_details_2 = "{}    {}: {}    {}: {}".format(self.provider_ref, self. supplier,
        #                                                          self.supplier_name, self.tag_short_list,
        #                                                          self.order_code)
        #self.provider_details_3 = "{}: {}    {}: {}/{}    {}: {}".format(self.expiry_date, self.expiry_date_details,
        #                                                                 self.l_ns, self.line_details_lo, 
        #                                                                 self.line_details_serialnumber, self.in_date,
        #                                                                 self.tag_created_date)

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
        pop = DetailPopup(details={'CADUCIDAD': self.expired, "N' SERIE": self.line_details_serialnumber,
                                   'ENTRADA': self.created},
                          quantity=self.line_quantity)
        pop.open()


class MaterialScreen(BoxLayout):
    '''
    Inventory Screen class.
    '''
    
    def __init__(self, **kwargs):
        super(MaterialScreen, self).__init__(**kwargs)

    def search(self):
        '''
        Called when the search button is pressed/release.
        '''
        get_screen_manager().current = 'filter'

    def move(self):
        '''
        Called when the move button is pressed/release.
        '''
        print self.ids['selectable_grid']

    def move_up(self):
        '''
        Called when the move_up button is pressed/release.
        '''
        print self.ids['selectable_grid']

    def move_down(self):
        '''
        Called when the move_down button is pressed/release.
        '''
        print self.ids

    def show_list(self):
        '''
        Called when the show_list button is pressed/release.
        '''
        print self.ids
