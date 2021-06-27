class Ghostbot:
    name = ""
    linked_bot = None
    address = None

    def __init__(self, address, name, linked_bot):
        self.address = address
        self.name = name
        self.linked_bot = linked_bot
        print(f"{name}, {address}")
