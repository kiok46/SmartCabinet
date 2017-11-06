'''
Filter Screen.
'''

from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (ObjectProperty, StringProperty,
                             ListProperty, DictProperty, NumericProperty)
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.button import Button
from kivy.core.window import Window
from cabinet.layouts import GreyInfoBox, GreyInfoGrid
from cabinet.helper import *
from cabinet.labels import InfoLabelMedium2
from cabinet.buttons import SelectableButton, KeyboardButton
from kivy.uix.behaviors.compoundselection import CompoundSelectionBehavior


__all__ = ('FilterScreen', 'FilterWidget', 'KeyboardWidget',
           'SelectableFilter', 'KeyboardButton')


class FilterWidget(GreyInfoBox):
    '''
    Container of all the filter widgets.
    '''
    active_quantity = StringProperty()
    '''
    Reference to active filter info label.
    '''
    active_filters = ObjectProperty()
    '''
    Reference to active filters.
    '''
    selectable_filter = ObjectProperty()
    '''
    Reference to selectable filter.
    '''

    def trash(self):
        self.selectable_filter.do_trash()

    def move_up(self):
        pass

    def move_down(self):
        pass


class ActiveFilters(GridLayout, CompoundSelectionBehavior):
    '''
    Active Filter class, deals with all the functionality related to active
    filters.
    '''
    keys_dict = DictProperty([])
    '''
    Contains the instance of all the widgets dynamically created in the python side.
    '''

    def __init__(self, **kwargs):
        super(ActiveFilters, self).__init__(**kwargs)
        self.cols=1
        self.padding=(20, 3)
        self.keys_dict['select_filter_grid'] = self
        paging_gl = GreyInfoGrid(size_hint_y=.15, cols=1)
        self.keys_dict['paging_info_grid'] = paging_gl
        self.add_widget(paging_gl)
        self.number_of_filters=0

    def add_filter(self, text=''):
        '''
        Adds filters to the grid.
        '''
        self.keys_dict['select_filter_grid'].add_widget(SelectableButton(text=text, 
                                                                         on_touch_down=self.do_touch))
        #if self.number_of_filters
        self.number_of_filters+=1

    def remove_filter(self):
        '''
        Removes filters from the grid.
        Note:
            Not used anywhere as of now, might be useful in future.
        '''
        self.remove_widget(self.keys_dict['select_filter_grid'])
        self.number_of_filters-=1


    def select_node(self, node):
        '''
        Triggered when the filter is selected.
        '''
        node.background_normal = ''
        node.background_color = (250/255., 247/255., 233/255., 1)
        return super(ActiveFilters, self).select_node(node)

    def deselect_node(self, node):
        '''
        Triggered when the filter is deselected.
        '''
        node.background_normal = ''
        node.background_color = (238/255., 243/255., 246/255., 1)
        return super(ActiveFilters, self).deselect_node(node)

    def do_touch(self, instance, touch):
        '''
        Triggered when the filter is touched.
        '''
        if ('button' in touch.profile and touch.button in
            ('scrollup', 'scrolldown', 'scrollleft', 'scrollright')) or\
            instance.collide_point(*touch.pos):
            self.select_with_touch(instance, touch)
        else:
            return False
        return True


class SelectableFilter(GridLayout, CompoundSelectionBehavior):
    '''
    Implements the selectable filter class, responsible for all the behaviors of
    selectable filters.
    '''
    keys_dict = DictProperty([])
    '''
    Contains the instance of all the widgets dynamically created in the python side.
    '''

    selected_filters = ListProperty()
    '''
    List of selectable filters.
    '''

    active_filter_dict = DictProperty()
    '''
    dictionary of active filters.
    '''

    current_selection = ObjectProperty()
    '''
    Holds the current selectef filter.
    '''

    selectable_labels = ListProperty(['UBICACION', 'DESIGNACION', 'PROVEEDOR',
                                      'FECHA', 'TERNA', 'LOTE', 'N2 SERIES',
                                      'CANTIDAD', 'CADUCIDAD'])
    '''
    Manually added label filters.
    Note:
        Not all filters are put in use yet.
    '''

    def __init__(self, **kwargs):
        super(SelectableFilter, self).__init__(**kwargs)

        self.cols=1
        self.padding=(20, 3)
        self.keys_dict['select_filter_grid'] = self
        gl = GreyInfoGrid(size_hint_y=.15, cols=1)
        self.keys_dict['select_filter_grid'] = self
        for i in self.selectable_labels:
            gl.add_widget(SelectableButton(text=str(i),
                                           on_touch_down=self.do_touch,
                                           size_hint_y= .1))
        self.add_widget(gl)

    def do_trash(self):
        '''
        Method that is called when user presses the trash button.
        This method deletes the selectable filter from the grid.
        '''
        try:
            if self.selected_nodes:
                self.parent.ids['active_filters'].keys_dict['select_filter_grid'].clear_widgets()
                self.selected_filters.remove(self.selected_nodes[0].text) 
                self.active_filter_dict.pop(self.selected_nodes[0].text)
                #self.self.selected_filters.pop(self.selected_nodes[0].text)
                #print self.active_filter_dict
                for j in self.active_filter_dict.values():
                    self.parent.ids['active_filters'].keys_dict['select_filter_grid'].add_widget(j)
                self.selected_nodes = []
                self.parent.active_quantity = str(len(self.selected_filters))
        except:
            pass

    def do_add_filter(self, filter_name):
        '''
        Adds a new filter to the grid.
        '''
        try:
            node = self.selected_nodes[0]
            if ("{}-{}".format(node.text, filter_name)) in self.selected_filters:
                pass
            if filter_name == '':
                pass
            else:
                self.selected_filters.append("{}-{}".format(node.text, filter_name))
                self.parent.ids['active_filters'].keys_dict['select_filter_grid'].clear_widgets()
                for i in self.selected_filters:
                    sb = SelectableButton(text=i, on_touch_down=self.do_touch)
                    self.active_filter_dict[node.text+'-'+ filter_name] = sb
                    self.parent.ids['active_filters'].keys_dict['select_filter_grid'].add_widget(sb)
                self.parent.active_quantity = str(len(self.selected_filters))
        except:
            pass

    def select_node(self, node):
        '''
        Triggered when the filter is selected.
        '''
        node.background_normal = ''
        node.background_color = (250/255., 247/255., 233/255., 1)
        return super(SelectableFilter, self).select_node(node)

    def deselect_node(self, node):
        '''
        Triggered when the filter is deselected.
        '''
        node.background_normal = ''
        node.background_color = (238/255., 243/255., 246/255., 1)
        return super(SelectableFilter, self).deselect_node(node)

    def do_touch(self, instance, touch):
        '''
        Triggered when the filter is touched.
        '''
        if ('button' in touch.profile and touch.button in
            ('scrollup', 'scrolldown', 'scrollleft', 'scrollright')) or\
            instance.collide_point(*touch.pos):
            self.select_with_touch(instance, touch)
        else:
            return False
        return True


class KeyboardWidget(GreyInfoGrid):
    '''
    This class handles the actions performed by the Keyboard Widget.
    '''
    keyboard_widget = ListProperty(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', 'AND',
                                    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', ',', 'OR',
                                    'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '/', 'NOT',
                                    'Z', 'X', 'C', 'V', 'B', 'N', 'M', ' ', ':', 'DEL', '.', 'OK'])

    def __init__(self, **kwargs):
        super(KeyboardWidget, self).__init__(**kwargs)
        self.cols = 12
        self.register_event_type('on_ok')
        for i in self.keyboard_widget:
            self.add_widget(KeyboardButton(text=i, on_release=self.key_released))

    def key_released(self, button):
        '''
        Decides which method to call after a button is released/pressed.
        '''
        if button.text == 'OK':
            self.dispatch('on_ok')
        elif button.text == 'NOT':
            pass
        elif button.text == 'OR':
            pass
        elif button.text == 'AND':
            pass
        elif button.text == 'DEL':
            self.eval_del()
        else:
            get_filter_screen().ids['text_input'].text += button.text 

    def eval_add(self, a, b):
        '''
        To introduce "ADD" functionality in filters.
        '''
        return (a+b)

    def eval_or(self, a, b):
        '''
        To introduce "OR" functionality in filters.
        '''
        return (a or b)

    def eval_not(self, a, b):
        '''
        To introduce "NOT" functionality in filters.
        '''
        pass
        #return (a not b)

    def eval_del(self):
        '''
        To introduce "DEL" functionality in filters.
        '''
        get_filter_screen().ids['text_input'].text = ''

    def on_ok(self):
        '''
        This is an event that triggers the further functionality after the "OK" is pressed in the filter screen.
        '''
        get_filter_screen().filter_widget.selectable_filter.do_add_filter(filter_name=get_filter_screen().ids['text_input'].text)
        get_filter_screen().ids['text_input'].text = ''
        #print get_filter_screen().filter_widget.selectable_filter.active_filter_dict


class FilterScreen(BoxLayout):
    '''
    This filter screen class which handles all the functioning related to the
    filter screen.
    '''

    keyboard_widget = ObjectProperty()
    '''
    reference to the keyboard widget.
    '''

    filter_widget = ObjectProperty()
    '''
    reference to the finter widget.
    '''

    def on_ok(self):
        #self.parent.parent.parent.ids['inventory_screen'].move_up
        #get_screen_manager().current = 'inventory'

        from cabinet.behaviors import SelectableGrid, PagingWidget
        from cabinet.labels import LightGreyCanvasLabel
        get_screen_manager().current = 'inventory'
        filters = get_filter_screen().filter_widget.selectable_filter.active_filter_dict

        def sort_filters(filters):
            '''
            returns the dict to specify the filters.
            for example:
                {u'CANTIDAD': [u'3']}
                {u'CANTIDAD': [u'5', u'3']}
            '''
            dict_of_filters = {}
            list_of_values = []
            for i in filters.keys():
                a, b = i.split('-')
                # list_of_filters.append(b)
                if a in dict_of_filters.keys():
                    dict_of_filters[a].append(b)
                    list_of_values = []
                else:
                    list_of_values.append(b)
                    dict_of_filters[a] = list_of_values
            return dict_of_filters

        filter_ = sort_filters(filters)
        if filter_:
            inventory_with_filters = get_inventory_screen().ids['inventory_area']
            sg = get_inventory_screen().ids['selectable_grid']
            #sg.clear_widgets()
            #inventory_with_filters.remove_widget(sg)
            inventory_with_filters.clear_widgets()
            selectable_grid = SelectableGrid(cols=1, filters=filter_)
            paging_widget = PagingWidget(size_hint_y= .1,
                                         filters=filter_,
                                         grid_class=selectable_grid)
            mcl = LightGreyCanvasLabel(size_hint_y= .1)
            inventory_with_filters.add_widget(selectable_grid, index=2)
            inventory_with_filters.add_widget(mcl)
            inventory_with_filters.add_widget(paging_widget)
        
        #selectable_grid.clear_widgets()

    def reorder(self):
        '''
        Reorder the filters according to the alphabets.
        '''
        pass
