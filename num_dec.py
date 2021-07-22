import re
from decimal import *

#+UTILITY FUNCTIONS---------------------------------------------------

def parts_helper(s, ps, res):
    if len(s) > abs(ps):
        if ps < 0:
            res.append(s[ps:])
            return parts_helper(s[:ps], ps, res)
        else:
            res.append(s[:ps])
            return parts_helper(s[ps:],ps,res)
    else:
        res.append(s)
        if ps < 0:
            res.reverse()
        return res

def parts(s, ps):
    """Partitions the string <s> from right to left into strings of
    size <ps> and then returns a list of the partitions. If ps < 0 the
    partitioning is done from right to left instead."""
    return parts_helper(s, ps, list([]))

#+PRIVATE REGEX'S-----------------------------------------------------

#The basic strategy is to build up complex regex's from simpler ones

on = "1"
te = "10"
hu = "100"
th = "1000"
mi = "1000000"
bi = "1000000000"
tr = "1000000000000"

# Each regular expression may have a unique id and possibly an
# associated power of 10. For example, a regex n1_999_rx(3,1) could be
# used in a regexp whose id is 1 to match the first three digits of
# 123456, and n1_999_rx(0,1) could be used to match the last three
# digits. To introduce a new regex, just pick a unique id and then use
# the provided 'building blocks' the functions with names like
# 'n_*_rx' to build up the regex.

# The purpose of the commas is to preserve word boundaries. If word
# boundaries are ignored, a sequence of numbers may have more than one
# interpretation e.g. '4 10 5 10' could be taken to mean 4050 or
# 4510. With the commas '4 10, 5 10,' yields 4050 and '4 10, 5, 10,'
# yields 4510 with no ambiguity.

def n0_rx(i,j):
    """Returns a regex for the number 0. The variable 'i' indicates
    which power of 10 the regex is associated with and the variable
    'j' indicates the id of the parent regex."""
    return "(?:(?P<on_"+str(i)+"_0_"+str(j)+">0), ?)"

def n1_9_rx(i, j):
    """Returns a regex for a number 1-9. The variable 'i' indicates
    which power of 10 the regex is associated with and the variable
    'j' indicates the id of the parent regex."""
    return "(?:(?P<on_"+str(i)+"_0_"+str(j)+">[1-9]), ?)"

def n10_90_rx(i, j):
    """Returns a regex for a number 10-90. The variable 'i' indicates
    which power of 10 the regex is associated with and the variable
    'j' indicates the id of the parent regex."""
    return "(?:(?P<te_"+str(i)+"_1_"+str(j)+">[1-9]) "+te+", ?)"

def n100_900_rx(i, j):
    """Returns a regex for a number 100-900. The variable 'i'
    indicates which power of 10 the regex is associated with and the
    variable 'j' indicates the id of the parent regex."""
    return "(?:(?P<hu_"+str(i)+"_2_"+str(j)+">[1-9]), "+hu+", ?)"

def n10_99_rx(i, j):
    """Returns a regex for a number 10-99. The variable 'i'
    indicates which power of 10 the regex is associated with and the
    variable 'j' indicates the id of the parent regex."""
    return "("+n10_90_rx(i, j) + n1_9_rx(i, j) + "?)"

def n1_99_rx(i, j):
    """Returns a regex for a number 1-99. The variable 'i'
    indicates which power of 10 the regex is associated with and the
    variable 'j' indicates the id of the parent regex."""
    return "(?:" + n10_90_rx(i, j) + "?" + n1_9_rx(i, j) + "?)"

def n1_999_rx(i, j):
    """Returns a regex for a number 1-999. The variable 'i'
    indicates which power of 10 the regex is associated with and the
    variable 'j' indicates the id of the parent regex."""
    return "(?:" + n100_900_rx(i, j) + "?" + n1_99_rx(i, j) + "?)"

def test_regex_bounds(regex, _min, _max):
    """Used to test regex's as they are built up."""
    print "Testing: n"+str(_min)+"_"+str(_max)
    s99 = "9 10, 9,"
    s999 = "9, 100, " + s99
    s999_th = s999 + " " + th + ","
    s999_mi = s999 + " " + mi + ","
    s999_bi = s999 + " " + bi + ","
    s999_tr = s999 + " " + tr + ","
    bounds = {1:"1,", 2:"2,", 9:"9,", 10:"1 10,", 19:"1 10, 9,",
              20:"2 10,", 99:s99, 100:"1, 100,", 999:s999,
              1000:"1, "+th+",", 999000:s999_th, 10**6:"1, "+mi+",",
              999*10**6:s999_mi, 10**9:"1, "+bi+",", 999*10**9:s999_bi,
              10**12:"1, "+tr+",", 999*10**12:s999_tr}
    rc = re.compile("^("+regex+")$")
    for k,v in bounds.iteritems():
        if _min <= k and k <= _max:
            print k,": ",v
            assert(rc.match(v)!=None)

# These will be used to build up 'main_rx'

# TODO: move the 'test_regex_bounds' functions to a separate test.

n1_th_999_th = "(?:"+n1_999_rx(3*1, 1)+" "+th+", ?)"
# test_regex_bounds(n1_th_999_th, 1000, 999000)

n1_mi_999_mi = "(?:"+n1_999_rx(3*2, 1)+" "+mi+", ?)"
# test_regex_bounds(n1_mi_999_mi, 10**6, 999*10**6)

n1_bi_999_bi = "(?:"+n1_999_rx(3*3, 1)+" "+bi+", ?)"
# test_regex_bounds(n1_bi_999_bi, 10**9, 999*10**9)

n1_tr_999_tr = "(?:"+n1_999_rx(3*4, 1)+" "+tr+", ?)"
# test_regex_bounds(n1_tr_999_tr, 10**12, 999*10**12)

# Three higher level regex's

# Most numbers will match this regex.
main_rx = r"(?:" + n1_tr_999_tr + "?" + n1_bi_999_bi + "?" + n1_mi_999_mi + "?" + n1_th_999_th + "?" + n1_999_rx(0, 1) + "?(?<=\d,))"

# Ex: the match '4, 100, 2 10, 1, 1000, 1 100, 1 10 7,' yields 421,117
#     the match '1, 2, 3, 4, 5, 6, 7, 8, 9,' yields 123,456,789
#     the match '40,50,3' yields 4053

# Some 4-digit numbers will match this regex (g=4)
quads_rx = r"(?:(?:"+n10_99_rx(2, 2)+" 100,)(?: "+n1_99_rx(0, 2)+")?)"

# Ex: the match '90, 7, 100,' yields 9700, and
#     the match '40, 1, 100, 50' yields 4150

zero_rx = r"(?:"+n0_rx(0,3)+")"

# Top-level regex

# Order is important; the quads regex must be place before the main
# regex. Otherwise 90, 7, 100 would yield 97100 instead of 9700.

top_rx = "(?:" + quads_rx + "|" + main_rx + "|" + zero_rx + ")"

#DICTIONARIES---------------------------------------------------------

dec_to_numeral = {"0":"zero", "1":"one", "2":"two", "3":"three", "4":"four", "5":"five", "6":"six", "7":"seven", "8":"eight", "9":"nine", "10":"ten", "11":"eleven", "12":"twelve", "13":"thirteen", "14":"fourteen", "15":"fifteen", "16":"sixteen", "17":"seventeen", "18":"eighteen", "19":"nineteen", "20":"twenty", "30":"thirty", "40":"forty", "50":"fifty", "60":"sixty", "70":"seventy", "80":"eighty", "90":"ninety", hu:"hundred", th:"thousand", mi:"million", bi:"billion", tr:"trillion"}

numerals_desc = ['trillion', 'billion', 'million', 'thousand', 'hundred', 'ninety', 'eighty', 'seventy', 'sixty', 'fifty', 'forty', 'thirty', 'twenty', 'nineteen', 'eighteen', 'seventeen', 'sixteen', 'fifteen', 'fourteen', 'thirteen', 'twelve', 'eleven', 'ten', 'nine', 'eight', 'seven', 'six', 'five', 'four', 'three', 'two', 'one', 'zero', 'oh']

numeral_to_dec = {"oh":"0", "zero":"0", "one":"1", "two":"2", "three":"3", "four":"4", "five":"5", "six":"6", "seven":"7", "eight":"8", "nine":"9", "ten":"1 10", "eleven":"1 10, 1", "twelve":"1 10, 2", "thirteen":"1 10, 3", "fourteen":"1 10, 4", "fifteen":"1 10, 5", "sixteen":"1 10, 6", "seventeen":"1 10, 7", "eighteen":"1 10, 8", "nineteen":"1 10, 9", "twenty":"2 10", "thirty":"3 10", "forty":"4 10", "fifty":"5 10", "sixty":"6 10", "seventy":"7 10", "eighty":"8 10", "ninety":"9 10", "hundred":hu, "thousand":th, "million":mi, "billion":bi, "trillion":tr}

# Numeral to decimal conversion --------------------------------------

def match_to_dec(m):
    """Returns the match as a decimal."""
    total = 0
    cap = re.compile("^(?:on|te|hu)_([0-9])_([0-9])_([0-9])$")
    for k,v in m.groupdict().iteritems():
        if v:
            m = cap.match(k)
            np = int(m.group(1))
            dp = int(m.group(2))
            total += int(v)*pow(10, int(np)+dp)
    return str(total)

def cat_decs(s):
    """Concatenate any space-separated decimals in <s>."""
    return re.sub(r"(?P<dig>[0-9]) (?=[0-9])", lambda m: m.group("dig"), s)

def toDecimalHelper(m):
    """Returns a single decimal as a string for the matching sequence of numerals."""
    s = m.group(0)
    s = re.sub(r"ten ((?=nine|eight|seven|six|five|four|three|two|one))",r"ten;\1",s)
    for k in numerals_desc:
        s = re.sub(k, numeral_to_dec[k]+",",s)
    s = cat_decs(re.sub(top_rx, match_to_dec, s))
    s = re.sub(r"(\d);(\d)",r"\1\2",s)
    return s

# Decimal to numeral conversion---------------------------------------

def toNum0_999SF(s):
    if abs(int(s)) >= pow(10, 3):
        raise Exception("abs(s) is too large; max is 10^3-1")

    if int(s) < 0:
        raise Exception("s must be non-negative")

    l = []
    #strip off all leading zeros
    s2 = str(int(s))

    # the third digit has numerals 'one hundred', 'two hundred', ...,
    # or 'nine hundred'
    if len(s2) == 3 and s2[-3] != "0":
        l.append(dec_to_numeral[s2[-3]] + " hundred")

    if len(s2) >= 2 and s2[-2] != "0":
        if s2[-2] != "1":
            # the second digit has a numeral 'twenty',..., or 'ninety'
            l.append(dec_to_numeral[s2[-2] + "0"])
        else:
            # a single numeral represents the last two digits:
            # 'ten','eleven',..., or 'nineteen'
            l.append(dec_to_numeral[s2[-2:]])

    if s2[-1] != "0" and (len(s2)==1 or s2[-2] != "1"):
        # the last digit has a numeral 'one','two',..., or 'nine'
        l.append(dec_to_numeral[s2[-1]])

    return " ".join(l)

def toNumeralsSF(s):
    if abs(int(s)) >= pow(10, 15):
        raise Exception("abs(s) is too large; max is 10^15-1")

    if int(s) < 0:
        return "negative " + toNumeralsSF(s[1:])

    l=[]
    for i in range(0, len(s)):
        if s[i]=="0":
            l.append("zero")
        else:
            break

    ps=parts(s,-3)
    for i in range(0,len(ps)-1):
        if int(ps[i]) != 0:
            l.append(toNum0_999SF(ps[i]) + " " + dec_to_numeral[str(10**(3*(len(ps)-1-i)))])

    if int(ps[-1]) != 0:
        l.append(toNum0_999SF(ps[-1]))

    return " ".join(l)

def toNumeralsHelper(s, g):
    """Converts the string representation of an integer <s> to
    numerals with digit groups of size <g>. """
    # TODO: add type checking

    if g==0:
        g2=len(s)
    elif g=="-4*":
        g2=-4
    elif g=="4*":
        g2=4
    else:
        g2=g

    l2 = parts(s, g2)
    l3 = list([])

    if g=="-4*" or g=="4*":
        for p in l2:
            if len(p) < 4:
                l3.append(toNumeralsSF(p))
            else:
                l3.append(toNumeralsSF(p[:2]))
                if int(p[:2]) != 0:
                    l3.append("hundred")
                else:
                    l3.append(toNumeralsSF(p[2:]))
                    continue
                if int(p[2:]) != 0:
                    l3.append(toNumeralsSF(str(int(p[2:]))))

    else:
        for p in l2:
            l3.append(toNumeralsSF(p))

    return l3

def toNumerals(s, g):
    """Return the string that results from replacing all decimals in
    the string <s> with their corresponding numerals using chunks of
    at most <g> digits, where g=...,-3,-2,-1,0,1,2,3,... or g="-4*" or
    g="4*". A minus sign indicates that the direction of the chunking
    should be from right to left.  The default direction is from left
    to right.  If <g> is omitted or <g>=0, use all the decimal's
    digits.

    Examples:
    toNumerals("1858", "4*") = "eighteen hundred fifty eight"
    toNumerals("1858",    4) = "one thousand eight hundred fifty eight"
    toNumerals("1858",    3) = "one hundred eighty five eight"
    toNumerals("1858",    2) = "eighteen fifty eight"
    toNumerals("1858",    1) = "one eight five eight"
    toNumerals("1858",    0) = "one thousand eight hundred fifty eight"
    toNumerals("1858"      ) = "one thousand eight hundred fifty eight"
    toNumerals("1858",   -1) = "one eight five eight"
    toNumerals("1858",   -2) = "eighteen fifty eight"
    toNumerals("1858",   -3) = "one eight hundred fifty eight"
    toNumerals("1858",   -4) = "one thousand eight hundred fifty eight"
    toNumerals("1858","-4*") = "eighteen hundred fifty eight"
    """
    return re.sub("( |^)([0-9]+)( |$)", lambda m: m.group(1)+" ".join(toNumeralsHelper(m.group(2), g))+m.group(3), s)

#PUBLIC API-----------------------------------------------------------

def toDecimal(s):
    """Replaces any sequences of numerals in the string <s> with their
    corresponding decimals.

    Examples:
    toDecimal("one thousand eight hundred fifty eight") = "1858"
    toDecimal("eighteen hundred fifty eight") = "1858"
    toDecimal("eighteen fifty eight") = "1858"
    toDecimal("one eight five eight") = "1858"
    """
    numeral = "(?:" + "|".join(numerals_desc) + ")"
    numeral_seq = "(?: |^)("+numeral+"(?: " + numeral + ")*)(?: |$)"

    return re.sub(numeral_seq, toDecimalHelper, s)

#TESTING--------------------------------------------------------------

def test_str_eq(s1, s2):
    """Tests if the two strings match."""
    if s1!=s2:
        raise Exception ("Test failed for s1=\""+s1+"\""+"and s2=\""+s2+"\"")

def test_basic():
    print "Basic toDecimal test"
    test_str_eq(toDecimal("eighteen hundred fifty eight"), "1858") # 1800;58
    test_str_eq(toDecimal("one thousand eight hundred fifty eight"), "1858") #1858
    test_str_eq(toDecimal("one hundred eighty five eight"), "1858") #185;8
    test_str_eq(toDecimal("eighteen fifty eight"), "1858") #18;58
    test_str_eq(toDecimal("one eight five eight"), "1858") #1;8;5;8
    test_str_eq(toDecimal("one eight hundred fifty eight"), "1858") #1;858
    print "Passed"

    print "Basic toNumerals test"
    test_str_eq(toNumerals("1858", "4*"), "eighteen hundred fifty eight")
    test_str_eq(toNumerals("1858",    4), "one thousand eight hundred fifty eight")
    test_str_eq(toNumerals("1858",    3), "one hundred eighty five eight")
    test_str_eq(toNumerals("1858",    2), "eighteen fifty eight")
    test_str_eq(toNumerals("1858",    1), "one eight five eight")
    test_str_eq(toNumerals("1858",    0), "one thousand eight hundred fifty eight")
#   test_str_eq(toNumerals("1858"      ), "one thousand eight hundred fifty eight")
    test_str_eq(toNumerals("1858",   -1), "one eight five eight")
    test_str_eq(toNumerals("1858",   -2), "eighteen fifty eight")
    test_str_eq(toNumerals("1858",   -3), "one eight hundred fifty eight")
    test_str_eq(toNumerals("1858",   -4), "one thousand eight hundred fifty eight")
    test_str_eq(toNumerals("1858","-4*"), "eighteen hundred fifty eight")
    print "Passed"

def test_non_nums():
    print "Non-numeral test"
    s="The point is twofold: (1) tents without stakes may blow away, and (2) the sixers will not play the niners."
    test_str_eq(toDecimal(s), s)
    test_str_eq(toDecimal("I'll have thirteen eggs for breakfast, please."), "I'll have 13 eggs for breakfast, please.")
    print "Passed"

def test_non_dec():
    print "Non-dec test"
    s="A-1"
    test_str_eq(toNumerals(s,0), s)
    s="1-A"
    test_str_eq(toNumerals(s,0), s)
    s="12-34-56-78"
    test_str_eq(toNumerals(s,0), s)
    print "Passed"

def test_comps(g, _max):
    """Tests the composition of toDecimal and toNumerals & vice versa
    for g <= 1. For all g > 1, the test can fail. For example, if g=2,
    then toDecimal(toNumerals("201",2))="21"!="201"
    """
    for i in range(1, _max):
        dec=str(i)
        nums=toNumerals(dec,g)
        dn=toDecimal(nums)
        nd=toNumerals(dn,g)
        if dec != dn or nums != nd:
            raise Exception("Test failed for i="+dec+" & g="+str(g)+", "+dec+"!="+dn+" or '"+nums+"'!='"+nd+"'")

def testPackage(_max):
    print "Starting tests"

    test_basic()

    test_non_nums()

    print "Testing compositions for all numbers from 0 to " + str(_max) + " for g=1,0,-1,-2,\"-4*\""

    print "Starting digit-by-digit test (g=1)"
    test_comps(1, _max)
    print "Passed"

    print "Starting all-digits test (g=0)"
    test_comps(0, _max)
    print "Passed"

    print "Starting digit-by-digit test (g=-1)"
    test_comps(1, _max)
    print "Passed"

    print "Starting pairs test (g=-2)"
    test_comps(-2, _max)
    print "Passed"

    print "Starting quads test (g=\"-4*\")"
    test_comps("-4*", _max)
    print "Passed"

    print "All tests passed"
