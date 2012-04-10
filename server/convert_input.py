#### encoding: utf8

import csv
import json
import re

orig = list(csv.DictReader(file('input.csv')))

out = []

link = re.compile('(\[(.+des([0-9]+).htm)\])')

for x in orig:
    nnn = {}
    nnn['book'] = x['book'].decode('utf8')
    nnn['chapter'] = x['chapter'].decode('utf8')
    nnn['subchapter'] = x['title'].decode('utf8')
    nnn['subject'] = x['subject'].decode('utf8')
    nnn['recommendation'] = x['recommendation'].decode('utf8')
    nnn['responsible_authority'] = x['responsible_authority'].decode('utf8')
    nnn['result_metric'] = x['result_metric'].decode('utf8')
    nnn['budget'] = { 'description' : x.get('budget_cost').decode('utf8'),
                      'millions' : x.get('budget_cost_millions',0),
                      'year_span' : 0  }
    nnn['timeline'] = [ { 'due_date' : x.get('schedule','').decode('utf8'),
                          'links' : [],
                          'milestone_name' : x.get('execution_metric').decode('utf8') } ]
    if x['gov_current_status']:
        for s in x['gov_current_status'].decode('utf8').split(';'):
            date = None
            links = []
            if '8.1.12' in s:
                date = "8/1/2012"
            if '29.1.12' in s:
                data = "29/1/2012"
            if '18.12.12' in s:
                date = '18/12/2011'
            if '18.12.11' in s:
                date = '18/12/2011'
            if '30.10.2011' in s:
                date = '30/10/2011'
            if '5.12' in s:
                date = '5/12/2011'
            if '4.12.2011' in s:
                date = '4/12/2011'
            if '29.1.2012' in s:
                date = '29/1/2012'
            if '25.12.11' in s:
                date = '25/12/2011'
            if '18.12.2011' in s:
                date = '18/12/2011'
            m = link.search(s)
            if m != None:
                match, url, num = m.groups()
                links.append( { 'url' : url, 'description' : u'התקבל בהחלטת ממשלה מספר %s' % num} )
            if date:
                nnn['timeline'].append( { 'due_date' : date, 'links' : links, 'milestone_name' : s } )
            else:
                nnn['implementation_status_text'] = s       
    nnn['tags'] = [ t.strip() for t in x.get('tags').split(';') if t.strip() != '' ]
    nnn['implementation_status'] = {'80':'WORKAROUND','100':'FIXED' }.get(x['gov_current_status_code'],'NEW')

    out.append( {'gov' : nnn, 'slug': x['slug'] } )

print json.dumps(out,indent=4)
