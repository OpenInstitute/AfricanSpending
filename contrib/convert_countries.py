from __future__ import print_function
import os
import yaml, json
import unicodecsv
from pprint import pprint

COUNTRIES = ['za', 'dz', 'ao', 'bw', 'bf', 'bi',
             'cm', 'cf', 'td', 'cg', 'cd', 'dj', 'eg',
             'er', 'et', 'ga', 'gm', 'gh', 'gn', 'gw',
             'ci', 'ke', 'ly', 'ls', 'lr', 'mg', 'mw',
             'ml', 'ma', 'mz', 'na', 'ne', 'ng', 'sn',
             'sl', 'so', 'sd', 'sz', 'tz', 'tn', 'ug',
             'zm', 'zw', 'gq', 'ss', 'bj', 'cv', 'mr',
             'mu', 'rw', 'st', 'sc', 'eh', 'tg']

print(len(set(COUNTRIES)))

print([c.upper() for c in COUNTRIES])

my_path = os.path.dirname(__file__)

out_file = os.path.join(my_path, '../data/library/countries.yaml')

try:
    out = yaml.load(open(out_file, 'rb').read())
except Exception as e:
    print(e)
    out = {}

with open(os.path.join(my_path, 'countries.csv'), 'r') as fh:
    reader = unicodecsv.DictReader(fh)
    for row in reader:
        if row.get('linked_country'):
            continue
        key = row.get('iso2').lower()
        if key not in COUNTRIES:
            continue
        data = {
            'iso2': row.get('iso2'),
            'iso3': row.get('iso3'),
            'label_full': row.get('country'),
            'label': row.get('country')
        }
        od = out.get(key, {})
        for k, v in list(data.items()):
            if k not in od:
                od[k] = v
        out[key] = od

for cd in json.load(open(os.path.join(my_path, 'obs.json'), 'rb')):
    key = cd['code'].lower()
    if key not in out:
        continue
    #pprint(cd)
    out[key]['obi'] = cd.get('obi_scores')
    out[key]['ibp_library'] = cd.get('library')
    out[key]['obstracker_url'] = 'http://www.obstracker.org/country/%s' % cd.get('country')
    out[key]['obi_url'] = 'http://survey.internationalbudget.org/#profile/%s' % cd.get('code')


print(sorted([o.get('iso3') for o in list(out.values())]))

print('missing', set(COUNTRIES) - set(out.keys()))


with open(out_file, 'wb') as fd:
    fd.write(yaml.safe_dump(out, canonical=False,
                            default_flow_style=False,
                            allow_unicode=True,
                            indent=2))

