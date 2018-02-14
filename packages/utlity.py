

def flatter_list(items):
    '''
     fastest way to flatten list of elements
     Eg: [(1, 2), (2, 45)] => [1, 2, 2, 45]
    '''
    return [item for sublist in items for item in sublist]

