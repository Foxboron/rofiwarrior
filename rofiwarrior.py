#!/bin/env python

import sys

import dateutil.parser

from rofi import Rofi
from taskw import TaskWarrior


class RofiWarrior:
    def __init__(self):
        self.rofi = Rofi()
        self.taskw = TaskWarrior()

        self.keybinds = {
                "key1": ('Alt+t','list todo'),
                "key2": ('Alt+a','add todo'),
                "key3": ('Alt+d','due dates'),
                }

        self.actions = [
                None, # Padding
                self.list_todo,
                self.add_todo,
                self.list_tasks_due,
                sys.exit
                ]


    def list_todo(self, tasks=None):
        if not tasks:
            tasks = self.taskw.load_tasks()["pending"]
        items = []
        for i in tasks:
            items.append(i["description"])
        l = self._callback(items)

    def add_todo(self):
        task = self.rofi.text_entry("Add task: ")
        if not task:
            self.list_todo()
        self.taskw._execute("add", *task.split())

    def list_tasks_due(self):
        tasks = self.taskw.load_tasks()
        date_items = {}
        items = []
        
        # Wow, such horrible
        for i in tasks["pending"]:
            if "due" in i.keys():
                date = dateutil.parser.parse(i["due"])
                date = str(date).split("+")[0]
                if date_items.get(date):
                    date_items[date].append(i)
                else:
                    date_items[date] = [i]

        items = sorted(date_items.keys())
        ret = self._callback(items)
        tasks = date_items[items[ret]]
        self.list_todo(tasks)

    def _callback(self, items=[], prompt=">> "):
        ret = self.rofi.select(prompt, items, **self.keybinds)
        f = self.actions[ret[1]]
        if f:
            f()
        else:
            return ret[0]
     
    def run(self):
        self.list_todo()


if __name__ == '__main__':
    rw = RofiWarrior()
    rw.run()
