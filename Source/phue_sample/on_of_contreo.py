from phue import Bridge

b = Bridge("192.168.0.21")
b.connect()

lights = b.lights
print(lights)

for i in range(0,len(lights)):
	if i==0:
		lights[i].on = False
	elif i==1:
		lights[i].on = True
	elif i==2:
		lights[i].on = False