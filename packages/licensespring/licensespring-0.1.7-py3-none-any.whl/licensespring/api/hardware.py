import uuid


class HardwareIdProvider:
    def get_id(self):
        return uuid.getnode()
