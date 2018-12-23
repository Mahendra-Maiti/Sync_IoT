import matplotlib.pyplot as plt

input_file_name="dataSync_bandwidth.txt"


x=[10,50,100,200,300,400,500,600,700,800,900,1000]
y_1=[1.11,5.1,10.33,20.58,31.31,42.49,52.39,62.33,71.12,85.00,98.46,106.18]
y_2=[1.98,8.72,20.02, 31.38, 45.14, 57.01, 69.46, 84.19, 111.23, 138.44, 161.35, 198.68]

# received_points=[]
# delivered_points=[]

#lines=[line.rstrip('\n') for line in open(input_file_name)]
#for line in lines:
#    words=line.split(' ')
#    if len(words)==0:
#        continue
#    print(words)
#    print(words)
#    y_1.append(float(words[0]))
#    y_2.append(float(words[1]))
#    x.append(int(words[2]))

print(x)
print(y_1)
print(y_2)


plt.plot(x,y_1, label='iot-edge')
plt.plot(x,y_2, label='iot-cloud')
plt.xlabel('Number of messages')
plt.ylabel('Time in seconds ')
plt.legend()
plt.show()
#received_points=[20,50,100,200, 250, 300,400, 600, 900,1000, 1500, 2000, 2500, 3000, 3500, 4000, 8000]
#
#delivered_points_1=[17,45,81,158,220, 236,307, 491, 764, 872, 1336, 1772, 2179, 2603, 2932, 3205, 5968]
#
#delivered_points_2=[]

#for val in received_points:
#    delivered_points_2.append((int)((val/12)+1))


#print(received_points)
#print(delivered_points_1)
#print(len(received_points))
#print(len(delivered_points_1))

#plt.plot(received_points,received_points, label="unfiltered")
#plt.plot(received_points,delivered_points_1, label="filter_1")
#plt.plot(received_points,delivered_points_2, label="filter_2")
#plt.xlabel("received points")
#plt.ylabel("delivered points")
#plt.legend()
#plt.show()
#plt.savefig('result.png')



