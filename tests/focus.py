'''
Focus Behavior
==============

'''

__all__ = ('FocusBehavior', )

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.properties import OptionProperty, ObjectProperty, BooleanProperty, \
    AliasProperty
from kivy.config import Config
from kivy.base import EventLoop

# When we are generating documentation, Config doesn't exist
_is_desktop = False
_keyboard_mode = 'system'
if Config:
    _is_desktop = Config.getboolean('kivy', 'desktop')
    _keyboard_mode = Config.get('kivy', 'keyboard_mode')


class FocusBehavior(object):
    '''Provides keyboard focus behavior. When combined with other
    FocusBehavior widgets it allows one to cycle focus among them by pressing
    tab. Please see the
    :mod:`focus behavior module documentation <kivy.uix.behaviors.focus>`
    for more information.

    .. versionadded:: 1.9.0

    '''

    _requested_keyboard = False
    _keyboard = ObjectProperty(None, allownone=True)
    _keyboards = {}

    ignored_touch = []
    '''A list of touches that should not be used to defocus. After on_touch_up,
    every touch that is not in :attr:`ignored_touch` will defocus all the
    focused widgets if the config keyboard mode is not multi. Touches on
    focusable widgets that were used to focus are automatically added here.

    Example usage::

        class Unfocusable(Widget):

            def on_touch_down(self, touch):
                if self.collide_point(*touch.pos):
                    FocusBehavior.ignored_touch.append(touch)

    Notice that you need to access this as a class, not an instance variable.
    '''

    def _set_keyboard(self, value):
        focus = self.focus
        keyboard = self._keyboard
        keyboards = FocusBehavior._keyboards
        if keyboard:
            self.focus = False    # this'll unbind
            if self._keyboard:  # remove assigned keyboard from dict
                del keyboards[keyboard]
        if value and not value in keyboards:
            keyboards[value] = None
        self._keyboard = value
        self.focus = focus

    def _get_keyboard(self):
        return self._keyboard
    keyboard = AliasProperty(_get_keyboard, _set_keyboard,
                             bind=('_keyboard', ))
    '''The keyboard to bind to (or bound to the widget) when focused.

    When None, a keyboard is requested and released whenever the widget comes
    into and out of focus. If not None, it must be a keyboard, which gets
    bound and unbound from the widget whenever it's in or out of focus. It is
    useful only when more than one keyboard is available, so it is recommended
    to be set to None when only one keyboard is available.

    If more than one keyboard is available, whenever an instance gets focused
    a new keyboard will be requested if None. Unless the other instances lose
    focus (e.g. if tab was used), a new keyboard will appear. When this is
    undesired, the keyboard property can be used. For example, if there are
    two users with two keyboards, then each keyboard can be assigned to
    different groups of instances of FocusBehavior, ensuring that within
    each group, only one FocusBehavior will have focus, and will receive input
    from the correct keyboard. See `keyboard_mode` in :mod:`~kivy.config` for
    more information on the keyboard modes.

    **Keyboard and focus behavior**

    When using the keyboard, there are some important default behaviors you
    should keep in mind.

    * When Config's `keyboard_mode` is multi, each new touch is considered
      a touch by a different user and will set the focus (if clicked on a
      focusable) with a new keyboard. Already focused elements will not lose
      their focus (even if an unfocusable widget is touched).

    * If the keyboard property is set, that keyboard will be used when the
      instance gets focused. If widgets with different keyboards are linked
      through :attr:`focus_next` and :attr:`focus_previous`, then as they are
      tabbed through, different keyboards will become active. Therefore,
      typically it's undesirable to link instances which are assigned
      different keyboards.

    * When a widget has focus, setting its keyboard to None will remove its
      keyboard, but the widget will then immediately try to get
      another keyboard. In order to remove its keyboard, rather set its
      :attr:`focus` to False.

    * When using a software keyboard, typical on mobile and touch devices, the
      keyboard display behavior is determined by the
      :attr:`~kivy.core.window.WindowBase.softinput_mode` property. You can use
      this property to ensure the focused widget is not covered or obscured.

    :attr:`keyboard` is an :class:`~kivy.properties.AliasProperty` and defaults
    to None.

    .. warning:

        When assigning a keyboard, the keyboard must not be released while
        it is still assigned to an instance. Similarly, the keyboard created
        by the instance on focus and assigned to :attr:`keyboard` if None,
        will be released by the instance when the instance loses focus.
        Therefore, it is not safe to assign this keyboard to another instance's
        :attr:`keyboard`.
    '''

    is_focusable = BooleanProperty(_is_desktop)
    '''Whether the instance can become focused. If focused, it'll lose focus
    when set to False.

    :attr:`is_focusable` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to True on a desktop (i.e. `desktop` is True in
    :mod:`~kivy.config`), False otherwise.
    '''

    focus = BooleanProperty(False)
    '''Whether the instance currently has focus.

    Setting it to True will bind to and/or request the keyboard, and input
    will be forwarded to the instance. Setting it to False will unbind
    and/or release the keyboard. For a given keyboard, only one widget can
    have its focus, so focusing one will automatically unfocus the other
    instance holding its focus.

    When using a software keyboard, please refer to the
    :attr:`~kivy.core.window.WindowBase.softinput_mode` property to determine
    how the keyboard display is handled.

    :attr:`focus` is a :class:`~kivy.properties.BooleanProperty` and defaults to
    False.
    '''

    focused = focus
    '''An alias of :attr:`focus`.

    :attr:`focused` is a :class:`~kivy.properties.BooleanProperty` and defaults
    to False.

    .. warning::
        :attr:`focused` is an alias of :attr:`focus` and will be removed in
        2.0.0.
    '''

    def _set_on_focus_next(self, instance, value):
        ''' If changing code, ensure following code is not infinite loop:
        widget.focus_next = widget
        widget.focus_previous = widget
        widget.focus_previous = widget2
        '''
        next = self._old_focus_next
        if next is value:   # prevent infinite loop
            return

        if isinstance(next, FocusBehavior):
            next.focus_previous = None
        self._old_focus_next = value
        if value is None or value is StopIteration:
            return
        if not isinstance(value, FocusBehavior):
            raise ValueError('focus_next accepts only objects based'
                             ' on FocusBehavior, or the `StopIteration` class.')
        value.focus_previous = self

    focus_next = ObjectProperty(None, allownone=True)
    '''The :class:`FocusBehavior` instance to acquire focus when
    tab is pressed and this instance has focus, if not `None` or
    `StopIteration`.

    When tab is pressed, focus cycles through all the :class:`FocusBehavior`
    widgets that are linked through :attr:`focus_next` and are focusable. If
    :attr:`focus_next` is `None`, it instead walks the children lists to find
    the next focusable widget. Finally, if :attr:`focus_next` is
    the `StopIteration` class, focus won't move forward, but end here.

    .. note:

        Setting :attr:`focus_next` automatically sets :attr:`focus_previous`
        of the other instance to point to this instance, if not None or
        `StopIteration`. Similarly, if it wasn't None or `StopIteration`, it
        also sets the :attr:`focus_previous` property of the instance
        previously in :attr:`focus_next` to `None`. Therefore, it is only
        required to set one of the :attr:`focus_previous` or
        :attr:`focus_next` links since the other side will be set
        automatically.

    :attr:`focus_next` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    '''

    def _set_on_focus_previous(self, instance, value):
        prev = self._old_focus_previous
        if prev is value:
            return

        if isinstance(prev, FocusBehavior):
            prev.focus_next = None
        self._old_focus_previous = value
        if value is None or value is StopIteration:
            return
        if not isinstance(value, FocusBehavior):
            raise ValueError('focus_previous accepts only objects based'
                             ' on FocusBehavior, or the `StopIteration` class.')
        value.focus_next = self

    focus_previous = ObjectProperty(None, allownone=True)
    '''The :class:`FocusBehavior` instance to acquire focus when
    shift+tab is pressed on this instance, if not None or `StopIteration`.

    When shift+tab is pressed, focus cycles through all the
    :class:`FocusBehavior` widgets that are linked through
    :attr:`focus_previous` and are focusable. If :attr:`focus_previous` is
    `None`, it instead walks the children tree to find the
    previous focusable widget. Finally, if :attr:`focus_previous` is the
    `StopIteration` class, focus won't move backward, but end here.

    .. note:

        Setting :attr:`focus_previous` automatically sets :attr:`focus_next`
        of the other instance to point to this instance, if not None or
        `StopIteration`. Similarly, if it wasn't None or `StopIteration`, it
        also sets the :attr:`focus_next` property of the instance previously in
        :attr:`focus_previous` to `None`. Therefore, it is only required
        to set one of the :attr:`focus_previous` or :attr:`focus_next`
        links since the other side will be set automatically.

    :attr:`focus_previous` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    '''

    keyboard_mode = OptionProperty('auto', options=('auto', 'managed'))
    '''Determines how the keyboard visibility should be managed. 'auto' will
    result in the standard behaviour of showing/hiding on focus. 'managed'
    requires setting the keyboard visibility manually, or calling the helper
    functions :meth:`show_keyboard` and :meth:`hide_keyboard`.

    :attr:`keyboard_mode` is an :class:`~kivy.properties.OptionsProperty` and
    defaults to 'auto'. Can be one of 'auto' or 'managed'.
    '''

    input_type = OptionProperty('text', options=('text', 'number', 'url',
                                                 'mail', 'datetime', 'tel',
                                                 'address'))
    '''The kind of input keyboard to request.

    .. versionadded:: 1.8.0

    :attr:`input_type` is an :class:`~kivy.properties.OptionsProperty` and
    defaults to 'text'. Can be one of 'text', 'number', 'url', 'mail',
    'datetime', 'tel' or 'address'.
    '''

    unfocus_on_touch = BooleanProperty(_keyboard_mode not in
                                       ('multi', 'systemandmulti'))
    '''Whether a instance should lose focus when clicked outside the instance.

    When a user clicks on a widget that is focus aware and shares the same
    keyboard as this widget (which in the case of only one keyboard, are
    all focus aware widgets), then as the other widgets gains focus, this
    widget loses focus. In addition to that, if this property is `True`,
    clicking on any widget other than this widget, will remove focus form this
    widget.

    :attr:`unfocus_on_touch` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to `False` if the `keyboard_mode` in :attr:`~kivy.config.Config`
    is `'multi'` or `'systemandmulti'`, otherwise it defaults to `True`.
    '''

    def __init__(self, **kwargs):
        self._old_focus_next = None
        self._old_focus_previous = None
        super(FocusBehavior, self).__init__(**kwargs)

        self._keyboard_mode = _keyboard_mode
        fbind = self.fbind
        fbind('focus', self._on_focus)
        fbind('disabled', self._on_focusable)
        fbind('is_focusable', self._on_focusable)
        fbind('focus_next', self._set_on_focus_next)
        fbind('focus_previous', self._set_on_focus_previous)

    def _on_focusable(self, instance, value):
        if self.disabled or not self.is_focusable:
            self.focus = False

    def _on_focus(self, instance, value, *largs):
        if self.is_focusable and self.keyboard_mode == 'auto':
            if value:
                self._bind_keyboard()
            else:
                self._unbind_keyboard()

    def _ensure_keyboard(self):
        if self._keyboard is None:
            self._requested_keyboard = True
            keyboard = self._keyboard =\
                EventLoop.window.request_keyboard(
                    self._keyboard_released, self, input_type=self.input_type)
            keyboards = FocusBehavior._keyboards
            if keyboard not in keyboards:
                keyboards[keyboard] = None

    def _bind_keyboard(self):
        self._ensure_keyboard()
        keyboard = self._keyboard

        if not keyboard or self.disabled or not self.is_focusable:
            self.focus = False
            return
        keyboards = FocusBehavior._keyboards
        old_focus = keyboards[keyboard]  # keyboard should be in dict
        if old_focus:
            old_focus.focus = False
            # keyboard shouldn't have been released here, see keyboard warning
        keyboards[keyboard] = self
        keyboard.bind(on_key_down=self.keyboard_on_key_down,
                      on_key_up=self.keyboard_on_key_up,
                      on_textinput=self.keyboard_on_textinput)

    def _unbind_keyboard(self):
        keyboard = self._keyboard
        if keyboard:
            keyboard.unbind(on_key_down=self.keyboard_on_key_down,
                            on_key_up=self.keyboard_on_key_up,
                            on_textinput=self.keyboard_on_textinput)
            if self._requested_keyboard:
                keyboard.release()
                self._keyboard = None
                self._requested_keyboard = False
                del FocusBehavior._keyboards[keyboard]
            else:
                FocusBehavior._keyboards[keyboard] = None

    def keyboard_on_textinput(self, window, text):
        pass

    def _keyboard_released(self):
        self.focus = False

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if (not self.disabled and self.is_focusable and
            ('button' not in touch.profile or
             not touch.button.startswith('scroll'))):
            self.focus = True
            FocusBehavior.ignored_touch.append(touch)
        return super(FocusBehavior, self).on_touch_down(touch)

    @staticmethod
    def _handle_post_on_touch_up(touch):
        ''' Called by window after each touch has finished.
        '''
        touches = FocusBehavior.ignored_touch
        if touch in touches:
            touches.remove(touch)
            return
        if 'button' in touch.profile and touch.button in\
                ('scrollup', 'scrolldown', 'scrollleft', 'scrollright'):
            return
        for focusable in list(FocusBehavior._keyboards.values()):
            if focusable is None or not focusable.unfocus_on_touch:
                continue
            focusable.focus = False

    def get_focus_next(self, focus_dir):
        return self._get_focus_next(focus_dir)

    def _get_focus_next(self, focus_dir):
        current = self
        walk_tree = 'walk' if focus_dir is 'focus_next' else 'walk_reverse'

        while 1:
            # if we hit a focusable, walk through focus_xxx
            while getattr(current, focus_dir) is not None:
                current = getattr(current, focus_dir)
                if current is self or current is StopIteration:
                    return None  # make sure we don't loop forever
                if current.is_focusable and not current.disabled:
                    return current

            # hit unfocusable, walk widget tree
            itr = getattr(current, walk_tree)(loopback=True)
            if focus_dir is 'focus_next':
                next(itr)  # current is returned first  when walking forward
            for current in itr:
                if isinstance(current, FocusBehavior):
                    break
            # why did we stop
            if isinstance(current, FocusBehavior):
                if current is self:
                    return None
                if current.is_focusable and not current.disabled:
                    return current
            else:
                return None

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        '''The method bound to the keyboard when the instance has focus.

        When the instance becomes focused, this method is bound to the
        keyboard and will be called for every input press. The parameters are
        the same as :meth:`kivy.core.window.WindowBase.on_key_down`.

        When overwriting the method in the derived widget, super should be
        called to enable tab cycling. If the derived widget wishes to use tab
        for its own purposes, it can call super after it has processed the
        character (if it does not wish to consume the tab).

        Similar to other keyboard functions, it should return True if the
        key was consumed.
        '''
        if keycode[1] == 'tab':  # deal with cycle
            if ['shift'] == modifiers:
                next = self.get_focus_next('focus_previous')
            else:
                next = self.get_focus_next('focus_next')
            if next:
                self.focus = False

                next.focus = True

            return True
        return False

    def keyboard_on_key_up(self, window, keycode):
        '''The method bound to the keyboard when the instance has focus.

        When the instance becomes focused, this method is bound to the
        keyboard and will be called for every input release. The parameters are
        the same as :meth:`kivy.core.window.WindowBase.on_key_up`.

        When overwriting the method in the derived widget, super should be
        called to enable de-focusing on escape. If the derived widget wishes
        to use escape for its own purposes, it can call super after it has
        processed the character (if it does not wish to consume the escape).

        See :meth:`keyboard_on_key_down`
        '''
        if keycode[1] == 'escape':
            self.focus = False
            return True
        return False

    def show_keyboard(self):
        '''
        Convenience function to show the keyboard in managed mode.
        '''
        if self.keyboard_mode == 'managed':
            self._bind_keyboard()

    def hide_keyboard(self):
        '''
        Convenience function to hide the keyboard in managed mode.
        '''
        if self.keyboard_mode == 'managed':
            self._unbind_keyboard()


class FocusWithColor(FocusBehavior):
    ''' Class that when focused, changes its background color to red.
    '''

    _color = None
    _rect = None

    def __init__(self, **kwargs):
        super(FocusWithColor, self).__init__(**kwargs)
        with self.canvas:
            self._color = Color(1, 1, 1, .2)
            self._rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self._rect.pos = instance.pos
        self._rect.size = instance.size

    def on_focused(self, instance, value, *largs):
        self._color.rgba = [1, 1, 0, .2] if value else [1, 1, 1, .2]


class FocusButton(FocusWithColor, Button):
    pass


class FocusLabel(FocusWithColor, Button):

    def on_release(self):
        FocusApp.count = FocusApp.instances.index(self)


class FocusApp(App):

    instances=[]
    count = 0

    def go_right(self, *args):
        temp = self.instances[self.__class__.count].get_focus_next('focus_next')
        temp.focus = True
        self.__class__.count += 1
        if self.__class__.count >= len(self.instances):
            self.__class__.count = 0

    def go_left(self, *args):
        temp = self.instances[self.__class__.count].get_focus_next('focus_previous')
        temp.focus = True
        self.__class__.count -= 1
        if self.__class__.count < 0:
            self.__class__.count = len(self.instances)-1

    def build(self):
        root = BoxLayout(padding=[10, 10], spacing=5)
        root.add_widget(FocusButton(text='Go->.', size_hint_x=0.4,
                                   on_release=self.go_right))
        for i in range(5):
            temp = FocusLabel(text=str(i))
            self.instances.append(temp)
            root.add_widget(temp)

        for i, instance in enumerate(self.instances):
            if i == len(self.instances)-1:
                instance.focus_next = self.instances[0]
            else:
                instance.focus_next = self.instances[i+1]

        root.add_widget(FocusButton(text='<-Go', size_hint_x=0.4,
                                   on_release=self.go_left))

        return root


if __name__ == '__main__':
    FocusApp().run()