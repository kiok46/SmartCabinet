from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.properties import ObjectProperty, StringProperty, DictProperty
from cabinet.layouts import GreyInfoBox
from cabinet.labels import InfoLabelMedium2


class DetailPopup(Popup):

    detailbox = ObjectProperty()
    '''
    Reference to detail box, it contains DetailPopWidget and PageInfo.
    '''

    def __init__(self, **kwargs):
        super(DetailPopup, self).__init__(**kwargs)
        self.details = kwargs.get('details')
        self.quantity = kwargs.get('quantity')

        self.page = 1 # default.
        if int(self.quantity)%13 == 0:
            self.total_pages = int(self.quantity)/13
        else:
            self.total_pages = int(self.quantity)/13 + 1
        self.create_page_list() # get the list of pages.

        quantity_ = str(self.paging_list[self.page-1])
        self.page_number = "PAGE {}/{}".format(str(self.page), str(self.total_pages))
        self.page_info = PageInfo(size_hint_y=.1, page_number=self.page_number)

        self.detailpopwidget = DetailPopWidget(provider_details=self.details,
                                               quantity=quantity_)
        self.detailbox.add_widget(self.detailpopwidget)
        self.detailbox.add_widget(self.page_info)

    def prev_page(self):
        '''
        Handles when the up key is pressed.
        '''
        if self.page == 1:
            pass
        else:
            self.page -= 1
        self.page_info.page_number = "PAGE {}/{}".format(str(self.page),
                                                         str(self.total_pages))
        quantity_ = str(self.paging_list[self.page-1])
        self.detailbox.clear_widgets()
        self.detailpopwidget = DetailPopWidget(provider_details=self.details,
                                               quantity=quantity_)
        self.detailbox.add_widget(self.detailpopwidget)
        self.detailbox.add_widget(self.page_info)        


    def next_page(self):
        '''
        Handles when the down key is pressed.
        '''
        if self.page >= self.total_pages:
            pass
        else:
            self.page += 1
        self.page_info.page_number = "PAGE {}/{}".format(str(self.page),
                                                         str(self.total_pages))
        quantity_ = str(self.paging_list[self.page-1])
        self.detailbox.clear_widgets()
        self.detailpopwidget = DetailPopWidget(provider_details=self.details,
                                               quantity=quantity_)
        self.detailbox.add_widget(self.detailpopwidget)
        self.detailbox.add_widget(self.page_info)   

    def create_page_list(self):
        '''
        Create a item list.
        '''
        div = int(self.quantity)/13
        mod = int(self.quantity)%13
        self.paging_list = []
        for i in range(div):
            self.paging_list.append(str(13))
        if mod != 0:
            self.paging_list.append(str(mod))


class PageInfo(GreyInfoBox):
    page_number = StringProperty("PAGE 1/12")
    '''
    Page number of custom popup.
    Deafults to: "PAGE 1/12"
    '''


class DetailPopWidget(GridLayout):
    provider_details = DictProperty()
    quantity = StringProperty()

    def __init__(self, **kwargs):
        super(DetailPopWidget, self).__init__(**kwargs)
        self.details = kwargs.get('provider_details')
        self.quantity = kwargs.get('quantity')
        self.cols = 1
        self.padding = (20, 3)

        for i in range(0, int(self.quantity)):
            ilm = InfoLabelMedium2(halign= 'left', valign='middle', font_size=28,
                                   size_hint_y= None, size=(self.size[0], dp(35)),
                                   text="[color=0000][font=fonts/Gotham-Black-2]" + \
                                        "CADUCIADA:[/font] {}    [font=fonts/Gotham-".format(self.details['CADUCIDAD']) + \
                                        "Black-2]ENTRADA:[/font]{}    [font=fonts/".format(self.details["N' SERIE"]) + \
                                        "Gotham-Black-2]N' SERIE:[/font] {}[/color]".format(self.details['ENTRADA']))
            #with ilm.canvas:
            #    Color(rgba = (0, 0, 0, 1)),
            #    Line(points=(ilm.x, ilm.y, ilm.x+ilm.width, ilm.y))
            self.add_widget(ilm)
