import time

class Ykush(object):
    """Intended to be included as a subclass of the board that needs it

    Properties provided by base class:
        host: Lab host
        ykush_serial: Serial number of YKUSH device
        ykush_port: Port number on that device
    """
    def ykush_set_power(self, value):
        self.host.exec0('ykushcmd', '-s', self.ykush_serial,
                        '-u' if value else '-d', self.ykush_port)

    def ykush_on(self):
        self.ykush_set_power(True)

    def ykush_off(self):
        self.ykush_set_power(False)

    def ykush_is_on(self):
        out = self.host.exec0('ykushcmd', '-s', self.ykush_serial,
                              '-g', self.ykush_port)
        return 'ON' in out

    def ykush_reset(self):
        if self.ykush_is_on():
            self.ykush_off()
            time.sleep(1)
        self.ykush_on()

    def ykush_delay(self):
        time.sleep(.25)
