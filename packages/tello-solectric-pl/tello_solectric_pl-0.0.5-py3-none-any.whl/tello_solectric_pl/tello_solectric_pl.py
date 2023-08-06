import logging
import sys
from djitellopy import Tello


class TelloMain(Tello):
    """
    Klasa z ogólnymi funkcjami, które mogą się przydać w przyszłości
    """

    def __init__(self, info_all=False):
        if not info_all:
            Tello.LOGGER.setLevel(logging.CRITICAL)
        super().__init__()

    def query_hardware(self) -> str:
        """

        :return: "RMTT" if using the Controller on top of the RMTT, or "TelloEDU", if using a Tello or RMTT without
        the controller.
        :rtype:
        """
        try:
            hardware = self.send_read_command("hardware?")
            if hardware in ("ok", "unknown command: hardware?"):
                hardware = "TelloEDU"
            else:
                print(f"Bład przy sprawdzeniu hardware: {hardware}")
        except Exception as exc:
            hardware = "TelloEDU"

        return hardware

    def get_speed(self) -> int:
        """Query speed setting (cm/s)
        This method is in the DroneBlocksTello class because the Tello class
        uses a different command that no longer seems supported.
        Returns:
            int: 1-100
        """
        speed_value = self.send_read_command("speed?")
        try:
            speed_value = int(float(speed_value))
            self.last_speed_value = speed_value
        except:
            speed_value = self.last_speed_value

        return speed_value

    def tello_connect(self, hardware_type, min_battery_level, wait_for_state) -> bool:
        connection_success = False
        hardware_ok = False
        hardware_probe = "xxxx"

        try:
            super().connect(wait_for_state=wait_for_state)
            connection_success = True
        except Exception as e:
            print(f"Błąd przy wywołaniu CONNECT: {e}")
            return False

        hardware_probe = self.query_hardware()
        if hardware_type == hardware_probe:
            hardware_ok = True
            print(f"Połączono z dronem typu {hardware_type}")
            battery_level = self.get_battery()
            print(f"Poziom baterii == ({battery_level} %)")
            if battery_level < min_battery_level:
                print(
                    f"Poziom baterii zbyt niski - wymagane minimum to {min_battery_level} %."
                )
                return False
        else:
            print(f"Otrzymano: {repr(hardware_probe)} -> nie pasuje do {hardware_type}")

        return connection_success and hardware_ok


class TelloEDU(TelloMain):
    """

    Klasa przeznaczona dla dronów Tello-EDU (czarny)
    W metodzie D.connect() sprawdza, czy to taki dron, czy poziom naładowania baterii jest wystarczający
    """

    def __init__(self, info_all=False):
        """

        :param info_all: Czy ysyłać wszystkie informacje na ekran, True lub False (default)
        """
        super().__init__(info_all=info_all)

    def connect(self, wait_for_state=True) -> bool:

        return super().tello_connect(
            hardware_type="TelloEDU",
            min_battery_level=25,
            wait_for_state=wait_for_state,
        )


class RyzenTT(TelloMain):
    """
    Klasa przeznaczona dla dronów Ryzen-TT (czerwony)
    W metodzie D.connect() sprawdza, czy to taki dron
    W przyszłości pojawią się definicje metod
    """

    hardware_type = "RyzenTT"
    min_battery_level = 25
    pass
