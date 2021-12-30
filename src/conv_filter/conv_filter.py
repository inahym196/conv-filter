from conv_filter import parser
from conv_filter.Filter import JunosFilter


def run():
    args = parser.run()
    filter = JunosFilter(path=args.src)
    print(filter)
