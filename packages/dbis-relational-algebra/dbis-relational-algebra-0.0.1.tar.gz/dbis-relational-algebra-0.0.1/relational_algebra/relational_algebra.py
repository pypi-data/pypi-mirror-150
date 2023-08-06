import subprocess
import re
from IPython.display import display, Markdown
from tabulate import tabulate

def extract_tuples_and_attributes(db_path, expression):
    result = subprocess.run(["radb", db_path], input = expression, encoding = 'utf8', capture_output = True)

    #print(result.stdout)

    if "ra> " in result.stdout:
        output = result.stdout.split("ra> ")[1]
    else:
        output = result.stdout
    
    if ("ERROR: " in output):
        print("Error: " + output.split("ERROR: ")[1])
        return False
    else:
        lines = output.split("\n")
        attributes = re.findall("[(| ]\w+:", lines[0])
        attributes = list(map(lambda s: s[1:-1], attributes))
        tuples = []
        for line in lines[2:]:
            if line.startswith("-"):
                break
            tuples.append(list(map(str.strip, line.split(","))))
        return tuples, attributes

def radb_evaluate(db_path, expression):
    x = extract_tuples_and_attributes(db_path, expression)
    if (x == False):
        return False
    else:
        tuples, attributes = x
        table = tabulate(tuples, attributes, tablefmt="github")
        display(Markdown(table))
        return expression

def radb_check(db_path, expression, tuples_should, attributes_should):
    x = extract_tuples_and_attributes(db_path, expression)
    if (x == False):
        return False
    else:
        tuples, attributes = x
        #print(tuples)
        #print(attributes)
        return check_table(attributes, attributes_should, tuples, tuples_should)

def check_table(attributes, attributes_should, tuples, tuples_should):
    errors = 0
    for i in range(len(attributes_should)):
        if (i >= len(attributes) or attributes[i] != attributes_should[i]):
            print(f"Missing or wrong attribute at position {i}. Expected: {attributes_should[i]}")
            errors += 1
    for i in range(len(tuples_should)):
        if (tuples_should[i] not in tuples):
            print(f"Missing tuple: {tuples_should[i]}")
            errors += 1

    if errors == 0:
        return True
    else:
        return False
        