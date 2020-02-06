import pygame
import thorpy

import ressources.config
from ressources.sliders import *
from view.statutils import *
from view.button import Button

class Gui:
    """ This class contains user interface utilities : sidebar and progress bar

        Sidebar : The various objects (statistics, sliders and buttons) are stored in thorpy.Box objects

        Thorpy objects hierarchy :

        --- Box: main box self.main_box (the father of all the boxes)

        ------ Box: "Statistics" label box
        --------- Text: "Statistics" label
        ------ Box: box which contains self.stats_box. For each stat :
        --------- Box: horizontal box (contains two statistics)
        ------------ Box: statistic cell
        --------------- Text: stat label
        --------------- Text: stat value
        ...

        ------ Box: Parameters title box
        --------- Text: "Parameters" label
        ------ Box: Slider box. For each parameter :
        --------- Text: Parameter label
        --------- Slider
        ...

        ------ Button

        The main box is stored in a thorpy.Menu object. The thorpy.Menu.update() method updates all the elements that
        it contains.
    """


    def __init__(self, menu_surface):
        """
        Gui constructor
        :param menu_surface: Pygame.Surface object that will be assigned to the sidebar
        """

        # For optimisation purposes to avoid updating the values at each tick, which takes a lot of proc use
        self.isupdate = False

        # Imports the parameters contained in config.py
        self.config = ressources.config.para

        #  For zoom and position
        self.zoom_position = Button("Reset zoom and position",
                                    (1500,
                                     600),
                                    self,
                                    COLOR_ELECTRON_BLUE,
                                    BLACK,
                                    (180, 40),
                                    font_size=14)

        # Default theme
        thorpy.set_theme("human")

        # Generate the elements of the menu
        self.generate_menu()

        # Stylizes the menu
        self.set_style()

        # Assignes menu_surface as main surface for the sidebar
        self.assign_surface(self.menu, menu_surface)

        # Displays the menu
        self.main_box.set_topleft(POS_SURFACE_MENU)

        # Updates the menu
        self.main_box.blit()
        self.main_box.update()

    def generate_menu(self):
        """Creates the elements of the sidebar"""

        # List which contains all of the elements
        self.elements = []

        # Logo
        img = thorpy.Image(path=self.config.image_LOGO)
        self.elements.append(img)

        # Statistics
        self.init_stats_box()

        # Sliders
        self.generate_sliders()

        # Settings button
        self.settings_button = thorpy.make_button("Settings", func=self.settings_button_pressed)
        self.settings_button.set_main_color(BLACK)
        self.elements.append(self.settings_button)

        # Pause button
        self.gui_pause = False
        self.pause_button = thorpy.make_button("Play/Pause", func=self.pause_button_pressed)
        self.pause_button.set_main_color(BLACK)
        self.elements.append(self.pause_button)

        # Quit
        self.gui_quit = False
        self.quit_button = thorpy.make_button("Quit", func=self.quit_button_pressed)
        self.quit_button.set_main_color(BLACK)
        self.elements.append(self.quit_button)

        # Color palette to show velocity
        thorpy.set_theme("human")
        self.color_palette = thorpy.ColorSetter.make()
        self.elements.append(self.color_palette)

        # Stores all the elements in the main box
        thorpy.style.DEF_COLOR = BLACK
        self.main_box = thorpy.Background(color=((0, 0, 0, 100)), elements=self.elements)
        thorpy.store(self.main_box, x=DIM_MENU_X / 2, y=0, mode="v", align="center")

        # Calls react_slider() method when the sliders are updated
        slider_reaction = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                    reac_func=self.react_slider,
                                    event_args={"id": thorpy.constants.EVENT_SLIDE},
                                    reac_name="Reacts to slide event")
        self.main_box.add_reaction(slider_reaction)

        # Stores the main box in a menu
        self.menu = thorpy.Menu(self.main_box)

    def update(self, stats):
        """
            Updates : parameters, statistics, sidebar view.
            :param stats: list that contains the new values of the statistics
        """
        # If there is a slider reaction, then updates the values chosen by the user
        if self.isupdate:
            self.update_values()
            self.isupdate = False

        # Updates statistics
        self.update_stats_box(stats)

        # Updates the sidebar
        self.main_box.blit()
        self.main_box.update()

    def init_stats_box(self):
        """Initialize the statistics box
        Depends on statutils.py"""

        # Statistics menu label
        thorpy.set_theme("classic")
        menu_title = thorpy.make_text("Statistics", font_color=BLACK)
        thorpy.style.DEF_COLOR = (COLOR_ELECTRON_BLUE)
        menu_title_box = thorpy.Box(elements=[menu_title], size=[DIM_MENU_X - 25, 25])
        menu_title_box.set_main_color(COLOR_ELECTRON_BLUE)
        thorpy.set_theme("human")
        self.elements.append(menu_title_box)

        # List to store the statistics
        self.elements_stats = []

        # Wraps each statistic (label and value) in a box and stores it in elements_stats
        # uses statutils.py's init_stats() method to get the labels
        for stat in init_stats():
            text = thorpy.make_text(stat)
            value = thorpy.make_text("")
            stat_box = thorpy.Box(elements=[text, value], size=DIM_STAT_BOX)
            stat_box.set_main_color(BLACK)
            self.elements_stats.append(stat_box)

        # We store them horizontally and we handle the case when there is an uneven number of statistics
        boxesH = []
        for i in range(0, len(self.elements_stats), 2):
            if i + 1 != len(self.elements_stats):
                boxesH.append(thorpy.make_group(elements=[self.elements_stats[i],
                                                          self.elements_stats[i + 1]], mode="h"))
            else:
                boxesH.append(self.elements_stats[i])

        # So we can have white borders and black background
        thorpy.style.DEF_COLOR = BLACK

        # We store each the horizontal boxes in the statistics box
        self.stats_box = thorpy.Box(elements=boxesH)

        # We append the statistics box in our elements list
        self.elements.append(self.stats_box)

    def update_stats_box(self, stats):
        """
        Updates the statistics values.
        Depends on statutils.py
        :param stats: list that contains the new values of the statistics (contains ints, floats and tuples)
        """

        # Creates thorpy text objects to display the new values
        for k in range(len(stats)):
            value = stats[k]
            new_value_text = ""
            # (average, minimum, maximum) tuples
            if type(value) == tuple:
                for i in range(len(value)):
                    new_value_text += '%.2f' % value[i] + "  "
            # Floats
            elif type(value) == float:
                new_value_text += '%.2f' % value[i]
            # Ints
            else:
                new_value_text += str(value)
            # here we may be should raise an exception if is neither an int, float or tuple

            # We replace the old text by the new text
            self.elements_stats[k].get_elements()[1].set_text(new_value_text)

            # We put it just below the label
            self.elements_stats[k].get_elements()[1].stick_to(self.elements_stats[k].get_elements()[0],
                                                              target_side="bottom", self_side="top")

    def generate_sliders(self):
        """ Creates sliders for all the parameters contained in sliders_Config.default{}
            Checks if the Show argument of the parameter is equal to True before creating the slider"""

        # ParametersLabel
        thorpy.set_theme("classic")
        menu_title = thorpy.make_text("Parameters")
        thorpy.style.DEF_COLOR = (COLOR_ELECTRON_BLUE)
        menu_title_box = thorpy.Box(elements=[menu_title], size=[DIM_MENU_X - 25, 25])
        menu_title_box.set_main_color(COLOR_ELECTRON_BLUE)
        self.elements.append(menu_title_box)

        # Theme
        thorpy.set_theme("human")

        # Sliders dictionnary
        self.sliders = {}

        # Box that will contain all the sliders (and their labels)
        box_sliders = []

        # For each parameter with Show=True in sliders
        for name, k in sliders_Config.default.items():
            # If show=True
            if k[4]:

                # Creates the labels
                if k[-1] != "":
                    box_sliders.append(thorpy.make_text(k[-1]))
                else:
                    box_sliders.append(thorpy.make_text(name))

                # Creates the labels
                min = k[0]
                init = k[1]
                max = k[2]
                type = k[3]
                self.sliders[name] = thorpy.SliderX(length=DIM_SLIDER_X, limvals=(min, max), text="",
                                                    initial_value=init, type_=type)

                # Rounds the step of float parameters to 1 decimal
                self.sliders[name]._round_decimals = 1

                # We append the slider to box_sliders
                box_sliders.append(self.sliders[name])

        # some stylizing
        thorpy.set_theme("human")
        thorpy.style.DEF_COLOR = BLACK

        # Appends the sliders to a box, and this box to the main box elements list
        box_sliders = thorpy.Box(box_sliders)
        self.elements.append(box_sliders)

    def set_style(self):
        """Some stylizing"""

        # Main box
        self.main_box.set_main_color(BLACK)

        for slider in self.sliders.values():
            slider.get_dragger().set_main_color(WHITE)
            slider.get_dragger().set_size(DIM_DRAGGER)
            slider.get_slider().set_main_color(WHITE)
            slider.get_slider().set_size(DIM_SLIDER)

        # Due to a bug in thorpy methods, we have to reset the slider values to the values stored in config here
        for name, k in sliders_Config.default.items():
            eval("self.sliders[name].set_value(self.config.%s)" % name)

        # Quit button
        self.set_font_style(self.quit_button, FONT_COLOR, FONT_SIZE, FONT)
        self.quit_button.set_font_color_hover(WHITE)

        # Pause button
        self.set_font_style(self.pause_button, FONT_COLOR, FONT_SIZE, FONT)
        self.pause_button.set_font_color_hover(WHITE)

        # Settings button
        self.set_font_style(self.settings_button, FONT_COLOR, FONT_SIZE, FONT)
        self.pause_button.set_font_color_hover(WHITE)

        # All the boxes boxs
        for element in self.main_box.get_descendants():
            if element.get_text() != "":
                self.set_font_style(element, FONT_COLOR, FONT_SIZE, FONT)
        for element in self.main_box.get_elements():
            element.set_main_color(COLOR_ELECTRON_BLUE_ALPHA)

    def set_font_style(self, element, font_color, font_size, font):
        """
        Assigns a font style to a thorpy text object
        :param element: thorpy.make_text() text object
        :param font_color: (R, G, B) tuple
        :param font_size: int
        :param font: string with the font name
        """
        element.set_font_color(font_color)
        element.set_font_size(font_size)
        element.set_font(font)

    def assign_surface(self, mon_menu, ma_surface):
        """
        Assigns a surface to the elements of a menu
        :param mon_menu: thorpy.Menu object
        :param ma_surface: pygame.Surface object
        """
        for element in mon_menu.get_population():
            element.surface = ma_surface

    def update_values(self):
        """Updates the values chosen by the user in self.config parameters"""
        for name, slider in self.sliders.items():
            exec("self.config.%s=%s" % (name, slider.get_value()))

    def quit_button_pressed(self):
        """Called when the quit button is pressed"""
        self.gui_quit = True

    def settings_button_pressed(self):
        """Called when the settings button is pressed"""
        self.config.settings = True

    def pause_button_pressed(self):
        """Called when the pause button is pressed"""
        self.gui_pause = not self.gui_pause

    # End of sidebar methods
    #######################################################################
    # Beginning of progress_bar methods

    def progress_bar(self, pos, size, progress, screen, bar_color, bg=False, bg_color=BLACK, vertical=False,
                     reverse=False, round=False, radius=20):
        """
        Draws a progress bar /!\ This function works for the project but not all cases are treated
        :param pos sets position of progress bar
        :param size sets size of progress bar
        :param progress is the current progress, between 0 and 1
        :param screen is the screen where the bar should be drawn
        :param bg is background, if is necessary
        :param vertical is wether you want vertical or horizontal bar
        :param reverse make the bar drawing backward (100% -> 0%)
        :param round sets if you want round rectangles or not
        :param radius is the radius of angles if round is True
        """
        if progress < 0:
            progress = 0

        # Useful for life bars
        if bg:
            self.round_rect(screen, pygame.Rect(pos, size), bg_color, radius)

        inner_pos = pos
        if reverse and vertical:
            """
            This case is particular, because pos represent the top left corner, and rect is drawn from pos
            We have to reduce size and lower position to get what we want
            """
            changed_size = size[1] - (size[1] * progress)
            inner_pos = (pos[0], pos[1] + changed_size)
            inner_size = (size[0], size[1] * progress)
        elif not reverse and vertical:
            inner_size = (size[0], progress)
        elif not reverse and not vertical:
            inner_size = (size[0] * progress, size[1])
        if round:
            self.round_rect(screen, pygame.Rect(inner_pos, inner_size), bar_color, radius)
        else:
            pygame.draw.rect(screen, bar_color, pygame.Rect(inner_pos, inner_size))

    # The 2 functions below come from an existing project
    def round_rect(self, surface, rect, color, rad=20):
        """
        Draw a rect with rounded corners to surface.  Argument rad can be specified
        to adjust curvature of edges (given in pixels).  An optional border
        width can also be supplied; if not provided the rect will be filled.
        Both the color and optional interior color (the inside argument) support
        alpha.
        """
        rect = pygame.Rect(rect)
        zeroed_rect = rect.copy()
        zeroed_rect.topleft = 0, 0
        image = pygame.Surface(rect.size).convert_alpha()
        image.fill((0, 0, 0, 0))
        self._render_region(image, zeroed_rect, color, rad)
        return surface.blit(image, rect)

    def _render_region(self, image, rect, color, rad):
        """Helper function for round_rect."""
        corners = rect.inflate(-2 * rad, -2 * rad)
        for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
            pygame.draw.circle(image, color, getattr(corners, attribute), rad)
        image.fill(color, rect.inflate(-2 * rad, 0))
        image.fill(color, rect.inflate(0, -2 * rad))

    def react_slider(self,event):
        self.isupdate = True

    def draw_reset_button(self, screen):
        self.zoom_position = Button("Reset zoom and position",
                                    (screen.get_width() * 0.85,
                                     screen.get_height() * 0.45),
                                    self,
                                    GREEN,
                                    BLACK,
                                    (180, 40),
                                    font_size=14)
        self.zoom_position.draw(screen)

