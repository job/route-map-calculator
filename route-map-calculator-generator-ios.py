#!/usr/bin/env pypy

import random

answers = {}

def add_or_not(x, y):
    global answers
    try:
        answers[x].append(y)
    except KeyError:
        answers[x] = []
        answers[x].append(y)

# loop through all possible answers whithin our constraints and store them

for x in xrange(1, 257):
    for y in xrange(1, 257):
        # + = 1
        if x + y < 65536:
            add_or_not(x + y, [1, x, y])
        # * = 2
        if x * y < 65536:
            add_or_not(x * y, [2, x, y])
        # - = 3
        if 0 < x - y < 65536:
            add_or_not(x - y, [3, x, y])
        # / = 4
        if 0 < x / y < 65536:
            add_or_not(x / y, [4, x, y])

a = answers.copy()

add_cache = []
multiply_cache = []
entries = 1
ordered = {}

keys = a.keys()
random.shuffle(keys)

for i in keys:
    print ""
    for b in a[i]:
        # add
        if b[0] == 1:
            if (b[1], b[2]) not in add_cache and (b[2], b[1]) not in add_cache:
                print("ip community-list standard %s_%s_%s permit 65000:%s 0:%s 0:%s" % \
                    (b[0], b[1], b[2], b[0], b[1], b[2]))
                add_cache.append((b[1], b[2]))
        # multiply
        elif b[0] == 2:
            if (b[1], b[2]) not in multiply_cache and (b[2], b[1]) not in multiply_cache:
                print("ip community-list standard %s_%s_%s permit 65000:%s 0:%s 0:%s" % \
                    (b[0], b[1], b[2], b[0], b[1], b[2]))
                multiply_cache.append((b[1], b[2]))
        # substract
        elif b[0] == 3:
            try:
                ordered[i] += 1
                seq = ordered[i]
            except KeyError:
                seq = 1
                ordered[i] = seq
            print("ip community-list expanded c%s permit %s ^65000:%s_0:%s_0:%s$" % \
                          (i, seq, b[0], b[1], b[2]))
        elif b[0] == 4:
            try:
                ordered[i] += 1
                seq = ordered[i]
            except KeyError:
                seq = 1
                ordered[i] = seq
            print("ip community-list expanded c%s permit %s ^65000:%s_0:%s_0:%s$" % \
                          (i, seq, b[0], b[1], b[2]))

    print ""
    communities = []
    for b in a[i]:
        # add
        if b[0] == 1:
            if (b[2], b[1]) in add_cache and b[2] != b[1]:
                pass
            else:
                communities.append("%s_%s_%s" % (b[0], b[1], b[2]))
        # multiply
        elif b[0] == 2:
            if (b[2], b[1]) in multiply_cache and b[2] != b[1]:
                pass
            else:
                communities.append("%s_%s_%s" % (b[0], b[1], b[2]))
        # substract
        elif b[0] == 3:
            communities.append("c%s_%s_%s" % (b[0], b[1], b[2]))
        elif b[0] == 4:
            communities.append("c%s_%s_%s" % (b[0], b[1], b[2]))

    for c in xrange(0, len(communities), 5):
        print "route-map calculator permit %s" % entries
        entries += 1
        print " match community ",
        print ' '.join(str(j) for j in communities[c:c+5])
        print " set community 0:%s" % i

