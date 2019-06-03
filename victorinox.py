#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import icalendar, re, requests

headers = requests.utils.default_headers()
headers.update(
    {
        'Connection': 'close',
        'User-Agent': 'Victorinox/0.2 (https://github.com/jprenken/victorinox)'
    }
)

def application(environ, start_response):
    if environ['REQUEST_URI'] is '/':
        status = '200'
        response_headers = [('Content-Type', 'text/plain')]
        start_response(status, response_headers)
        return [':)\n']
    try:
        request = requests.get('https://portal.victorops.com%s' % environ['REQUEST_URI'], headers=headers, timeout=5)

        status = str(request.status_code)

        cal = icalendar.Calendar.from_ical(request.content.decode('utf-8'))
        everyone = re.compile(r' \- everyone:everyone$')
        cal.subcomponents[:] = [comp for comp in cal.subcomponents if not (comp.name is 'VEVENT' and everyone.search(comp['SUMMARY']))]

        output = cal.to_ical().decode('utf-8')

        response_headers = [('Content-Type', request.headers['Content-Type'])]

        start_response(status, response_headers)

        return [output.encode('utf8')]
    except:
        status = '500'
        response_headers = [('Content-Type', 'text/plain')]
        start_response(status, response_headers)
        return ['Failed']
