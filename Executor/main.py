import sys
import os

if len(sys.argv) == 1 or str(sys.argv[1]) == "/?":
    print('''Usage: /q/ for quotes
       /? for this help message
       /a <arg> for customize exec (Do not require /q/) 
       /l <Link> execute as custom Link''')
    sys.exit()

count = len(sys.argv)
in_string = str()
data = sys.argv[1:]
exec_program = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
processed = 0
if '/l' in sys.argv and processed == 0:
    argp = sys.argv.index('/l')
    if len(sys.argv) <= 4:
        in_string = " " + str(str(sys.argv[argp + 1]).split('//')[1])
        data = sys.argv[2]
        if "/a" in data:
            in_string = ""
            data = str(data).split("%20")[1:]
            processed = 0
        else:
            print("Single Value")
            processed = 1
            data = []
    elif len(sys.argv) >= 5:
        in_string = str(str(sys.argv[argp + 1]).split('//')[1])[:-1]
        data = sys.argv[1:argp] + sys.argv[argp + 2:]
        argp = data.index('/a')
        exec_program = str(data[argp + 1])
        data = data[1:argp] + data[argp + 2:]
        processed = 1
if '/a' in sys.argv and processed == 0:
    argp = sys.argv.index('/a')
    exec_program = str(sys.argv[argp + 1])
    data = sys.argv[1:argp] + sys.argv[argp + 2:]
elif '/a' in data and processed == 0:
    argp = data.index('/a')
    exec_program = str(data[argp + 1]).replace("%5C", "\\")
    data = data[1:argp] + data[argp + 2:]
print(f'Count: {count}', f'\nData List:{data}', f'\nSys Arguments List:{sys.argv}')
for arg in data:
    if "/q/" in arg:
        if "/q/" in arg[:3]:
            arg = f'"{arg[3:]}'
        if "/q/" in arg[-3:]:
            arg = f'{arg[:-3]}"'
        in_string = in_string + " " + arg
    else:
        in_string = in_string + " " + arg
print(f'Starting: "{exec_program}"{in_string}')
print(os.popen(f'"{exec_program}"{in_string}').read())
