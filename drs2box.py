import os
import subprocess
import drs2tuple
import re
import sys

b_r = re.compile("b([0-9]+)$")
c_r = re.compile("c([0-9]+)$")
p_r = re.compile("p([0-9]+)$")
k_r = re.compile("k([0-9]+)$")

special = ["NOT", "POS", "NEC", "OR", "IMP", "DUPLEX"]
ignore = ["CONSTITUENT","PROP"]

bt = []
ct = []

def refcode(ref):
	nref = []
	for r in ref:
		if p_r.match(r) is None:
			nref.append(r[0]+"_{"+r[1:]+"}")
		else:
			nref.append(r"""\pi_{"""+r[1:]+"}")
	return nref

def concode(cons):
	con = []
	for index, aim in enumerate(cons):
		args = []
		for c in ct:
			if c[0] == aim[1]:
				args.append(c[2])
		for idx, r in enumerate(args):
			if p_r.match(r) is None:
				args[idx] = r[0]+"_{"+r[1:]+"}"
			else:
				args[idx] = r"""\pi_{"""+r[1:]+"}"
		if aim[0] in special:
			con.append(aim[0]+r"""($"""+", ".join(args) + r"""$)""")
		if aim[0] in ignore:
			pass
		else:
			con.append(aim[0]+r"""($"""+", ".join(args) + r"""$)""")
	return con

def process(c_box,sub_ref,ref,conditions):
	cc = ""
	n_box = 0
	if c_box in ref or c_box in conditions:
		if sub_ref:
			if len(sub_ref) > 1:
				for sub in sub_ref:
					temp = process(nextbox(c_box,n_box),[sub],ref,conditions)
					cc += temp[0] + " "
					n_box += temp[1]
				return (cc,n_box)
			else:
				cc += r"""$"""+reg(sub_ref[0])+r"""$:~"""
		if c_box in ref:
			cc += r"""\drs{$""" + ", ".join(refcode(ref[c_box])) + r"""$}"""
		else:
			cc += r"""\drs{~}"""
		if c_box == "b0":
			l = 6
		else:
			l = 3
		n = len(conditions[c_box])//l
		con = concode(conditions[c_box])
		cc += r"""{""" + ", ".join(con[:l])
		for i in range(n):
			i += 1
			cc += r""" \\ """ + ", ".join(con[i*l:(i+1)*l])
		n_box += 1
		if c_box in ref and (any(k_r.match(r) for r in ref[c_box]) or any(p_r.match(r) for r in ref[c_box])):
			cc += r""" \\ """
			sub_ref = []
			for r in ref[c_box]:
				if k_r.match(r) is not None or p_r.match(r) is not None:
					sub_ref.append(r)
			temp = process(nextbox(c_box,1),sub_ref,ref,conditions)
			cc += temp[0]
			n_box += temp[1]
		cc += r"""}"""
		return (cc,n_box)
	else:
		return (cc,n_box)

def reg(r):
	if p_r.match(r) is None:
		return (r[0]+"_{"+r[1:]+"}")
	else:
		return (r"""\pi_{"""+r[1:]+"}")

def nextbox(c_box,n):
	return c_box[0] + str(int(c_box[1:])+n)

def box(drs):
	drs = drs.strip()
	tuples = drs2tuple.process(drs.split())
	for t in tuples:
		if b_r.match(t[0]) is not None:
			bt.append(t)
		elif c_r.match(t[0]) is not None:
			ct.append(t)
		else:
			print("The tuple " + t +" is not in the correct form.")
			return

	gcode = ""
	ref = {}
	conditions = {}

	for b in bt:
		if b[1] == "REF":
			if b[0] not in ref:
				ref[b[0]] = [b[2]]
			else:
				ref[b[0]].append(b[2])
		else:
			if b[0] not in conditions:
				conditions[b[0]] = [(b[1],b[2])]
			else:
				conditions[b[0]].append((b[1],b[2]))

	gcode = process("b0",[],ref,conditions)[0]

	content = r"""
	\documentclass[a4paper]{article}
	\usepackage{fancyhdr}
	\pagestyle{empty}
	\usepackage[landscape]{geometry}
	\usepackage{drs}
	\include{drs.macros}

	\begin{document}


	\begin{figure*}[t]
	\begin{small}
	""" + gcode + r"""
	\end{small}
	\end{figure*}

	\end{document}
	"""

	try:
		graph(content,drs)
	except Exception as e:
		return 0
	else:
		pass
	finally:
		pass

	return 1

def graph(content,drs):
	try:
		filename = str(hash(drs))
		with open(filename+'.tex','w') as f:
			f.write(content)
		proc = subprocess.Popen(['pdflatex', filename+'.tex'])
		proc.communicate()
		os.system('convert -verbose -density 150 '+filename+'.pdf -resize 75% -quality 100% '+filename+'.png')
	except Exception as e:
		raise
	else:
		pass
	finally:
		os.unlink(filename+'.tex')
		os.unlink(filename+'.log')
		os.unlink(filename+'.aux')

def drs2box(drs):
	bt = []
	ct = []
	try:
		box(drs)
	except Exception as e:
		return 0
	else:
		return 1
	finally:
		pass

if __name__ == "__main__":
	drs = "DRS( month( X1 ) earlier( E1 ) AGENT( E1 X1 ) THEME( E1 P1 ) P1( SDRS( K1( DRS( israel( X2 ) THING( X3 ) OF( X4 X3 ) ambassador( X4 ) venezuela( X5 ) to( X4 X5 ) recall( E2 ) AGENT( E2 X2 ) THEME( E2 X4 ) ) ) K2( DRS( mr.( X6 ) EQ( X7 X6 ) chavez( X7 ) say( E3 ) CAUSE( E3 X7 ) TOPIC( E3 P2 ) P2( DRS( israel( X8 ) OF( X9 X8 ) attack( X9 ) hezbollah( X10 ) against( X9 X10 ) lebanon( X11 ) in( X9 X11 ) genocide( X12 ) be( E4 ) AGENT( E4 X9 ) THEME( E4 X12 ) ) ) ) ) after( K1 K2 ) ) ) )"
	drs2box(drs)