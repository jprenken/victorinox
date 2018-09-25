#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import icalendar, re, requests

def application(environ, start_response):
    try:
        request = requests.get('https://portal.victorops.com%s' % environ['REQUEST_URI'])

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
