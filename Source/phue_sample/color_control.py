from phue import Bridge

b = Bridge("192.168.0.21")
b.connect()

lights = b.lights
print(lights)

for i in range(0,len(lights)):
    if i==0:
        lights[i].xy = [0.5,1]
    elif i==1:
        lights[i].xy = [0.1,0.1]
    elif i==2:
        lights[i].xy = [0.7,0.3]