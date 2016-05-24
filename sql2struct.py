
# 对于Golang中的ORM处理经常需要针对数据库中表的字段新建Struct
# 这个工具就是针对目前存在的表结构，自动生成Struct
# 使用方法：python sql2struct.py your.sql your.go

import sys

def convertCaptitle(s):
	s = s[1:len(s)-1]
	l = s.split('_')
	s = ''
	for i in l:
		s += i.title()

	return s

if __name__ == '__main__':
	if len(sys.argv) < 3:
		sys.exit(-1)

	sql = open(sys.argv[1])
	go = open(sys.argv[2], "wb")
	flag = False

	for line in sql:
		if line.startswith('CREATE'):
			flag = True
			s = line.strip().split(' ')[2]
			s = convertCaptitle(s)
			go.write("type " + s + " struct{\n")
		elif flag == True:
			line = line.strip()
			if line.startswith('`'):
				L = line.split(' ')
				attr = convertCaptitle(L[0])
				gotype = ''
				if L[1].startswith('tinyint'):
					gotype = L[2]=='unsigned' and 'uint8' or 'int8'
				elif L[1].startswith('smallint'):
					gotype = L[2]=='unsigned' and 'uint16' or 'int16'
				elif L[1].startswith('mediumint') or L[1].startswith('int'):
					gotype = L[2]=='unsigned' and 'uint32' or 'int32'
				elif L[1].startswith('bigint'):
					gotype = L[2]=='unsigned' and 'uint64' or 'int64'
				elif L[1].startswith('float'):
					gotype = 'float32'
				elif L[1].startswith('double'):
					gotype = 'float64'
				elif L[1].startswith('decimal'):
					gotype = 'float64'
				elif L[1].startswith('timestamp') or L[1].startswith('datetime'):
					gotype = 'time.Time'
				elif L[1].startswith('time'):
					gotype = 'time.Duration'
				elif L[1].startswith('year'):
					gotype = 'int16'
				else:
					gotype = 'string'

				content = ' '.join(['\t', attr, gotype])
				if L[-2] == 'COMMENT':
					content += '\t//' + L[-1]
				go.write(content+'\n')

			elif line.startswith(') ENGINE'):
				flag = False
				go.write("}")
				break


