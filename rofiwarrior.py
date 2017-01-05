#!/bin/env python

import sys

from rofi import Rofi
from taskw import TaskWarrior


class RofiWarrior:
    def __init__(self):
        self.rofi = Rofi()
        self.taskw = TaskWarrior()

        self.keybinds = {
                'exit_hotkeys': ('Alt+F4','Control+q'),
                "key1": ('Alt+t','list todo'),
                "key2": ('Alt+a','add todo'),
                }

        self.actions = [
                None, # Padding
                self.list_todo,
                self.add_todo,
                sys.exit
                ]


    def list_todo(self):
        tasks = self.taskw.load_tasks()
        ret_tasks = []
        for i in tasks["pending"]:
            ret_tasks.append(i["description"])

        self._callback(items=ret_tasks)

    def add_todo(self):
        task = self.rofi.text_entry("Add task: ")
        self.taskw._execute("add", *task.split())

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
