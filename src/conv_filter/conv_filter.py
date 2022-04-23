from conv_filter import parser, junos
from conv_filter.vds import Vds_Rule


def run():
    args = parser.run()
    firewall = junos.Config(path=args.src)
    vds_filter = Vds_Rule(firewall)
    print(firewall)
