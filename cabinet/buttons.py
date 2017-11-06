import weakref
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Ellipse, Line, Rectangle, BorderImage


__all__ = ('SelectableButton', 'KeyboardButton', 'RectShadowButton',
	       'ImageButton', 'IconButton')


class SelectableButton(Button):
    pass


class KeyboardButton(Button):

    def __init__(self, **kwargs):
        super(KeyboardButton, self).__init__(**kwargs)
        self.color = (0, 0, 0, 1)


class RectShadowButton(ButtonBehavior, Label):
    '''
    Button used in the paginisation.
    '''

    instances = []
    '''
    Stores the instances of the RectShadowButton class.
    '''
    prev_node = None

    def __init__(self, **kwargs):
        super(RectShadowButton, self).__init__(**kwargs)
        self.create_instances()

    def create_instances(self):
        self.__class__.instances.append(weakref.proxy(self))
        if len(self.__class__.instances) == 1:
            self.prev_node = self
        else:
            self.prev_node = self.__class__.instances[len(self.__class__.instances)-1]

    def on_press(self):
        '''     
        Handles the on_press of the paging buttons.
        '''
        with self.canvas.before:
            BorderImage(source= 'icons/active_background.png', size= self.size,
                        pos= self.pos)
      
    def on_release(self):
        '''       
        Handles the on_release of the paging buttons.
        Note:
            If you want to add color to your button after adding the image.
            Use the following:
            `with self.canvas.before:
                Color(rgba = (238/255., 243/255., 246/255., 1))   
                Rectangle(pos=self.pos, size=(self.size))`
        '''
        try:
            for i, instance in enumerate(RectShadowButton.instances):
                if instance.text == 'Ant.':
                    with self.prev_node.canvas.before:
                               
                        BorderImage(source= 'icons/active_background.png',
                                    size= self.prev_node.size,
                                    pos= self.prev_node.pos)
                if instance.text == 'Sig.':
                    pass
                if instance.text in ['Ant.', 'Sig.']:
                    with self.canvas.before:      
                        BorderImage(source= 'icons/before_background.png',
                                    size= self.size,
                                    pos= self.pos)
                else:
                    with instance.canvas.before:
                        BorderImage(source= 'icons/number_background.png',
                                    size= instance.size,
                                    pos= instance.pos)

            if not self.text in ['Ant.', 'Sig.']:
                with self.canvas.before:   
                    BorderImage(source= 'icons/active_background.png',
                                size= self.size,
                                pos= self.pos)
        except:
            if self.text in ['Ant.', 'Sig.']:
                with self.canvas.before:   
                    BorderImage(source= 'icons/before_background.png',
                                size= self.size,
                                pos= self.pos)
            if not self.text in ['Ant.', 'Sig.']:
                with self.canvas.before:   
                    BorderImage(source= 'icons/before_background.png',
                                size= self.size,
                                pos= self.pos)


class ImageButton(ButtonBehavior, Image):
    '''
    This widget is not really used anywhere yet, but might be usefull in future.
    Basically adds a buttons behaviour to an image.
    '''

    def on_press(self):
        with self.canvas.before:
            Color(rgba = (250/255., 247/255., 233/255., 1)),
            Rectangle(pos=(self.pos[0], self.pos[1]+1), size=(self.size))

    def on_release(self):
        with self.canvas.before:
            Color(rgba = (254/255., 255/255., 255/255., 1)),
            Rectangle(pos=(self.pos[0], self.pos[1]+1), size=(self.size))


class IconButton(ButtonBehavior, Image):
    '''
    Used in the sidebars as Icon buttons.
    '''

    def on_press(self):
        with self.canvas.before:
            Color(rgba = (250/255., 247/255., 233/255., 1)),
            Rectangle(pos=(self.pos[0], self.pos[1]+1), size=(self.size))

    def on_release(self):
        with self.canvas.before:
            Color(rgba = (249/255., 250/255., 251/255., 1)),
            Rectangle(pos=(self.pos[0], self.pos[1]+1), size=(self.size))
