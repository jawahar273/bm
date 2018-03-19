def flatter_list(items):
    '''
     fastest way to flatten list of elements
     Eg: [(1, 2), (2, 45)] => [1, 2, 2, 45]
    '''
    return [item for sublist in items for item in sublist]


def to_hexdigit(name):
    '''
    Get the name and conver to md5 string.

    @params name get the name.
    '''
    from hashlib import md5
    return md5(name.encode()).hexdigest()


def to_hrs(mins=0, secs=0, time_format=False) -> str:
    '''
    Convert the given minutes or seconds into hours.

    @params mins time in minus.
    @params secs time in secs.
    @params time_format is to return the time format.
    '''
    assert not (mins > 0 and secs > 0), ('Both the mins and secs as arguments'
                                         'are not allowed')
    if secs > 0:
        mins, secs = divmod(secs, 60)
    hrs, mins = divmod(mins, 60)
    if time_format:
        return '%d:%02d:%02d' % (hrs, mins, secs)
    return '%d' % (hrs)
