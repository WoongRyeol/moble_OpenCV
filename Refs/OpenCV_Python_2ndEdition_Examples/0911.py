# 09011.py
import cv2
import numpy as np

#1
def distance(f1, f2):    
    x1, y1 = f1.pt
    x2, y2 = f2.pt
    return np.sqrt((x2 - x1)**2+ (y2 - y1)**2)

def filteringByDistance(kp, distE=0.5):
    size = len(kp)
    mask = np.arange(1,size+1).astype(np.bool8) # all True   
    for i, f1 in enumerate(kp):
        if not mask[i]:
            continue
        else: # True
            for j, f2 in enumerate(kp):
                if i == j:
                    continue
                if distance(f1, f2)<distE:
                    mask[j] = False
    np_kp = np.array(kp)
    return list(np_kp[mask])
    
#2
src = cv2.imread('./data/cornerTest.jpg')
gray= cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)

##siftF = cv2.SIFT_create()
siftF = cv2.SIFT_create(edgeThreshold = 80)

kp= siftF.detect(gray)
print('len(kp)=', len(kp))

#3
kp = sorted(kp, key=lambda f: f.response, reverse=True)
##filtered_kp = list(filter(lambda f: f.response>0.01, kp))
filtered_kp = filteringByDistance(kp, 10)
print('len(filtered_kp)=', len(filtered_kp))

kp, des = siftF.compute(gray, filtered_kp)
print('des.shape=', des.shape)
print('des.dtype=', des.dtype)
print('des=', des)

#4
dst = cv2.drawKeypoints(src, filtered_kp, None, color=(0,0,255))  
for f in filtered_kp:
    x, y = f.pt
    size = f.size
    rect = ((x, y), (size, size), f.angle)
    box = cv2.boxPoints(rect).astype(np.int32)
    cv2.polylines(dst, [box], True, (0,255,0), 2)
    cv2.circle(dst, (round(x), round(y)), round(f.size/2), (255,0,0), 2)
cv2.imshow('dst',  dst)
cv2.waitKey()
cv2.destroyAllWindows()
