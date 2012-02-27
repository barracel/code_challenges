#!/usr/bin/python
from PIL import Image
import os
import sys

'''
Instagram Engineering Challenge: The Unshredder
    http://instagram-engineering.tumblr.com/post/12651721845/instagram-engineering-challenge-the-unshredder

@author: Oscar Fernandez Barracel
'''

def sum_shred_edges(shred_width, sample_height, width, height, data):
    '''Calculates averages of sample_height for the left and right edges of
    each shred'''
    sum_edges = [ [[[0,0,0] for _ in xrange(0, height/sample_height + 1)],
                   [[0,0,0] for _ in xrange(0, height/sample_height + 1)]]
                for x in xrange(0, width/shred_width)]
    for y in xrange(0, height):
        yoffset = y * width
        shred_y = y / sample_height
        for shred_x, x in enumerate(xrange(0, width, shred_width)):
            left = x + yoffset
            rigth = left + shred_width - 1
            lpixel, rpixel = data[left], data[rigth]
            sum_edges[shred_x][0][shred_y][0] += lpixel[0]
            sum_edges[shred_x][0][shred_y][1] += lpixel[1]
            sum_edges[shred_x][0][shred_y][2] += lpixel[2]
            sum_edges[shred_x][1][shred_y][0] += rpixel[0]
            sum_edges[shred_x][1][shred_y][1] += rpixel[1]
            sum_edges[shred_x][1][shred_y][2] += rpixel[2]
    return list(enumerate(sum_edges))

def is_better(score1, score2):
    '''Returns True is score1 is better than score2'''
    better1 = 0
    for y in xrange(0, len(score1)):
        # Comparing each color by separated got better results than the average
        sample_score = (int(score1[y][0] < score2[y][0]) +
                        int(score1[y][1] < score2[y][1]) +
                        int(score1[y][2] < score2[y][2]))
        better1 += int(sample_score > 1)
    return better1 > int(len(score1) / 2)


def find_best_neighbour(edge, shreds, key):
    ''' Finds the best neighbour by searching the one with the less color
    differences among samples.
    key=0 to compare left edges
    key=1 to compare right edges
    '''
    assert key in (0, 1)
    best_score = None
    best_shred = None
    for shred in shreds:
        edge2 = shred[1][key]
        score = []
        for y in xrange(0, len(edge2)):
            score.append((abs(edge[y][0] - edge2[y][0]),
                          abs(edge[y][1] - edge2[y][1]),
                          abs(edge[y][2] - edge2[y][2])))
        if not best_score or is_better(score, best_score):
            best_score = score
            best_shred = shred
    return best_score, best_shred

def main(imgfilein, imgfileout, sample_height):
    img = Image.open(imgfilein)
    img.convert("RGBA")
    data = img.getdata()

    best_score = None
    best_shred_width = None
    best_solution = None
    valid_sherd_widths = [n for n in xrange(4, img.size[0])
                          if img.size[0] % n == 0]
    for shred_width in valid_sherd_widths:
        shreds = sum_shred_edges(shred_width, sample_height, img.size[0],
                                 img.size[1], data)
        solution = [shreds.pop()]
        score = [(0,0,0)]
        while shreds:
            eleft = solution[0][1][0]
            eright = solution[len(solution) - 1][1][1]
            lscore, lshred = find_best_neighbour(eleft, shreds, 1)
            rscore, rshred = find_best_neighbour(eright, shreds, 0)

            # Searching best of left/right match ensures we don't misplace the
            # leftmost/rightmost shred
            if is_better(lscore, rscore):
                solution.insert(0,lshred)
                shreds.remove(lshred)
                score += lscore
            else:
                solution.append(rshred)
                shreds.remove(rshred)
                score += rscore

        if not best_score or is_better(score, best_score):
            best_score = score
            best_shred_width = shred_width
            best_solution = solution

    print "Best shred width detected: %s" % best_shred_width

    unshredded = Image.new("RGBA", img.size)
    x = 0
    for shred in best_solution:
        x1, y1 = best_shred_width * shred[0], 0
        x2, y2 = x1 + best_shred_width, img.size[1]
        source_region = img.crop((x1, y1, x2, y2))
        destination_point = (x, 0)
        unshredded.paste(source_region, destination_point)
        x += best_shred_width

    # Output the new image
    unshredded.save(imgfileout, "JPEG")


def print_usage(exit_code):
    print 'Usage: %s IMG_FILE [sample_height]' % os.path.basename(__file__)
    sys.exit(exit_code)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print_usage(1)

    filein = sys.argv[1]
    fileout = "unshredded.jpg"

    try:
        sample_height = int(sys.argv[2])
    except IndexError:
        sample_height = 16
    except ValueError, e:
        print e
        print_usage(1)

    main(filein, fileout, sample_height)
    print "File saved: %s" % fileout
