from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, NumericProperty
from kivy.properties import ObjectProperty, ListProperty, partial
from kivy.uix.behaviors.compoundselection import CompoundSelectionBehavior
from cabinet.screens.inventory import InventoryWidget
from kivy.clock import Clock
from cabinet.layouts import GreyInfoBox
from kivy.graphics import Color, Ellipse, Line, Rectangle, BorderImage

from cabinet.database import *
from cabinet.helper import *
from cabinet.labels import *
from cabinet.buttons import IconButton, ImageButton, RectShadowButton

import math
import psycopg2


__all__ = ('PagingWidget', 'SelectableGrid')


class PagingWidget(GreyInfoBox):
    '''
    This class handles the paginization for all the screens.
    '''
    
    paging_buttons = ObjectProperty()
    '''
    Reference to paging_buttons in PagingWidgets.
    defaults to: ''
    '''

    page_number = StringProperty('PAGE 2/12')
    '''
    Reference to page_number in PagingWidgets.
    defaults to: 'PAGE 2/12'
    '''

    database_content = ListProperty()
    '''
    Reference to database_content in PagingWidgets.
    defaults to: []
    '''

    current_page = NumericProperty(1)
    '''
    Reference to current_page in PagingWidgets.
    defaults to: '1'
    '''

    prev_page = NumericProperty(1)
    '''
    Reference to prev_page in PagingWidgets.
    defaults to: '1'
    '''

    def __init__(self, **kwargs):
        super(PagingWidget, self).__init__(**kwargs)
        self.initiate_widgets(**kwargs)

    def refresh_database_content(self):
        '''
        Method used to refresh the data extracted from the database.
        '''
        self.database_content = get_running_app().refresh_content()


    def initiate_widgets(self, **kwargs):
        '''
        Initiate all the widgets attached to Paging widget.
        '''
        self.database_content = get_running_app().db_content()
        self.database_content = self.database_content
        counter = 0
        for i in range(0, len(self.database_content)):
            if self.database_content[i][2] and self.database_content[i][6] and self.database_content[i][1]:
                counter+=1
        self.content_length = counter
        self.total_pages = int(math.ceil(self.content_length/7.))
        self.current_page = 1
        self.page_number = "PAGE " + str(self.current_page) + "/" + str(self.total_pages)

        self.filter = kwargs.get('filters')
        self.selectable_filter_grid = kwargs.get('grid_class')
        self.page_label = InfoLabelMedium2(halign='right', valign='bottom', 
                                           color=(0, 0, 0, 1), text='{}'.format(self.page_number))
        box = BoxLayout(orientation='horizontal', padding=(5, 5), spacing=15)
        prev_but = RectShadowButton(text='Ant.', size_hint_x=.3, color=(0, 0, 0, 1),
                                    on_release=partial(self.show_page, self.filter))
        #box.
        inner_box = BoxLayout(orientation='horizontal', spacing=15)
        box.add_widget(prev_but)
        if self.total_pages <= 7:
            for i in range(self.total_pages):
                inner_box.add_widget(RectShadowButton(text=str(i+1), size_hint_x=None,
                                                      size=(100, self.size[1]), color=(0, 0, 0, 1), 
                                                      on_release=partial(self.show_page, self.filter)))
        else:
            inner_box.add_widget(RectShadowButton(text=str(self.current_page), size_hint_x=None,
                                                  size=(100, self.size[1]), color=(0, 0, 0, 1),
                                                  on_release=partial(self.show_page, self.filter)))
            inner_box.add_widget(RectShadowButton(text=str(self.current_page+1), size_hint_x=None,
                                                  size=(100, self.size[1]), color=(0, 0, 0, 1),
                                                  on_release=partial(self.show_page, self.filter)))
            inner_box.add_widget(RectShadowButton(text=str(self.current_page+2), size_hint_x=None,
                                                  size=(100, self.size[1]), color=(0, 0, 0, 1),
                                                  on_release=partial(self.show_page, self.filter)))
            inner_box.add_widget(Label(text='...', color=(0, 0, 0, 1)))
            inner_box.add_widget(RectShadowButton(text=str(self.total_pages-2), size_hint_x=None,
                                                  size=(100, self.size[1]), color=(0, 0, 0, 1),
                                                  on_release=partial(self.show_page, self.filter)))
            inner_box.add_widget(RectShadowButton(text=str(self.total_pages-1), size_hint_x=None,
                                                  size=(100, self.size[1]), color=(0, 0, 0, 1),
                                                  on_release=partial(self.show_page, self.filter)))
            inner_box.add_widget(RectShadowButton(text=str(self.total_pages), size_hint_x=None,
                                                  size=(100, self.size[1]), color=(0, 0, 0, 1),
                                                  on_release=partial(self.show_page, self.filter)))
        box.add_widget(inner_box)

        next_but = RectShadowButton(text='Sig.', size_hint_x=.3, color=(0, 0, 0, 1),
                                    on_release=partial(self.show_page, self.filter))

        box.add_widget(next_but)
        self.add_widget(box)
        self.add_widget(self.page_label)

    def get_addable_widgets(self):
        list_ = []
        for i in range(self.content_length/7):
            list_.append(7)
        list_.append(self.content_length%7)
        return list_

    def split_text(self, text):
        '''
        Not really used anywhere right now.
        '''
        return text.split('[color=0000]')[1].split('[/color]')[0]

    def update_page(self):
        '''
        Updates the page numbers.
        '''
        self.page_label.text = "PAGE " + str(self.current_page) + \
                               +"/" + str(self.total_pages)

    def get_each_page(self):
        '''
        Returns all the pages in the form of a dictionary.
        Divivded like 7,7,7,1 if there are suposed to be 22 pages.
        '''
        dict_ = {}
        temp=0
        for i in range(self.total_pages):
            temp_list=[]
            if i == self.total_pages-1:
                for j in range(self.content_length%7):
                    temp_list.append(self.database_content[j])
            else:
                for j in range(7*i, (7*i)+7):
                    temp+=1
                    temp_list.append(self.database_content[j])
            dict_[i] = temp_list
        return dict_

    def show_page(self, filters, button): 
        '''
        This is an important method for adding widgets to the selectable grid.
        '''
        if button.text == 'Ant.':
            if self.prev_page > 1:
                self.current_page = self.prev_page-1
        elif button.text == 'Sig.':
            if self.prev_page < self.total_pages:
                self.current_page = self.prev_page + 1
        else:
            self.current_page = int(button.text)
        self.prev_page = self.current_page
        self.update_page()
        translate_to_english = {'UBICACION': 'LOCATION',
             'DESIGNACION': 'DESIGNATION',
             'PROVEEDOR': 'PROVIDOR',
             'FECHA': 'DATE',
             'TERNA': 'TERNA',
             'LOTE': 'LOT',
             'N2 SERIE': 'N2 SERIES',
             'CANTIDAD': 'QUANTITY',
             'CADUCIDAD': 'EXPIRATION'}
        self.filters = filters

        if not self.filters:
            count=0
            #page_details = self.get_each_page()
            selectable_grid = get_inventory_screen().ids['selectable_grid']
            selectable_grid.clear_widgets()

            temp = []
            for i in range(0, len(self.database_content)):
                if self.database_content[i][2] and self.database_content[i][6] and self.database_content[i][1]:
                    temp.append(i)
            end = self.current_page*7
            start = (self.current_page-1)*7
            for i in temp[start:end]:
                try:
                    if self.database_content[i][2] == True:
                        if self.database_content[i][11] is None:
                            order_code = self.database_content[i][10]
                        else:
                            order_code = self.database_content[i][11]
                        selectable_grid.add_widget(InventoryWidget(provider_name=self.database_content[i][8],
                                                                   order_code=order_code,
                                                                   location=self.database_content[i][9],
                                                                   provider_ref=self.database_content[i][12],
                                                                   quantity=self.database_content[i][7],
                                                                   line_detail_id=self.database_content[i][3],
                                                                   created_date=self.database_content[i][1],
                                                                   line_serial_no=self.database_content[i][5],
                                                                   description=self.database_content[i][13],
                                                                   expire_date=self.database_content[i][6]))
                        count+=1
                except:
                    selectable_grid.add_widget(InfoLabelMedium2(text="[color=0000]{}[/color]".format(self.database_content[i][0]),
                                                                font_size=28, halign='center', valign='middle'))
                    count+=1

            if count < 7:
                for i in range(count, 7):
                    selectable_grid.add_widget(InfoLabelMedium2())

        else:
            self.selectable_filter_grid.clear_widgets()
            count=0
            temp = []
            for i in self.filters.keys():
                self.key=0
                if i in translate_to_english.keys():
                    if translate_to_english[i] == 'LOCATION':
                        self.key = 9
                        self.value = self.filters['UBICACION']
                    if translate_to_english[i] == 'DESIGNATION':
                        self.key = 7
                        self.value = self.filters['DESIGNACION']
                    if translate_to_english[i] == 'PROVIDOR':
                        self.key = 8
                        self.value = self.filters['PROVEEDOR']
                    if translate_to_english[i] == 'DATE':
                        self.key = 7
                        self.value = self.filters['FECHA']
                    if translate_to_english[i] == 'TERNA':
                        self.key = 7
                        self.value = self.filters['TERNA']
                    if translate_to_english[i] == 'LOT':
                        self.key = 7
                        self.value = self.filters['LOTE']
                    if translate_to_english[i] == 'N2 SERIES':
                        self.key = 7
                        self.value = self.filters['N2 SERIE']
                    if translate_to_english[i] == 'QUANTITY':
                        self.key = 7
                        self.value = self.filters['CANTIDAD']
                    if translate_to_english[i] == 'EXPIRATION':
                        self.key = 6
                        self.value = self.filters['CADUCIDAD']
                try:
                    for i in range(0, len(self.database_content)):
                        for j in self.value:
                            if str(self.database_content[i][self.key]) == str(j) and self.database_content[i][2]:
                                temp.append(i)

                    end = self.current_page*7
                    start = (self.current_page-1)*7
                    for i in temp[start:end]:
                        if self.database_content[i][11] is None:
                            order_code = self.database_content[i][10]
                        else:
                            order_code = self.database_content[i][11]
                        self.selectable_filter_grid.add_widget(InventoryWidget(provider_name=self.database_content[i][8],
                                                                               order_code=order_code,
                                                                               location=self.database_content[i][9],
                                                                               provider_ref=self.database_content[i][12],
                                                                               quantity=self.database_content[i][7],
                                                                               line_detail_id=self.database_content[i][3],
                                                                               created_date=self.database_content[i][1],
                                                                               line_serial_no=self.database_content[i][5],
                                                                               description=self.database_content[i][13],
                                                                               expire_date=self.database_content[i][6]))
                        count+=1
                            
                except:
                    self.selectable_filter_grid.add_widget(InfoLabelMedium2())
            if count < 7:
                for i in range(count, 7):
                    self.selectable_filter_grid.add_widget(InfoLabelMedium2())


class SelectableGrid(CompoundSelectionBehavior, GridLayout):
    '''
    We are calling the database in this class itself, and then it will be used in all the
    other classes and file via accessing the database_content global variable.
    '''

    database_content = ListProperty()

    prev_selection = ObjectProperty()


    def __init__(self, **kwargs):
        """ Use the initialize method to bind to the keyboard to enable
        keyboard interaction e.g. using shift and control for multi-select.
        """
        super(SelectableGrid, self).__init__(**kwargs)
        keyboard = Window.request_keyboard(None, self)
        keyboard.bind(on_key_down=self.select_with_key_down,
                      on_key_up=self.select_with_key_up)
        self.cols=1

        self.initiate_widgets(**kwargs)
        

    def refresh_database_content(self):
        '''
        Method used to refresh the data extracted from the database.
        '''
        self.database_content = refresh_content()


    def initiate_widgets(self, **kwargs):
        '''
        Initiate all the widgets.
        '''

        self.filters = kwargs.get('filters')
        self.database_content = get_running_app().db_content()
        #print self.database_content
        '''
        Getting the data from the database.
        '''

        translate_to_english = {'UBICACION': 'LOCATION',
             'DESIGNACION': 'DESIGNATION',
             'PROVEEDOR': 'PROVIDOR',
             'FECHA': 'DATE',
             'TERNA': 'TERNA',
             'LOTE': 'LOT',
             'N2 SERIE': 'N2 SERIES',
             'CANTIDAD': 'QUANTITY',
             'CADUCIDAD': 'EXPIRATION'}

        if not self.filters:
            temp = []
            for i in range(0, len(self.database_content)):
                if self.database_content[i][2] and self.database_content[i][6] and self.database_content[i][1]:
                    temp.append(i)
            for i in temp[:7]:
                if self.database_content[i][11] is None:
                    order_code = self.database_content[i][10]
                else:
                    order_code = self.database_content[i][11]
                self.add_widget(InventoryWidget(provider_name=self.database_content[i][8],
                                                order_code=order_code,
                                                location=self.database_content[i][9],
                                                provider_ref=self.database_content[i][12],
                                                quantity=self.database_content[i][7],
                                                line_detail_id=self.database_content[i][3],
                                                created_date=self.database_content[i][1],
                                                line_serial_no=self.database_content[i][5],
                                                description=self.database_content[i][13],
                                                expire_date=self.database_content[i][6]))
            else:
                self.add_widget(InfoLabelMedium2())

        else:
            count=0
            temp = []
            for i in self.filters.keys():
                self.key=0
                if i in translate_to_english.keys():
                    if translate_to_english[i] == 'LOCATION':
                        self.key = 9
                        self.value = self.filters['UBICACION']
                    if translate_to_english[i] == 'DESIGNATION':
                        self.key = 7
                        self.value = self.filters['DESIGNACION']
                    if translate_to_english[i] == 'PROVIDOR':
                        self.key = 8
                        self.value = self.filters['PROVEEDOR']
                    if translate_to_english[i] == 'DATE':
                        self.key = 7
                        self.value = self.filters['FECHA']
                    if translate_to_english[i] == 'TERNA':
                        self.key = 7
                        self.value = self.filters['TERNA']
                    if translate_to_english[i] == 'LOT':
                        self.key = 7
                        self.value = self.filters['LOTE']
                    if translate_to_english[i] == 'N2 SERIES':
                        self.key = 7
                        self.value = self.filters['N2 SERIE']
                    if translate_to_english[i] == 'QUANTITY':
                        self.key = 7
                        self.value = self.filters['CANTIDAD']
                    if translate_to_english[i] == 'EXPIRATION':
                        self.key = 6
                        self.value = self.filters['CADUCIDAD']
                try:
                    
                    for i in range(0, len(self.database_content)):
                        for j in self.value:
                            if str(self.database_content[i][self.key]) == str(j):
                                if self.database_content[i][2] == True:
                                    temp.append(i)

                    for i in temp[:7]:
                        if self.database_content[i][11] is None:
                            order_code = self.database_content[i][10]
                        else:
                            order_code = self.database_content[i][11]
                        self.add_widget(InventoryWidget(provider_name=self.database_content[i][8],
                                                        order_code=order_code,
                                                        location=self.database_content[i][9],
                                                        provider_ref=self.database_content[i][12],
                                                        quantity=self.database_content[i][7],
                                                        line_detail_id=self.database_content[i][3],
                                                        created_date=self.database_content[i][1],
                                                        line_serial_no=self.database_content[i][5],
                                                        description=self.database_content[i][13],
                                                        expire_date=self.database_content[i][6]))
                        count+=1
                except:
                    self.add_widget(InfoLabelMedium2())
            if count < 7:
                for i in range(count, 7):
                    self.add_widget(InfoLabelMedium2())

    def clear_widget(self):
        return super(SelectableGrid, self).clear_widget(self)

    def add_widget(self, widget):
        """ Override the adding of widgets so we can bind and catch their
        *on_touch_down* events. """
        widget.bind(on_touch_down=self.button_touch_down,
                    on_touch_up=self.button_touch_up)
        return super(SelectableGrid, self).add_widget(widget)

    def click_down_effect(self, button):
        '''
        click down effect.
        '''
        self.prev_selection = button
        with button.canvas.before:
            Color(rgba = (250/255., 247/255., 233/255., 1)),
            Rectangle(pos=button.pos, size=(button.size))
        
    def click_up_effect(self, button):
        '''
        click up effect.
        '''
        with button.canvas.before:
            Color(rgba = (254/255., 255/255., 255/255., 1)),
            Rectangle(pos=button.pos, size=(button.size))

    def button_touch_down(self, button, touch):
        """ Use collision detection to select buttons when the touch occurs
        within their area. """
        if button.collide_point(*touch.pos):
            #print button.parent.size
            self.click_down_effect(button)
            self.select_with_touch(button, touch)

    def button_touch_up(self, button, touch):
        """ Use collision detection to de-select buttons when the touch
        occurs outside their area and *touch_multiselect* is not True. """
        if not (button.collide_point(*touch.pos) or self.touch_multiselect):
            self.click_up_effect(button)
            self.deselect_node(button)

    def select_node(self, node):
        #node.background_color = (1, 0, 0, 1)
        self.click_down_effect(node)
        return super(SelectableGrid, self).select_node(node)

    def deselect_node(self, node):
        #node.background_color = (1, 1, 1, 1)
        self.click_up_effect(node)
        return super(SelectableGrid, self).deselect_node(node)

    def on_selected_nodes(self, gird, nodes):
        #print("Selected nodes = {0}".format(nodes))
        #self.click_down_effect(grid)
        pass
