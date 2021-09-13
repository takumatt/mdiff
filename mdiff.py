#!/usr/bin/env python
#coding: utf-8

import lldb
import difflib

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("command script add -f mdiff.mdiff mdiff")

def mdiff(debugger, command, result, internal_dict):

    commands = command.split()

    res1 = exec_expression_o(debugger, commands[0])
    res2 = exec_expression_o(debugger, commands[1])

    if res1.GetError():
        result.SetError(res1.GetError())
        return
        
    if res2.GetError():
        result.SetError(res2.GetError())
        return

    contents1 = res1.GetOutput()
    contents2 = res2.GetOutput()

    diff = difflib.unified_diff(contents1.split('\n'), contents2.split('\n'))
    contents = '\n'.join(diff)

    result.AppendMessage(contents)

def exec_expression_o(debugger, command):

    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()

    # interpreter.HandleCommand('expression -lobjc -O -- ' + script, res)
    interpreter.HandleCommand('po ' + command, res)

    return res
