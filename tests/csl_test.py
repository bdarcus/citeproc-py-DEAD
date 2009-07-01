
import json
from lxml import etree
#import csl
import glob
import os

os.getcwd()

TESTS = glob.glob('*.json')

def run_ctest(test_index, test_path):
    try:
        test = json.loads(open(test_path).read())
        print("\n==================================\n", test['name'], "\n==================================")
        print("   expecting: ", test['result'])
        try:
            csl = etree.fromstring(test['csl'])
            # result = csl.processor.process_citations()
        except:
            print("\n    XML parsing failed, using following fragment:")
            print(test['csl'])
    except:
        print("  ", test_path, "  failed")


def run_tests(category='all'):
    print("There are ", len(TESTS), " tests to run.")
    for test_index, test_path in enumerate(TESTS):
        print("     test: ", test_index + 1, " ", test_path)
        run_ctest(test_index, test_path)


run_tests()
