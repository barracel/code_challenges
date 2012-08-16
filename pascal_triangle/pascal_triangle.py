import sys

def element(num, x):
    if num == 0:
        return 1 if x == 0 else 0
    return element(num-1, x - 1) + element(num-1, x)

_cache = {}
def element_memoized(num, x):
    value = _cache.get((num, x), None)
    if value:
        return value

    if num == 0:
        value = 1 if x == 0 else 0
    else:
        value = element_memoized(num-1, x - 1) + element_memoized(num-1, x)

    _cache[(num, x)] = value
    return value

def pascal_recursive(num, element_func=element):
    for n in xrange(0, num + 1):
        for x in xrange(0, n + 1):
            print element_func(n, x),
        print '\n',

def pascal_iterative(num):
    # left & right 1 cell padding to avoid boundary checks
    padding = 2
    row = [0] * (num + 1 + padding)
    row[1] = 1
    for n in xrange(1, num + 2):
        prev = row[0]
        for x in xrange(1, n + 1):
            tmp = row[x]
            row[x] = prev + row[x]
            prev = tmp
            print row[x],
        print '\n',

if __name__ == '__main__':
    try:
        num = sys.argv[1]
    except IndexError:
        num = int(raw_input('Enter number:'))

    print "Recursive:"
    pascal_recursive(num, element_func=element)

    print "\nRecursive memoized:"
    pascal_recursive(num, element_func=element_memoized)

    print "\nIterative:"
    pascal_iterative(num)
