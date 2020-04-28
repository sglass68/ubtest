import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from dli import Dli
from sdwire import Sdwire

class Xu3UBootBuilder(uboot.UBootBuilder):
    name = "xu3"
    defconfig = "odroid-xu3_defconfig"
    toolchain = "armv7-a"

class Xu3(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Dli,
    Sdwire,
):
    name = "xu3"
    desc = "Odroid XU-3"
    console_uart = "/dev/ttyusb_port10"
    dli_hostname = "192.168.4.19"
    dli_outlet = "3"
    dli_password = "1234"
    dli_user = "admin"
    sdwire_serial = "202001064002"

    ether_mac = "None"

    def poweron(self) -> None:
        """Procedure to turn power on."""
        self.sdwire_dut()
        self.dli_reset()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.dli_off()
        self.sdwire_ts()

    def connect(self, mach) -> channel.Channel:
        """Connect to the board's serial interface."""
        return mach.open_channel("picocom", "-q", "-b", "115200",
                                 self.console_uart)

    def flash(self, repo: git.GitRepository) -> None:
        self.dli_off()
        self.sdwire_ts()
        self.flash_samsung(repo)
        self.sdwire_dut()


class Xu3UBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = Xu3UBootBuilder()


class Xu3Linux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = ""
    password = ""


BOARD = Xu3
UBOOT = Xu3UBoot
LINUX = Xu3Linux
