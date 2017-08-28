
import os
import sys
import re
import subprocess

# Note - someone familiar with Windows might be able to make
# this work on Windows

if sys.platform.startswith('win') :
    print('These unit tests likely fail on Windows', os.platform)

os.system("rm testtmp/*")
os.system("mkdir -p testtmp")

# Known Failures
failures = [
    'BeautifulSoup.py',
    'roster.py',
    'search8.py',
    'search9.py',
    'socket1.py',
    'socket2.py',
    'urljpeg.py'
    # 'urllink2.py',  -- Fixed
    # 'urllinks.py',  -- Fixed
]

toskip = [
    'notry.py', # will always exception
    'unit.py', # avoid infinite loops
    'wikigrade.py',  # talks to ctools - too complex
    'argfile.py', # argument passing - no need to test
    'argtest.py', # argument passing - no need to test
    'gitpulls.py', # No auth codes
    'urllink3.py' # might run forever
]

print('======== Starting Python 2 Tests ==============')

success = 0
fail = 0
codefolder = '../code'

for i in os.listdir(codefolder):
    if not i.endswith(".py"): 
        continue
    if i in toskip : continue
    if i in failures : continue
    if i.startswith('tw') : continue
    if i.startswith('txt') : continue
    base = i.replace(".py","")
    data = open(codefolder+'/'+i).read()
    lines = data.split('\n')
    inputs = re.findall('input.*\([^\n]*\)',data.lower())
    finputs = re.findall('input.*\([^\n]*enter[^\n]*file[^\n].*\)',data.lower())
    if len(inputs) == 1 and len(finputs) == 1 : 
        cmd = "python "+codefolder+'/'+i+" < testinp/mbox-short.inp > testtmp/"+base+".txt"
        code = os.system(cmd)
    elif len(inputs) > 0 :
        inputname = 'testinp/'+base+'.inp'
        try:
            fh = open(inputname)
            fh.close()
            code = 0
        except:
            cmd = "Not Handled: "+i;
            code = 1

        if code == 0 :
            cmd = "python "+codefolder+'/'+i+" < testinp/"+base+".inp > testtmp/"+base+".txt"
            code = os.system(cmd)

    else :
        cmd = "python "+codefolder+'/'+i+" > testtmp/"+base+".txt"
        code = os.system(cmd)

    if code == 0 :
        success = success + 1
        continue

    fail = fail + 1
    print ('*** FAIL2 ***',cmd)

print('Tests 2 passed:',success)
print('Tests 2 failed:',fail)
if ( len(failures) > 0 ) : print('Unit Test TODO:',failures)
os.system("rm *.sqlite")

print("Comparing outputs...")

# code = os.system("diff -r testout testtmp | grep -v '^Only in testtmp: '")
p = os.popen("diff -r testout testtmp")
data = p.read()
lines = data.rstrip().split('\n')
diff = False
for line in lines:
    if line.startswith('Only in testtmp: ') :
        continue
    print (line)
    diff = True
if diff or fail >= 1 :
    sys.exit(1)

