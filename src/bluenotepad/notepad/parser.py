# -*- coding: utf-8 -*-
'''
Created on 11-08-2013

@author: Krzysztof Langner
'''
import re

def parseReportModel(text):
    ''' Return dictionary with variables as keys and event list as values '''
    variables = {}
    for line in text.splitlines():
        cleaned_line = line.strip()
        if len(cleaned_line) > 0 and cleaned_line[0] != '#':
            tokens = cleaned_line.split('=')
            if len(tokens) == 2:
                name = tokens[0].strip()
                m = re.search('\{([^\{]+)\}', tokens[1])
                if m:
                    value = m.group(1)
                    variables[name] = value.split(',')
    return variables
    
    
if __name__ == '__main__':
    text = '''
        # All waste events
        waste = {Preferences, Export page, Page down, Start, Bring to front}
        # Single high frequency events
        save = {Save}
        show_preview = {Show preview}
        module_removed = {Module removed}
        module_repositioned = {Module repositioned}
        change_page_height = {Change page height}
        remove_module = {Remove module}
    '''
    variables = parseReportModel(text)
    for name,events in variables.iteritems():
        print('%s: %s' % (name, events))