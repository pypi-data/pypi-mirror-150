"""
example of the format required for input
test = [
    ["full command", "short command", "description"],
    ["--help", "-h", "command help"],
    ["--today", "-n", "today's timetable"],
    ["--yesterday", "-y", "yesterday's timetable"],
    ["--tomorrow", "-t", "tomorrow's timeable"],
    ["--start {num days}", "-s {num days}", "timetable from {num days} ago"],
    ["--end {num days}", "-e {num days}", "timetable to {num days} time"]
]
Uses the following characters for formatting
═ ║ 
╝ ╚ ╗ ╔ 
╠ ╣ ╩ ╦ ╬
"""

def inv_array(arr):
    rtn = []
    height = len(arr)
    width = len(arr[0])
    for item in range(width):
        col = []
        for line in range(height):
            col.append(arr[line][item])
        rtn.append(col)
    return rtn

def n_chars(c, n):
        return c.join(['' for i in range(n + 1)])

def clean(table):
    final = []
    for x in table:
        o = []
        for y in x:
            o.append(y.replace('\n', ' | ').replace('|  |', '|'))
        final.append(o)
    return final

def tablify(table):
    table = clean(table)
    len_t = []
    width = 0
    height = len(table)
    for line in table:
        col = []
        for item in line:
            col.append(len(item))
        width = len(col)
        len_t.append(col)
    
    len_mir = inv_array(len_t)

    final =  "╔" + '╦'.join([n_chars('═', max(n)) for n in len_mir]) + '╗\n'
    final += "║" + '║'.join([table[0][i] + n_chars(' ', max(len_mir[i]) - len(table[0][i])) for i in range(width)]) + "║\n"
    final += "╠" + '╬'.join([n_chars('═', max(n)) for n in len_mir]) + '╣\n'
    final += '\n'.join([("║" + '║'.join([table[j + 1][i] + n_chars(' ', max(len_mir[i]) - len(table[j + 1][i])) for i in range(width)]) + "║") for j in range(height - 1)]) + "\n"
    final += "╚" + '╩'.join([n_chars('═', max(n)) for n in len_mir]) + '╝\n'

    return final

def tablify_str(table, length):
    table = tablify(table)

    final = []

    char_count = 0
    current = ""
    for line in table.split('\n'):
        if char_count + len(line) + 1 >= length:
            final.append(f"```{current}```")
            current = ""
            char_count = 0
        
        current += line + "\n"
        char_count += len(line) + 1
    final.append(f"```{current}```")
            
    #for n in range(0, math.ceil(len(table) / 1994)):
    #    final.append(f"```{table[1994 * n : 1994 * n + 1994]}```")

    return final