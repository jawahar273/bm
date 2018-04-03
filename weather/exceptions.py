from django.core.exceptions import ObjectDoesNotExist


class LatLonDoesNotExit(ObjectDoesNotExist):
    '''This class is child class of
    :class: `core.exceptions.ObjectDoesNotExist`
    set to raise if latitute and lontitute not found
    in database.
    '''

    def __str__(self):
        return 'latitute and lontitute of the given location'\
               ' is not present in the database'


class DateDoesNotExit(ObjectDoesNotExist):
    '''This class is child class of
    :class: `core.exceptions.ObjectDoesNotExist`
    set to raise if date of specific locaiont(geo points).
    '''
    def __str__(self):
        return 'date of the given location is not present'
