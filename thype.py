import math as m

def copysign(x, y):
	if y > 0:
		return abs(x)
	elif y < 0:
		return -abs(x)
	else:
		return 0

# corpus
# The corpus will just be a string.
# We will ignore shifted letters by unshifting them.

corpusname = "e10k"

with open(f"{corpusname}.txt", 'r') as corpusfile:
	corpus = corpusfile.read()

corpus = corpus.lower()

# layout
# The layout will be defined as a dict type with:
# Left -> Keys that the left hand will press
# Right -> Keys that the right hand will prss
# Home position of left thumb and right thumb will be assumed to be (0, 0)
#
# Alternating spaces is built in, but if only one side of the board has space then only that one will be used.
# 
# The way to define swipe keys is by using an array of indices, with negative meaning up and left, positive meaning right and down.
# The analyser will interpret [(0, 0), (1, 0)] as having to swipe from home position to the right by 1 tile to access the letter.
layout = {
	'name' : 'Hyper',
    'left' : {
        'e'  : [(0.5,  0)],
        ','  : [(0.5,  0), (0.5,  -1)],
        '.'  : [(0.5,  0), (0.5,  1)],
        '?'  : [(0.5,  0), (-0.5, 0)],

        'o'  : [(-0.5, 0)],
        'k'  : [(-0.5, 0), (0.5, 0)],

        'i'  : [(0.5,  -1)],
        ';'  : [(0.5,  -1), (-0.5, -1)],
        '\'' : [(0.5,  -1), (0.5,  0)],

        'g'  : [(-0.5, -1)],
        '"'  : [(-0.5, -1), (0.5,  -1)],
        'z'  : [(-0.5, -1), (-0.5, 0)],

        'a'  : [(0.5,  1)],
        'j'  : [(0.5,  1), (-0.5, 1)],
        '!'  : [(0.5,  1), (0.5,  0)],

        'u'  : [(-0.5, 1)],
        'x'  : [(-0.5, 1), (-0.5, 0)],

        ' '  : [(-1.5, 0)]
    },
    'right' : {
        'n' : [(0.5,  1)],
        'b' : [(0.5,  1), (-0.5, 1)],
        'd' : [(0.5,  1), (0.5,  0)],

        'l' : [(-0.5, 1)],
        'y' : [(-0.5, 1), (-0.5, 0)],
        '@' : [(-0.5, 1), (0.5,  1)],

        't' : [(0.5,  0)],
        'm' : [(0.5,  0), (0.5,  1)],
        'p' : [(0.5,  0), (-0.5, 0)],
        'w' : [(0.5,  0), (0.5,  -1)],

        's' : [(-0.5, 0)],
        'c' : [(-0.5, 0), (0.5,  0)],
        '-' : [(-0.5, 0), (-0.5, 1)],
        'q' : [(-0.5, 0), (-0.5, -1)],

        'h' : [(0.5,  -1)],
        'v' : [(0.5,  -1), (0.5,  0)],
        'f' : [(0.5,  -1), (-0.5, -1)],

        'r' : [(-0.5, -1)],
        '/' : [(-0.5, -1), (-0.5, 0)],
        '#' : [(-0.5, -1), (0.5,  -1)],

        ' '  : [(-1.5, 0)]
    }
} # this layout is hyper


totalsquareddistance = 0
totaldistance = 0
totalbiasedlevdist = 0
alternation = 0
typedbigrams = 0
movements = 0

lthumbpos = (0, 0)
rthumbpos = (0, 0)
lastfinger = -1 # -1 -> None, 0 -> Left, 1 -> Right

lastchar = ''
bigrams = {}

for char in corpus:
	typedbigrams += 1
	movements += 1
	if lastfinger == 1:
		if (char in layout['left'].keys()):
			if lastfinger == 1:
				alternation += 1
			charstroke = layout['left'][char]
			lastfinger = 0
			chardist = 0
			movements += len(charstroke) - 1
			for pos in charstroke:
				squareddist = (pos[0] - lthumbpos[0]) ** 2 + (pos[1] - lthumbpos[1]) ** 2 
				totalbiasedlevdist += copysign(0.5, lthumbpos[0] - pos[0]) + copysign(0.5, lthumbpos[1] - pos[1])
				totalsquareddistance += squareddist
				s = m.sqrt(squareddist)
				totaldistance += s
				chardist += s
				lthumbpos = pos
			bigrams.update({lastchar + char : chardist})
			lastchar = char
			continue
		elif (char in layout['right'].keys()):
			lastfinger = 1
			charstroke = layout['right'][char]
			chardist = 0
			movements += len(charstroke) - 1
			for pos in charstroke:
				squareddist = (pos[0] - lthumbpos[0]) ** 2 + (pos[1] - lthumbpos[1]) ** 2 
				totalbiasedlevdist += copysign(0.5, lthumbpos[0] - pos[0]) + copysign(0.5, lthumbpos[1] - pos[1])
				totalsquareddistance += squareddist
				s = m.sqrt(squareddist)
				totaldistance += s
				chardist += s
				rthumbpos = pos
			bigrams.update({lastchar + char : chardist})
			lastchar = char
			continue
		else:
			lastfinger = -1
	else:
		if (char in layout['right'].keys()):
			if lastfinger == 0:
				alternation += 1
			lastfinger = 1
			charstroke = layout['right'][char]
			chardist = 0
			movements += len(charstroke) - 1
			for pos in charstroke:
				squareddist = (pos[0] - lthumbpos[0]) ** 2 + (pos[1] - lthumbpos[1]) ** 2 
				totalbiasedlevdist += copysign(0.5, lthumbpos[0] - pos[0]) + copysign(0.5, lthumbpos[1] - pos[1])
				totalsquareddistance += squareddist
				s = m.sqrt(squareddist)
				totaldistance += s
				chardist += s
				rthumbpos = pos
			bigrams.update({lastchar + char : chardist})
			lastchar = char
			continue
		elif (char in layout['left'].keys()):
			lastfinger = 0
			charstroke = layout['left'][char]
			chardist = 0
			movements += len(charstroke) - 1
			for pos in charstroke:
				squareddist = (pos[0] - lthumbpos[0]) ** 2 + (pos[1] - lthumbpos[1]) ** 2 
				totalbiasedlevdist += copysign(0.5, lthumbpos[0] - pos[0]) + copysign(0.5, lthumbpos[1] - pos[1])
				totalsquareddistance += squareddist
				s = m.sqrt(squareddist)
				totaldistance += s
				chardist += s
				lthumbpos = pos
			bigrams.update({lastchar + char : chardist})
			lastchar = char
			continue
		else:
			lastfinger = -1
	typedbigrams -= 1
	movements -= 1

typedbigrams -= 1
movements -= 1

avgdist = totaldistance / typedbigrams
stddev = m.sqrt(totalsquareddistance / typedbigrams - (totaldistance / typedbigrams) ** 2)

bigramlist = list(bigrams.items())
easybigrams = list(filter(lambda x: x[1] <= avgdist - 1 * stddev, bigramlist))
hardbigrams = list(filter(lambda x: x[1] >= avgdist + 1 * stddev, bigramlist))

print(f'''Layout: {layout['name']}
Corpus: {corpusname}

Taps: {typedbigrams} | Swipes: {movements - typedbigrams}
Ratio: {typedbigrams / (movements - typedbigrams):.3f} : 1

Total squared distance: {totalsquareddistance}
Total distance: {totaldistance:.3f}
Average distance (per bigram): {avgdist:.3f}
Standard deviation of distance (per bigram): {stddev:.3f}

Average 'Inness' of bigrams: {totalbiasedlevdist / typedbigrams * 100:.3f}%

Easy bigrams %: {len(easybigrams) / typedbigrams * 100:.3f}% of typed bigrams 
Hard bigrams %: {len(hardbigrams) / typedbigrams * 100:.3f}% of typed bigrams 

Alternations: {alternation} out of {typedbigrams} typed bigrams ({alternation / typedbigrams * 100:.3f}%)''')
