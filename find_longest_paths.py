'''
Given a list of segments (a segment is defined by 2 integers),
combine them to find the longest path.
Two segments are combinable if they do not overlap.
We assume that the list of segments is sorted by the "start" order.

Example:
Input:
a:[1,4]
 3:  ---
b:[2,7]
 5:   -----
c:[3,8]
 5:    -----
d:[5,6]
 1:      -
e:[6,8]
 2:       --

Output:
The best length is 6
a+d+e
 6:  --- ---

'''
class ListSegments(object):
    """ListSegments represents a list of segments."""
    def __init__(self, list_segments):
        self.list_segments = list_segments
        self.length = self.compute_length()

    def find_start(self):
        """Find the start of the list."""
        return self.list_segments[0].start

    def find_end(self):
        """Find the end of the list."""
        return self.list_segments[-1].end

    def compute_length(self):
        """Return the length of the cumulated segments."""
        length = 0
        for segment in self.list_segments:
            length += segment.length

        return length

    def find_names(self):
        """Return the list of segments names part of the list."""
        names = []
        for segment in self.list_segments:
            names += segment.name
        return names

    def add(self, segment):
        '''
        If the segment fits at the end, append.
        If the segment fits at the beginning, add it at the beginning
        '''
        if segment.start >= self.find_end():
            # print "[1]  path start: %d,
            #             path end: %d,
            #             segment start: %d,
            #             segment end: %d" % (self.find_start(),
            #                                 self.find_end(),
            #                                 segment.start,
            #                                 segment.end)
            return ListSegments(self.list_segments + [segment])

        elif segment.end <= self.find_start():
            # print "[2]  path start: %d,
            #             path end: %d,
            #             segment start: %d,
            #             segment end: %d" % (self.find_start(),
            #                                 self.find_end(),
            #                                 segment.start,
            #                                 segment.end)
            return ListSegments([segment] + self.list_segments)

        else:
            # print "[3]  path start: %d,
            #             path end: %d,
            #             segment start: %d,
            #             segment end: %d" % (self.find_start(),
            #                                 self.find_end(),
            #                                 segment.start,
            #                                 segment.end)
            return []

    def __str__(self):
        """Redefine the __str__ method."""
        string_to_display = ""
        cursor_position = 0
        for segment in self.list_segments:
            string_to_display += " " * (segment.start - cursor_position)
            string_to_display += "-" * (segment.end - segment.start)
            cursor_position = segment.end

        elements_names = "+".join(self.find_names())
        return "%s\n%2d" % (elements_names, self.length) + ": " + string_to_display

    def pretty_str(self):
        """Pretty print for the list."""
        string_to_display = ""
        for segment in self.list_segments:
            string_to_display += "\n"+segment.pretty_str()

        return string_to_display

class Segment(object):
    """Represents a segment."""
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end
        self.length = self.compute_length()

    def __str__(self):
        """Redefine the __str__ method."""
        return "%s, start: %d, end:%d, length:%d" % (self.name, self.start, self.end, self.length)

    def compute_length(self):
        """Return the length of the segment."""
        return self.end - self.start

    def pretty_str(self):
        """Pretty print of the segment."""
        string_to_display = " " * self.start
        string_to_display += "-" * (self.end - self.start)

        return "%s:[%d,%d]\n%2d" % (self.name,
                                    self.start,
                                    self.end,
                                    self.length) + ": " + string_to_display


def find_longest_path(input_segments):
    '''
    Loop over the segment in input.
    If it is the first one, create a ListSegments object with that segment.
    If it is not the first one, we loop over the constructed paths and see if we
    can add that segment to an already existing path.
    If we found a path that matches, we add the segment and we add a new path_to_add
    with that segment so that we can start searches based on that segment as well.
    '''
    list_paths = []
    for segment in input_segments.list_segments:

        if len(list_paths) == 0:
            list_paths = [ListSegments([segment])]

        else:

            list_to_add_back = [ListSegments([segment])]

            for current_path in list_paths:
                #print "[%d] Path: %s (%d)" % (index, current_path,len(list_paths))

                path_to_add = current_path.add(segment)

                if path_to_add != []:
                    #print "THERE %s" % path_to_add
                    list_to_add_back += [path_to_add]

            if len(list_to_add_back) > 0:
                #for x in list_to_add_back:
                    #print "HERE %s" % x
                list_paths += list_to_add_back

    return list_paths


INPUT_SEGMENTS = ListSegments([Segment('a', 0, 2),
                               Segment('b', 1, 5),
                               Segment('c', 3, 10),
                               Segment('d', 5, 12),
                               Segment('e', 7, 8),
                               Segment('f', 8, 15)])

# INPUT_SEGMENTS = ListSegments([Segment('a',0,4),
#                                Segment('b',1,5),
#                                Segment('c',3,10),
#                                Segment('d',5,12),
#                                Segment('e',7,8),
#                                Segment('f',8,15)])

# INPUT_SEGMENTS = ListSegments([Segment('a', 1, 4),
#                                Segment('b', 2, 7),
#                                Segment('c', 3, 8),
#                                Segment('d', 5, 6),
#                                Segment('e', 6, 8)])

# INPUT_SEGMENTS = ListSegments([Segment('a', 1, 4),
#                                Segment('b', 2, 5)])

# INPUT_SEGMENTS = ListSegments([Segment('a',0,4),
#                                Segment('b',1,5),
#                                Segment('c',3,10),
#                                Segment('d',3,12),
#                                Segment('e',7,8),
#                                Segment('f',8,15)])

print "Here is the input:"
print INPUT_SEGMENTS.pretty_str()

print "Let's find the longest path"
RESULT = find_longest_path(INPUT_SEGMENTS)

print "Here are the %d constructed paths" % len(RESULT)
MAXIMUM_LENGTH = 0
MAXIMUM_PATH = None
LIST_MAXIMUM_PATH = []
for res in RESULT:
    if res.length > MAXIMUM_LENGTH:
        MAXIMUM_LENGTH = res.length
        MAXIMUM_PATH = res
        LIST_MAXIMUM_PATH = [res]
    elif res.length == MAXIMUM_LENGTH:
        LIST_MAXIMUM_PATH += [res]
    #print "\n"
    print res

print "########################"
if len(LIST_MAXIMUM_PATH) > 0:
    for path in LIST_MAXIMUM_PATH:
        print "The best length is %d" % MAXIMUM_LENGTH
        print path
print "########################"
