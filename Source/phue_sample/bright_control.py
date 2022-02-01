from phue import Bridge

b = Bridge("192.168.0.21")
b.connect()

lights = b.lights
print(lights)
flights = b.lights
print(lights)
for i in range(0,len(lights)):
	if i==0:
		lights[i].brightness=0
	elif i==1:
		lights[i].brightness=100
	elif i==2:
		lights[i].brightness=254