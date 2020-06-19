import jetson.inference
import jetson.utils
a=[[],[]]
count=0
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.gstCamera(720, 576, "0")  # using V4L2
display = jetson.utils.glDisplay()

while display.IsOpen():
	img, width, height = camera.CaptureRGBA()
	detections = net.Detect(img, width, height)
	display.RenderOnce(img, width, height)
	display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
	print("detected {:d} objects in image".format(len(detections)))
	if(len(detections)>2):
		for f in range(len(detections)):
			a.append([])
	else:
		a=[[],[]]
	try:
		for detection in detections:
			if detection.ClassID==3:
				a[count]=list(detection.Center)
				print("coordinates of the center of car "+str(count+1)+"{}".format(a[count]))
				count=count+1
		count=0
		x=abs((a[0][0]-a[1][0])/2)+min(a[0][0],a[1][0])
		y=(a[0][1]+a[1][1])/2
		print("center between cars ("+str(x)+","+str(y)+")")
	except:
		print("no objects were detected")