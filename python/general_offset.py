aff = """camera(27096,200.00,0.00,0.00,0.00,0.00,0.00,l,22);
camera(27118,-200.00,0.00,0.00,0.00,0.00,0.00,l,22);
camera(27140,-132.00,0.00,0.00,0.00,0.00,0.00,l,22);
camera(27162,132.00,0.00,0.00,0.00,0.00,0.00,l,22);
camera(27184,87.12,0.00,0.00,0.00,0.00,0.00,l,22);
camera(27206,-87.12,0.00,0.00,0.00,0.00,0.00,l,22);
camera(27228,-57.50,0.00,0.00,0.00,0.00,0.00,l,22);
camera(27250,57.50,0.00,0.00,0.00,0.00,0.00,l,22);
camera(27272,37.95,0.00,0.00,0.00,0.00,0.00,l,22);
camera(27294,-37.95,0.00,0.00,0.00,0.00,0.00,l,22);
camera(27316,-25.05,0.00,0.00,0.00,0.00,0.00,l,22);
camera(27338,25.05,0.00,0.00,0.00,0.00,0.00,l,22);
camera(27360,16.53,0.00,0.00,0.00,0.00,0.00,l,22);
camera(27382,-16.53,0.00,0.00,0.00,0.00,0.00,l,22);
camera(27404,-10.91,0.00,0.00,0.00,0.00,0.00,l,22);
camera(27426,10.91,0.00,0.00,0.00,0.00,0.00,l,22);""".split("\n")

OFFSET = 93329 - 27096

after = []

for cmd in aff:
	sp1 = cmd.split("(")
	procedure = sp1[0]
	sp2 = sp1[1].split(",")
	time = sp2[0]
	time_mod = str(int(time) + OFFSET)
	after.append(procedure + "(" + time_mod + "," + ",".join(sp2[1:]))
	
print("\n".join(after))
