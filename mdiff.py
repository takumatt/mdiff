#!/usr/bin/env python
#coding: utf-8

import lldb
import difflib

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("command script add -f mdiff.mdiff mdiff")

def mdiff(debugger, command, result, internal_dict):

    # TODO: flag
    context_line_number = 0
    plain = False

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

    diff_lines = list(difflib.unified_diff(contents1.splitlines(True), contents2.splitlines(True), n=context_line_number))

    if not plain:
        diff_lines = replace_prefixes_with_emojis(diff_linesv)
    
    contents = ''.join(diff_lines)

    result.AppendMessage(contents)

def exec_expression_o(debugger, command):

    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()

    # interpreter.HandleCommand('expression -lobjc -O -- ' + script, res)
    interpreter.HandleCommand('po ' + command, res)

    return res

def replace_prefixes_with_emojis(lines):

    def replace_with_emoji(line):
        prefix = line[0]
        if prefix == '+':
            return '➕' + line[1:]
        elif prefix == '-':
            return '➖' + line[1:]
        else:
            return line
        
    return lines[0:2] + list(map(replace_with_emoji, lines[3:]))
