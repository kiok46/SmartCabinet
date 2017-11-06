'''
Episode Screen.
'''
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from cabinet.helper import get_screen_manager
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.spinner import SpinnerOption, Spinner


__all__ = ('EpisodeScreen', 'EpisodeSummaryBox')


class ESpinnerOption(SpinnerOption):
    pass


class ESpinner(Spinner):
    option_cls = ObjectProperty(ESpinnerOption)

    def __init__(self, **kwargs):
        super(ESpinner, self).__init__(**kwargs)



class EpisodeSummaryBox(BoxLayout):
    product_line = StringProperty('GESTION DE INTERVENCION URGENTE Y NO PROGRAMADA')
    '''
    Reference to product_line in summary box.
    defaults to: 'GESTION DE INTERVENCION URGENTE Y NO PROGRAMADA'
    '''
    product_info_line = StringProperty('ASOCIADA AL PACIENTE NHC 1806040')
    '''
    Reference to product_info_line in summary box.
    defaults to: 'ASOCIADA AL PACIENTE NHC 1806040'
    '''


class EpisodeScreen(BoxLayout):
    '''
    Episode Screen class.
    '''

    product_info_line = StringProperty('1806040 - PEREZ DE LA CRUZ CAAVERIO, JOAQUIN FEDERICO')
    '''
    Reference to product_info_line in summary box.
    defaults to: ''
    '''
    
    date = StringProperty('EPISODIO: ')
    '''
    Reference to product_info_line in summary box.
    defaults to: ''
    '''

    spinner1_ = ObjectProperty()
    spinner1 = StringProperty('CENTRO: ')
    '''
    Reference to product_info_line in summary box.
    defaults to: ''
    '''

    spinner2 = StringProperty('SERVIZO: ')
    '''
    Reference to product_info_line in summary box.
    defaults to: ''
    '''

    spinner3 = StringProperty('SALA: ')
    '''
    Reference to product_info_line in summary box.
    defaults to: ''
    '''

    def __init__(self, **kwargs):
        super(EpisodeScreen, self).__init__(**kwargs)
        self.spinner_1_values = self.add_color_list(['a', 'b', 'c'])

    def add_color_list(self, values):
        temp=[]
        for value in values:
            value = '[color=0000]{}[/color]'.format(value)
            temp.append(value)
        return temp
