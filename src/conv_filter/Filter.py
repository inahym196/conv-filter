from typing import List, Dict
import pprint


class JunosFilter(object):
    def __init__(self, path) -> None:
        self.path = path
        self.config_lines: List[str] = self.load(path)
        self.format(self.config_lines)

    @staticmethod
    def load(path):
        with open(path) as f:
            config_lines: List[str] = f.read().splitlines()
        return config_lines

    def format(self, config_lines):

        def split(filter_line: str) -> Dict[str, str]:
            cols = filter_line.split()
            cols_map = {}
            if cols[3] != 'filter' or cols[5] != 'term':
                raise SyntaxError()
            cols_map['filtername'] = cols[4]
            cols_map['termname'] = cols[6]
            if cols[7] == 'from':
                cols_map['condition_statement'] = cols[8]
                cols_map['condition_value'] = cols[9]
            elif cols[7] == 'then':
                cols_map['action'] = cols[8]
            return cols_map

        filter_lines: List[str] = list(
            filter(lambda x: x.startswith('firewall'), config_lines))

        condition = List[str]
        term = Dict[str, condition]
        filterset: Dict[str, term] = {}
        for filter_line in filter_lines:
            try:
                filter_col = split(filter_line)
            except Exception:
                continue

            filtername = filter_col['filtername']
            termname = filter_col['termname']
            filterset.setdefault(filtername, {})
            filterset[filtername].setdefault(termname, {})

            if filter_col.get('action'):
                action = filter_col['action']
                filterset[filtername][termname].setdefault('action', [])
                filterset[filtername][termname]['action'].append(action)
            else:
                condition_statement = filter_col['condition_statement']
                condition_value = filter_col['condition_value']
                filterset[filtername][termname].setdefault(
                    condition_statement, [])
                filterset[filtername][termname][condition_statement].append(
                    condition_value)
        pprint.pprint(filterset)
