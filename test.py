import cv2

path_pred = 'detections/0_Parade_marchingband_1_382.txt'
x = ''
with open(path_pred, 'r') as f:
	x = ' '.join([' '.join(l.rstrip().split(' ')[2:]) for l in f])

path_gr = 'groundtruths/0_Parade_marchingband_1_382.txt'
y = ''
with open(path_gr, 'r') as f:
	y = ' '.join([' '.join(l.rstrip().split(' ')[1:]) for l in f])

#
# x = '64.217674 231.73273 35.264244 27.646057' \
#     ' 236.67157 99.22584 42.502563 30.762169' \
#     ' 278.7127 821.86096 29.425049 22.143555' \
#     ' 182.58232 149.15413 31.216934 24.541016' \
#     ' 312.17532 878.16785 34.420746 29.165527' \
#     ' 87.32564 330.41644 34.90988 20.158203' \
#     ' 270.09686 850.90295 27.868103 21.26709' \
#     ' 31.11831 22.135262 26.622572 19.708069' \
#     ' 142.77873 834.41425 22.960068 17.777832' \
#     ' 246.22243 714.4618 31.716415 19.066162' \
#     ' 285.26538 767.59467 34.36389 17.537476' \
#     ' 275.09296 932.74243 27.682892 18.985352' \
#     ' 238.41153 644.52954 25.071472 18.605835' \
#     ' 247.50581 355.60034 30.536972 19.611694' \
#     ' 291.4853 771.7525 32.843567 19.34253' \
#     ' 175.50726 171.82555 28.897964 21.31778' \
#     ' 242.49661 409.0966 24.28421 17.98944' \
#     ' 276.0854 567.4508 30.824463 23.707397' \
#     ' 300.14746 654.4272 29.694702 23.641113' \
#     ' 239.08832 295.65933 21.174683 14.408752'
#
# y = """102 234 30 43 21 33 17 23 232 63 25 36 208 51 12 15 147 182 25 34 172 173 25 32 332 92 18 26 367 247 23 29 386 243 16 20 402 242 22 26 430 232 21 29 445 285 21 27 515 271 26 31 510 251 22 21 472 273 16 22 472 160 18 21 501 156 14 22 526 149 15 24 568 123 17 18 463 232 17 31 560 277 25 34 643 237 21 24 656 271 23 35 653 297 24 32 503 202 14 27 550 242 19 26 714 245 21 37 764 287 26 35 834 143 18 21 819 278 24 31 851 272 21 23 877 312 28 33 931 277 21 27 579 251 23 27 257 286 29 36 960 290 18 27 """


img = cv2.imread('WIDER_val/images/2--Demonstration/2_Demonstration_Demonstration_Or_Protest_2_644.jpg')

red = []  # predict
k = []
for i, p in enumerate(x.split(' ')):
	if i % 4 == 0:
		k = []
	k.append(p)
	if len(k) == 4:
		red.append([int(float(i)) for i in k])
		k = []

blue = []  # ground
k = []
for i, p in enumerate(y.split(' ')):
	if i % 4 == 0:
		k = []
	k.append(p)
	if len(k) == 4:
		blue.append([int(float(i)) for i in k])
		k = []
# print(blue)
print(len(red))
print(len(blue))

for l in red[:]:
	print(l)
	# cv2.rectangle(img, (l[1], l[0]), (l[1] + l[2], l[0] + l[3]), (255, 68, 159), 2)  # predict
	cv2.rectangle(img, (l[0], l[1]), (l[0] + l[2], l[1] + l[3]), (0, 255, 0), 2)  # predict

a, b, d, c = red[0]
print(b, a, d, c)

print(a <= b, c <= d)
# cv2.rectangle(img, (x, y), (900, 1200), (0, 0, 255), 2)
for l in blue[:]:
	# pass
	cv2.rectangle(img, (l[0], l[1]), (l[0] + l[2], l[1] + l[3]), (0, 87, 146), 2)

a, b, c, d = blue[0]
print(blue[0])

print(a <= b, c <= d)
cv2.imwrite('a.jpg', img)
cv2.imshow('test', img)
cv2.waitKey(300000)
cv2.destroyAllWindows()

# quit(0)

#
# path = 'detections/0_Parade_marchingband_1_382.txt'
#
# k = []
# with open(path, 'r') as f:
# 	for line in f:
# 		k.append(line.rstrip().split(' '))
#
# print(k[0])
# for thing in k:
# 	thing[4], thing[5] = thing[5], thing[4]
#
# print(k[0])
# #
# with open(path, 'w') as f:
# 	for line in k:
# 		f.write(' '.join(line) + '\n')
