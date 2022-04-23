from __future__ import annotations
from typing import List, Dict, Optional, Any
import re


class Term(object):
    def __init__(self) -> None:
        self.action: List[str] = list()
        self.conditions: Dict[str, Any] = dict()

    def __repr__(self) -> str:
        return str({'action': self.action, 'condition': self.conditions})

    def set_conditions(self, condition: Dict[str, str]) -> None:
        if condition.get('name') and condition.get('value'):
            condition_name = condition['name']
            condition_value = condition['value']
            _condition: Optional[Dict[str, List[str]]
                                 ] = self.conditions.get(condition_name)
            if _condition is None:
                _condition: Dict[str, List[str]] = dict()
                _condition[condition_name] = list()
            _condition[condition_name].append(condition_value)
            self.conditions[condition_name] = _condition

    def append(self, action: Optional[str], condition: Optional[Dict[str, str]]):
        if action and action not in self.action:
            self.action.append(action)

        if condition:
            self.set_conditions(condition)


class Filter(object):
    def __init__(self, name) -> None:
        self.terms: Dict[str, Term] = dict()
        self.name: str = name

    def __repr__(self) -> str:
        return self.terms.__str__()

    def append(self, term_name: str, action: Optional[str], condition: Optional[Dict[str, str]]) -> None:
        term: Optional[Term] = self.terms.get(term_name)
        if term is None:
            term = Term()
        term.append(action, condition)
        self.terms[term_name] = term


class Firewall(object):

    def __init__(self) -> None:
        self.filters: Dict[str, Filter] = dict()

    def __str__(self) -> str:
        return self.filters.__str__()

    def append(self, filter_name: str, term_name: str, action: Optional[str], condition: Optional[Dict[str, str]]) -> None:
        filter: Optional[Filter] = self.filters.get(filter_name)
        if filter is None:
            filter = Filter(filter_name)
        filter.append(term_name, action, condition)
        self.filters[filter_name] = filter

    def append_from_firewall_line(self, firewall_line: str) -> None:

        filter_commonpart = re.search(
            r'^firewall .* filter (?P<filter_name>[-\w]+) term (?P<term_name>[-\w]+) (?P<rest>.*)', firewall_line)

        filter_name = filter_commonpart.group('filter_name')
        term_name = filter_commonpart.group('term_name')
        condition_cols: List[str] = filter_commonpart.group('rest').split()
        if condition_cols[0] == 'then':
            action = condition_cols[1]
            condition = None
        else:
            action = None
            condition = {'name': condition_cols[1], 'value': condition_cols[2]}
        self.append(filter_name, term_name, action, condition)

    @ classmethod
    def from_firewall_lines(cls, firewall_lines: List[str]) -> Firewall:
        firewall = Firewall()
        for firewall_line in firewall_lines:
            firewall.append_from_firewall_line(firewall_line)
        return firewall


class Config(object):
    def __init__(self, path) -> None:
        self.path = path
        self.config_lines: List[str] = self.load(path)
        self.firewall = self.parse_firewall(self.config_lines)

    def __str__(self) -> str:
        return str(self.firewall)

    @ staticmethod
    def load(path) -> List[str]:
        with open(path) as f:
            config_lines: List[str] = f.read().splitlines()
        return config_lines

    @ staticmethod
    def parse_firewall(config_lines) -> Dict[str, Dict[str, List[str]]]:

        firewall_lines: List[str] = list(
            filter(lambda x: x.startswith('firewall'), config_lines))

        firewall: Firewall = Firewall.from_firewall_lines(firewall_lines)
        return firewall
