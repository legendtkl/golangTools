import sys


def convert(s):
    L = [x for x in range(len(s)) if s[x]<'a']
    L.append(len(s))
    S = [s[L[i]:L[i+1]].lower() for i in range(len(L)-1)]
    return '_'.join(S)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(-1)

    sql = open(sys.argv[1])
    go = open(sys.argv[2], 'wb')
    flag = False

    for line in sql:
    	if line.startswith('type') or line.startswith('package') or line.startswith('}') or line=='\n':
    		go.write(line)
    	else:
    		line = line.strip()
    		L = line.split(' ')
    		attr = convert(L[0])

    		go.write(line + "\t`json:\""+attr+"\"`\n")
    go.close()
    sql.close()
    
