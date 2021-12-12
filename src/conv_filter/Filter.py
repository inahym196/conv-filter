from typing import List, Dict, Optional
import re


class Term(object):
    def __init__(self, condition: Optional[Dict[str, str]], action: str = 'permit') -> None:
        self.action: str = action
        self.condition: Dict[str, List[str]] = {}
        if condition:
            condition_name = condition.get('name')
            condition_value = condition.get('value')
            self.condition[condition_name] = [condition_value]

    # def __repr__(self) -> str:
        # return f'Term(condition={self.condition},action="{self.action}")'

    def __str__(self) -> str:
        return f'action: '

    def merge(self, action: Optional[str], condition: Optional[Dict[str, str]]):
        if action:
            self.action = action

        if condition:
            condition_name = condition.get('name')
            condition_value = condition.get('value')

            if self.condition.get(condition_name):
                if condition['value'] not in self.condition[condition_name]:
                    self.condition[condition_name].append(condition_value)
            else:
                self.condition[condition_name] = [condition_value]


class Filterset(object):
    def __init__(self) -> None:
        self.filterset: Dict[str, Dict[str, Term]] = {}

    def __repr__(self) -> str:
        return str(self.filterset)

    @ classmethod
    def from_firewall_lines(cls, firewall_lines: List[str]) -> 'Filterset':
        filterset = Filterset()
        for firewall_line in firewall_lines:
            filterset.append_from_firewall_line(firewall_line)
        return filterset

    def append(self, filtername: str, termname: str, action: Optional[str], condition: Optional[Dict[str, str]]):
        terms = self.filterset.get(filtername, {})
        term = terms.get(termname, Term(action=action, condition=condition))
        term.merge(action=action, condition=condition)
        self.filterset.setdefault(filtername, terms)
        self.filterset[filtername][termname] = term

    def append_from_firewall_line(self, firewall_line: str):

        filter_commonpart = re.search(
            r'^firewall .* filter (?P<filtername>[-\w]+) term (?P<termname>[-\w]+) (?P<rest>.*)', firewall_line)

        filtername = filter_commonpart.group('filtername')
        termname = filter_commonpart.group('termname')
        condition_cols: List[str] = filter_commonpart.group('rest').split()
        if condition_cols[0] == 'then':
            action = condition_cols[1]
            condition = None
        else:
            action = None
            condition = {'name': condition_cols[1], 'value': condition_cols[2]}
        self.append(filtername, termname, action, condition)


class JunosFilter(object):
    def __init__(self, path) -> None:
        self.path = path
        self.config_lines: List[str] = self.load(path)
        self.filterset = self.format(self.config_lines)

    @ staticmethod
    def load(path) -> List[str]:
        with open(path) as f:
            config_lines: List[str] = f.read().splitlines()
        return config_lines

    @ staticmethod
    def format(config_lines) -> Dict[str, Dict[str, List[str]]]:

        firewall_lines: List[str] = list(
            filter(lambda x: x.startswith('firewall'), config_lines))

        filterset = Filterset.from_firewall_lines(firewall_lines)
        print(filterset.__str__())
        return filterset

    # def to_vDS_filter(self) -> List[str]:
        # filterset: Dict[str, Dict[str, List[str]]] = self.filterset
        # for term in filterset.values():
        # if 'action' in term and term['action'] == 'accept':
        # if term['action'] == 'accept':
        # pass
        # else:
        # pass

        # if 'destination-' in term:
        # pass
        # if 'source-' in term:
        # pass
