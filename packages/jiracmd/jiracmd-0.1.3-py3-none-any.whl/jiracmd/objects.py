import json
import yaml
from datetime import datetime
from dataclasses import dataclass
from dataclasses import asdict
from jiracmd.utils import yaml_multiline_string_pipe
from abc import ABC, abstractmethod


@dataclass
class JiraObject(ABC):
    @abstractmethod
    def to_short_dict(self):
        return

    def to_dict(self):
        return asdict(self)

    def to_json(self, obj={}):
        obj_dict = obj or asdict(self)
        return json.dumps(obj_dict, indent=2, ensure_ascii=False)

    def to_yaml(self, obj={}):
        yaml.add_representer(str, yaml_multiline_string_pipe)
        obj_dict = obj or asdict(self)
        return yaml.dump(obj_dict, allow_unicode=True)

    def datetime_field(self, date_string, return_string=False):
        date_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f%z')
        if return_string:
            return date_obj.strftime('%Y-%m-%d %H:%M')
        return date_obj

    def get_outputs(self, short=False):
        output_dict = self.to_dict()
        if short:
            output_dict = self.to_short_dict()

        return {
            "dict": output_dict,
            "json": self.to_json(output_dict),
            "yaml": self.to_yaml(output_dict)
        }


@dataclass
class Issue(JiraObject):
    id: str
    self: str
    expand: str
    key: str
    fields: dict
    summary: str = ""
    issue_type: str = ""
    updated: str = None

    def __post_init__(self):
        self.summary = self.fields['summary']
        self.issue_type = self.fields['issuetype']['name']
        self.updated = self.datetime_field(
                self.fields['updated'],
                return_string=True)
        worklog = self.fields.pop('worklog', None)

    def to_short_dict(self, remove_items=[]):
        table_dict = {
            "key": self.key,
            "type": self.issue_type,
            "assignee": self.fields['assignee']['displayName'],
            "updated": self.updated,
            "summary": self.summary,
            "description": self.fields['description']
        }
        filtered_dict = {
            k:v for (k,v) in table_dict.items()
            if k not in remove_items
        }
        return filtered_dict

@dataclass
class Worklog(JiraObject):
    id: str
    self: str
    author: dict
    updateAuthor: dict
    timeSpent: str 
    timeSpentSeconds: int
    issueId: str
    created: str
    updated: str
    started: str
    issue_key: str = ""

    def __repr__(self):
        date_started = self.datetime_field(self.started, return_string=True)
        return f"Worklog(id={self.id}, timeSpent={self.timeSpent}, started={date_started})"

    def to_short_dict(self):
        table_dict = {
            "id": self.id,
            "author": self.author['displayName'],
            "issueKey": self.issue_key,
            "started": self.datetime_field(
                self.started,
                return_string=True
            ),
            "timeSpent": self.timeSpent
        }
        return table_dict

