#!/usr/bin/env python3

'''Extract performance data from trace output.'''

import re
from argparse import ArgumentParser
from collections import defaultdict

QUERY = re.compile(r'^.*query:\s+(SELECT|INSERT|UPDATE|DELETE)\s+(.*)$')
TNAME = r'(?:(' + r'\"[A-Za-z0-9_]+\"|[A-Za-z0-9_]+' + r'))'
QUERIES = {
    'SELECT': re.compile(r'^.*FROM\s+' + TNAME),
    'INSERT': re.compile(r'INTO\s+' + TNAME),
    'UPDATE': re.compile(r'^' + TNAME),
    'DELETE': re.compile(r'^FROM\s+' + TNAME),
}

QUERY_FINDER = re.compile(r'(query:\s+.*?)\s*\n?\s+File')


class Perf(object):
    '''Performance data extracted from lines of trace output.'''

    def __init__(self):
        self._lines = 0
        self._query = defaultdict(lambda: defaultdict(int))

    def __str__(self):
        lines = ['lines: {}'.format(self._lines)]
        for query in self._query:
            lines += ['', '[{}]'.format(query), '']
            table = self._query[query]
            for tname in sorted(
                table, key=lambda k, t=table: t[k], reverse=True
            ):
                lines.append('{}: {}'.format(tname, table[tname]))
        return '\n'.join(lines)

    def line(self, line):
        '''Extract data from `line`.'''
        self._lines += 1
        matched = QUERY.match(line)
        if not matched:
            return
        query = matched.group(1)
        detail = matched.group(2)
        try:
            tname = QUERIES[query].match(detail).group(1)
        except KeyError:
            return
        except (AttributeError, IndexError):
            print(query, detail)
            raise
        else:
            tname = tname.strip('"')
        self._query[query][tname] += 1


def main():
    '''Extract performance data from trace output in logfile.'''
    aparser = ArgumentParser(description=main.__doc__)
    aparser.add_argument('logfile', help='filename or "-" to read from stdin')
    args = aparser.parse_args()
    perf = Perf()
    with open('/dev/stdin' if args.logfile == '-' else args.logfile) as fid:
        for query in QUERY_FINDER.finditer(fid.read()):
            perf.line(query.group(1))
    print(perf)

if __name__ == '__main__':
    main()