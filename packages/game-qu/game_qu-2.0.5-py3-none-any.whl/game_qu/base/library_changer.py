from game_qu.base import important_constants
import importlib
from game_qu import library_abstraction


class LibraryChanger:
    """ A class that allows the user to modify constants and other variables instead of actually modifying the code.
        IMPORTANT: All the methods of this class must be called from the second line onwards with the first line being
        from game_qu.base.library_changer import LibraryChanger, so none of the other code is initialized with the old constants."""

    library_has_been_set = False
    current_library_name = ""
    overrided_functions = {}

    @staticmethod
    def set_screen_dimensions(screen_length, screen_height):
            """Sets the dimensions of the screen. IMPORTANT see class description for details on how to call the methods """

            important_constants.SCREEN_LENGTH = screen_length
            important_constants.SCREEN_HEIGHT = screen_height

    @staticmethod
    def set_background_color(background_color):
        """Sets the background color of the screen (doesn't affect anything if an image is the background)"""

        important_constants.BACKGROUND_COLOR = background_color

    @staticmethod
    def set_number_of_frames_history_keeper_stores(number_of_frames_history_keeper_stores):
        """Sets the number of frames the HistoryKeeper keeps in it at one time"""

        important_constants.NUMBER_OF_FRAMES_HISTORY_KEEPER_STORES = number_of_frames_history_keeper_stores

    @staticmethod
    def set_game_library(library_name):
        """ Sets the game library that runs all the code. Here are the valid names:
            'pyglet',
            'pygame'"""

        valid_library_names = ["pyglet", "pygame"]
        LibraryChanger.library_has_been_set = True

        if not valid_library_names.__contains__(library_name):
            raise ValueError(f"Do not recognize 'library_name' {library_name}. Here are the valid values: ['pyglet', 'pygame']")

        if library_name == "pyglet":
            LibraryChanger.current_library_name = library_name
            library_abstraction.keys = importlib.import_module("game_qu.pyglet_abstraction.keys")
            library_abstraction.utility_functions = importlib.import_module("game_qu.pyglet_abstraction.utility_functions")
            library_abstraction.variables = importlib.import_module("game_qu.pyglet_abstraction.variables")

        else:
            LibraryChanger.current_library_name = library_name
            library_abstraction.keys = importlib.import_module("game_qu.pygame_abstraction.keys")
            library_abstraction.utility_functions = importlib.import_module("game_qu.pygame_abstraction.utility_functions")
            library_abstraction.variables = importlib.import_module("game_qu.pygame_abstraction.variables")

    @staticmethod
    def get_library_has_been_set():
        """:returns: bool; whether the library for the game engine has been set"""

        return LibraryChanger.library_has_been_set

    @staticmethod
    def set_important_constant(constant_name, constant_value):
        """Sets the value of the constant with the name 'constant_name' to 'constant_value'"""

        setattr(important_constants, constant_name, constant_value)

    @staticmethod
    def set_is_using_controller(is_using_controller):
        """Sets whether the game will be using a controller (important_constants.IS_USING_CONTROLLER) to 'is_using_controller'"""

        important_constants.IS_USING_CONTROLLER = is_using_controller

    @staticmethod
    def set_full_screen(is_full_screen):
        """Makes the size of the application full screen. NOTE: This only works with pygame"""

        if LibraryChanger.current_library_name == "pygame":
            important_constants.IS_FULL_SCREEN = is_full_screen

        else:
            raise ValueError("Setting to full screen can only be done when the game engine is pygame")

    @staticmethod
    def set_function(function_name, function):
        """ Sets the normal function to the new function provided. For instance, this could override the default rendering
            style. This is generally not recommended unless you know what you are doing"""

        LibraryChanger.overrided_functions[function_name] = function

    @staticmethod
    def get_function(module, function_name):
        """ :returns: function; the normal function if the function was not overrided otherwise the overrided function"""

        return_value = getattr(module, function_name)

        if LibraryChanger.overrided_functions.__contains__(function_name):
            return_value = LibraryChanger.overrided_functions.get(function_name)

        return return_value
