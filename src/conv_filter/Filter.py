from typing import List, Dict, TypedDict
import re


class Term(TypedDict):
    name: str
    condition: Dict[str, str]
    action: str


class JunosFilter(object):
    def __init__(self, path) -> None:
        self.path = path
        self.config_lines: List[str] = self.load(path)
        self.filterset = self.format(self.config_lines)

    @staticmethod
    def load(path) -> List[str]:
        with open(path) as f:
            config_lines: List[str] = f.read().splitlines()
        return config_lines

    @staticmethod
    def format(config_lines) -> Dict[str, Dict[str, List[str]]]:

        filter_lines: List[str] = list(
            filter(lambda x: x.startswith('firewall'), config_lines))

        condition = List[str]
        term = Dict[str, condition]
        filterset: Dict[str, term] = {}
        for filter_line in filter_lines:

            filter_commonpart = re.search(
                r'^firewall .* filter (?P<filtername>[-\w]+) term (?P<termname>[-\w]+) (?P<rest>.*)', filter_line)
            filtername = filter_commonpart.group('filtername')
            termname = filter_commonpart.group('termname')
            condition_cols = filter_commonpart.group('rest').split()

            filterset.setdefault(filtername, {})
            filterset[filtername].setdefault(termname, {})

            if condition_cols[0] == 'then':
                action = condition_cols[1]
                filterset[filtername][termname].setdefault('action', [])
                filterset[filtername][termname]['action'].append(action)
            else:
                condition_name = condition_cols[1]
                condition_value = condition_cols[2]
                filterset[filtername][termname].setdefault(condition_name, [])
                filterset[filtername][termname][condition_name].append(
                    condition_value)
        return filterset

    def to_vDS_filter(self) -> List[str]:
        filterset: Dict[str, Dict[str, List[str]]] = self.filterset
        for term in filterset.values():
            if 'action' in term and term['action'] == 'accept':
                if term['action'] == 'accept':
                    pass
                else:
                    pass

            if 'destination-' in term:
                pass
            if 'source-' in term:
                pass
