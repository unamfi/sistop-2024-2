import string

memoria=[]
i=0
while i<=29:
	memoria.append('-')
	i=i+1
menu=1
choice=3
ch=0
space=0
lib=[]
temp=[]

while menu==1:
	i=0
	print("Asignación actual:")
	while i<30:
		print(memoria[i], end="")
		i=i+1
	print("\n |Asignar (0)|Liberar (1)|Salir (2):")
	choice=int(input())
	if choice==2:
		break
	if choice==0:
		space=0
		while space<2 or space>15:
			proc=string.ascii_uppercase[ch]
			print(f"Nuevo proceso ({proc}):")
			space=int(input())
		ch=ch+1
		y='-'
		available=memoria.count('-')
		if available>=space:
			adyacente=0
			i=0
			while adyacente<space:
				var=memoria[i]
				if var=='-':
					adyacente=adyacente+1
					lib.append(i)
				elif adyacente!=0:
					print("Compactando...")
					nextproc=memoria[i+1]
					y=nextproc
					occupied=memoria.count(nextproc)
					free=len(lib)-1
					x=0
					while x<free+1:
						memoria.pop(lib[free-x])
						memoria.insert(lib[free-x],nextproc)
						memoria.pop(lib[free-x]+occupied)
						memoria.insert(lib[free-x]+occupied,'-')
						x=x+1
					adyacente=0
					lib.clear()
				i=i+1
			x=0
			while x<space:
				y=lib[x]
				memoria.pop(y)
				memoria.insert(y, proc)
				x=x+1
			lib.clear()
		else:
			print ("No hay espacio suficiente")
	elif choice==1:
		i=0
		x=0
		z=0
		temp.clear()
		temp.append(' ')
		while i<30:
			if (memoria[i] != temp[x]) and memoria[i]!='-':
				temp.append(memoria[i])
				x=x+1
			i=i+1
		print(f"Proceso a liberar {temp}:")
		process=input()
		process=process.upper()
		used=len(memoria)
		while z<used:
			if memoria[z]==process:
				memoria.pop(z)
				memoria.insert(z,'-')
			z=z+1