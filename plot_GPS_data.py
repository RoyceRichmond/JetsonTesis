import folium
#from google.colab import files
#uploaded = files.upload()
m = folium.Map(location=[19.5470007,-99.0150628],zoom_start=17.5)
path="logging.txt"
x=[]
y=[]
alt=[]
with open(path) as f_o:    
    lines=f_o.readlines()
for co in range(len(lines)):
    b=lines[co]
    temp=b.rstrip().replace("["+str(co)+"]","")
    temp=temp.split(',')
    x.append(float(temp[0]))
    y.append(float(temp[1]))
    alt.append(float(temp[2]))
for a in range(len(lines)-1):
    folium.CircleMarker([x[a], y[a]],radius=5,color='blue',fill=True,fill_color='#3186cc',fill_opacity=0.7,parse_html=False).add_to(m)
m
#m.save('GPStest.html')