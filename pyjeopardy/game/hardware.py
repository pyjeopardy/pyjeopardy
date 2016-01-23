class Hardware:
    KEYBOARD = 1

    def __init__(self, hwtype, name):
        self.name = name
        self.type = hwtype

        self.all_keys = {}

    def get_key_for_name(self, keyname):
        for key, name in self.all_keys.items():
            if name == keyname:
                return key
        return None

class Keyboard(Hardware):
    def __init__(self):
        super(Keyboard, self).__init__(Hardware.KEYBOARD, "Keyboard")

        for key in range(65, 90):
            self.all_keys[key] = chr(key)
