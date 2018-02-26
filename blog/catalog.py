import re
from django.template.defaultfilters import striptags

def catalog(string):
    pattern = re.compile(r'<h\d.*</h\d>')
    match = pattern.findall(string)
    html = ''
    for i in range(len(match)):
        if match[i].startswith('<h2'):
            if i == 0:
                html += '<li><a href="#{}">{}</a><ul>'.format(striptags(match[i]), striptags(match[i]))
            elif i == len(match) - 1:
                html += '</ul></li><li><a href="#{}">{}</a></li>'.format(striptags(match[i]), striptags(match[i]))
            else:
                html += '</ul></li><li><a href="#{}">{}</a><ul>'.format(striptags(match[i]), striptags(match[i]))
        if match[i].startswith('<h3'):
            html += '<li><a href="#{}">{}</a></li>'.format(striptags(match[i]), striptags(match[i]))
            if i == len(match) - 1:
                html += '</ul>'
    return html
