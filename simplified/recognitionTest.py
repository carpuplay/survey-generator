import cv2
import numpy as np
from pdf2image import convert_from_path

images = convert_from_path("/Users/acarp/gitWorkspace/survey-generator/mamadou.pdf")

for i in range(len(images)):
    images[i].save('/Users/acarp/gitWorkspace/survey-generator/simplified/image_to_read.jpg', 'JPEG')

# read image
img = cv2.imread('/Users/acarp/gitWorkspace/survey-generator/simplified/image_to_read.jpg')
h, w = img.shape[:2]

# threshold on color
lower=(0,0,0)
upper=(50,50,50)
thresh = cv2.inRange(img, lower, upper)

# apply morphology close
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

# get contours
result = img.copy() 
centers = []
contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = contours[0] if len(contours) == 2 else contours[1]
print("count:", len(contours))
print('')
i = 1
for cntr in contours:
    M = cv2.moments(cntr)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    centers.append((cx,cy))
    cv2.rectangle(result, (cx+5, cy+5), (cx-5, cy-5), (0, 255, 0), -1)
    pt = (cx,cy)
    print("circle #:",i, "center:",pt)
    i = i + 1
    
# print list of centers
#print(centers)

# save results
cv2.imwrite('omr_sheet_thresh.png',thresh)
cv2.imwrite('omr_sheet_morph.png',morph)
cv2.imwrite('omr_sheet_result.png',result)
# show results
cv2.imshow("thresh", thresh)
cv2.imshow("morph", morph)
cv2.imshow("result", result)

cv2.waitKey(0)
cv2.destroyAllWindows()