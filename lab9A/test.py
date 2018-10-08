#!/usr/bin/env python3
import os, unittest, collections, types, json, traceback, pprint
import wrapper

TEST_DIRECTORY = os.path.dirname(__file__)

def validate_rendering(blobs):
    return all("pos" in b and "texture" in b and "player" in b for b in blobs)

def frame2set(frame):
    return {(("pos", tuple(blob["pos"])), ("texture", blob["texture"]), ("player", blob["player"])) for blob in frame}

def sort_blob_set(blobs):
    return [dict(b) for b in sorted(blobs)]

def verify_replay(student_trace, reference_trace):
    assert len(student_trace) == len(reference_trace)
    # pprint.pprint(zip(student_trace, reference_trace))
    for fid, (student, reference) in enumerate(zip(student_trace, reference_trace)):
        stustatus, stuframe = student
        refstatus, refframe = reference
        if not validate_rendering(stuframe):
            return "Invalid frame (contains a malformed blob):\n {}".format(pprint.pformat(stuframe))
        stuset, refset = frame2set(stuframe), frame2set(refframe)
        if stuset != refset or stustatus != refstatus:
            lines = ["", "# Frame #{} diverges from reference.".format(fid)]
            extraneous, missing = stuset - refset, refset - stuset
            if stustatus != refstatus:
                lines.append("\n## Incorrect game status: {} (expected {})".format(stustatus, refstatus))
            if missing:
                lines.append("\n## Missing from your rendering:")
                lines.append(pprint.pformat(sort_blob_set(missing)))
            if extraneous:
                lines.append("\n## Found in your rendering, but unexpected:")
                lines.append(pprint.pformat(sort_blob_set(extraneous)))
            return "\n".join(lines)

TRANSLATIONVECTOR_TEMPLATE = "Unexpected result: expected translation vector {}, got {}, for rectangles {}, {}."
INTERSECTION_TEMPLATE = "Unexpected result: your implementation claims that {} {} {}."

def verify_intersection(result, reference):
    for (r1, r2, res), ref in zip(result, reference):
        if res != ref:
            verb = "intersects" if res else "does not intersect"
            return INTERSECTION_TEMPLATE.format(r1, verb, r2)

def verify_translationvector(result, reference):
    for (r1, r2, res), ref in zip(result, reference):
        if isinstance(res,list): res = tuple(res)
        if isinstance(ref,list): ref = tuple(ref)
        if res != ref:
            return TRANSLATIONVECTOR_TEMPLATE.format(ref, res, r1, r2)

def verify(result, input_data, gold):
    restype, result = result

    if restype == "error":
        return False, "raised an error: {}".format(result)

    try:
        test_type = input_data.pop("type")
        verifn = {"replay": verify_replay,
                  "intersection": verify_intersection,
                  "translationvector": verify_translationvector}[test_type]
        errmsg = verifn(result, gold)

        if errmsg is not None:
            return False, errmsg
        else:
            return True, "is correct. Hooray!"
    except:
        traceback.print_exc()
        return False, "crashed :(. Stack trace is printed above so you can debug."

def verify_case(cname):
    # read .in and .out files from cases
    with open(os.path.join('cases',cname+'.in'),'r') as f:
        indata = f.read()

    with open(os.path.join('cases',cname+'.out'),'r') as f:
        outdata = f.read()

    # first run the test
    result = wrapper.run_test(json.loads(indata))

    # then run the verifier
    vresult,vmsg = verify(result, json.loads(indata), json.loads(outdata))

    # if failure, alert the test system
    if not vresult:
        raise AssertionError(vmsg)

##################################################
##  Tests
##################################################

class Test01(unittest.TestCase):
    def test_01(self): verify_case('1')
    def test_02(self): verify_case('2')
    def test_03(self): verify_case('3')

class Test02(unittest.TestCase):
    def test_04(self): verify_case('4')
    def test_05(self): verify_case('5')

class Test03(unittest.TestCase):
    def test_06(self): verify_case('6')
    def test_07(self): verify_case('7')
    def test_08(self): verify_case('8')
    def test_09(self): verify_case('9')

class Test04(unittest.TestCase):
    def test_10(self): verify_case('10')
    def test_11(self): verify_case('11')
    def test_12(self): verify_case('12')
    def test_13(self): verify_case('13')
    def test_14(self): verify_case('14')
    def test_15(self): verify_case('15')
    def test_16(self): verify_case('16')
    def test_17(self): verify_case('17')
    def test_18(self): verify_case('18')
    
class Test05(unittest.TestCase):
    def test_19(self): verify_case('19')

class Test06(unittest.TestCase):
    def test_20(self): verify_case('20')
    def test_21(self): verify_case('21')
    def test_22(self): verify_case('22')
    
##################################################
##  test setup
##################################################

if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
