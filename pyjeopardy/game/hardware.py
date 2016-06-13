class Hardware:
    def __init__(self, name):
        self.name = name

        self.active = False

        self.configdialog = None

        self.all_keys = {}

    def init(self):
        pass

    def get_key_for_name(self, keyname):
        for key, name in self.all_keys.items():
            if name == keyname:
                return key
        return None

    def connect(self):
        pass

    def disconnect(self):
        pass

    def start(self, callback):
        """
        callback receives hardware and key
        """
        pass

    def stop(self):
        pass


class HardwareError(Exception):
    def __init__(self, hardware, error):
        self.hardware = hardware
        self.error = error

    def __str__(self):
        return "{} {}".format(self.hardware.name, self.error)


class Keyboard(Hardware):
    def __init__(self):
        super(Keyboard, self).__init__("Keyboard")

        self.active = True

        for key in range(65, 91):  # A - Z
            self.all_keys[key] = chr(key)
