import re

txt = """There
aint much
rain in 
Spain"""

#Search for the sequence "ain", at the beginning of a line:
print(re.findall("^ain", txt, re.MULTILINE))

#This example would return no matches without the re.MULTILINE flag, because the ^ character without re.MULTILINE only get a match at the very beginning of the text:
print(re.findall("^ain", txt))


#Same result with the shorthand re.M flag:
print(re.findall("^ain", txt, re.M))


