from random import choices
from string import ascii_lowercase, ascii_uppercase
from textwrap import indent
from regex import compile as re_compile

from .extractor import TestcellBlock 

clean_pat = re_compile('\W|^(?=\d)')

def format_testcase_function(
        testcase: str,
        testcase_num: int
    ) -> str:
    testcase_clean = clean_pat.sub("_", testcase)
    return \
    f"def test_{testcase_clean}():\n" \
    "\tpart_completed, error = load_stored_test_data()\n" \
    f"\tif part_completed < {testcase_num}:\n" \
    "\t\traise error\n" \
    "\telse:\n" \
    "\t\treturn\n"
    
def compile_code_and_tests_into_py(
    code_blocks: TestcellBlock,
    ):
    """Given code and test blocks with testcase names matched by codeblock names, 
    return a python file that is pytest testable.

    Args:
        code_blocks: TestcellBlock containing relevant code.

    Returns:
        A string containing the python code that can be written to a file for pytest testing.
    """

    part_name = choices(ascii_lowercase + ascii_uppercase, k=20)
    part_name = "".join(part_name)

    func_name = choices(ascii_lowercase + ascii_uppercase, k=20)
    func_name = "".join(func_name)
    py_code = f"import pytest\nimport json\n\npart_completed = -1\ndef {func_name}({part_name}):\n"
    content = "global part_completed\n"

    for testcase in code_blocks.cases:
        print(f"Adding code for {testcase}")
        code_content = code_blocks.get_code_for_testcase(testcase)
        test_content = code_blocks.get_test_for_testcase(testcase)

        content += code_content
        content += "\n"
        if len(test_content) > 0:
            print(f"Adding test for {testcase}")
            content += f"if {part_name} == \"{testcase}\" or {part_name} == \"all\":\n"
            test_content += f"\nif {part_name} != \"all\":\n\treturn\n"
            content += indent(test_content, "\t")

        content += "part_completed = part_completed + 1\n\n"


    content += "raise Exception(\"All testcases passed\")\n"
    py_code += indent(content, "\t")

    py_code += \
    "def load_stored_test_data():\n" \
    "\twith open(\"test_data.json\", \"r\") as f:\n" \
    "\t\tdata = json.load(f)\n" \
    "\tpart_completed, note = data[\"part_completed\"], data[\"note\"]\n" \
    "\tif note == \"\":\n" \
    "\t\treturn part_completed, None\n" \
    "\terror = Exception(note)\n" \
    "\treturn part_completed, error\n"

    for i, testcase in enumerate(code_blocks.cases):
        py_code += format_testcase_function(testcase, i)

    py_code += \
    "if __name__ == \"__main__\":\n" \
    "\twith pytest.raises(Exception) as e:\n" \
    f"\t\t{func_name}(\"all\")\n" \
    "\tnote = \"\"\n" \
    "\tif \"All testcases passed\" not in str(e.value):\n" \
    "\t\tnote = str(e.getrepr())\n" \
    "\tjson_data = { \"part_completed\": part_completed, \"note\": note }\n" \
    "\twith open(\"test_data.json\", \"w\") as f:\n" \
    "\t\tf.write(json.dumps(json_data))\n"
    return py_code
