import tbot
from tbot.machine import board, channel, connector, linux
from tbot.tc import git, shell, uboot
from flash import Flash
from sdwire import Sdwire
from ykush import Ykush

class Rpi_3UBootBuilder(uboot.UBootBuilder):
    name = "rpi_3"
    defconfig = "rpi_3_32b_defconfig"
    toolchain = "armv7-a"

class Rpi_3(
    connector.ConsoleConnector,
    board.PowerControl,
    board.Board,
    Flash,
    Sdwire,
    Ykush,
):
    name = "Raspberry Pi 3b"
    console_uart = "/dev/ttyusb_port1"
    mount_point = "rpi3_b_boot"
    mount_uuid = "B529-9710"
    sdwire_serial = "sdwire-18"
    ykush_port = "1"
    ykush_serial = "YK17698"

    ether_mac = "b8:27:eb:b4:f9:f2"

    def poweron(self) -> None:
        """Procedure to turn power on."""
        self.sdwire_dut()
        self.ykush_reset()

    def poweroff(self) -> None:
        """Procedure to turn power off."""
        self.ykush_off()
        self.sdwire_ts()

    def connect(self, mach) -> channel.Channel:
        """Connect to the board's serial interface."""
        return mach.open_channel("picocom", "-q", "-b", "115200",
                                 self.console_uart)

    def flash(self, repo: git.GitRepository) -> None:
        self.ykush_off()
        self.sdwire_ts()
        self.flash_rpi(repo)
        self.sdwire_dut()


class Rpi_3UBoot(
    board.Connector,
    board.UBootAutobootIntercept,
    board.UBootShell,
):
    prompt = "=> "
    build = Rpi_3UBootBuilder()


class Rpi_3Linux(
    board.Connector,
    board.LinuxBootLogin,
    linux.Bash,
):
    username = "pi"
    password = "raspberry"


BOARD = Rpi_3
UBOOT = Rpi_3UBoot
LINUX = Rpi_3Linux
