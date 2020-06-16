import cv2
import numpy as np
imgsrc = r'tree.png'
img = cv2.imread(imgsrc, 0)
height = img.shape[0]
width = img.shape[1]
nparrayimage = np.array(img)
arr = nparrayimage.flatten()

window = int(input("Enter Window Size:"))
lookahead = int(input("Enter Lookahead Buffer Size:"))
search = window - lookahead -1
decodedarray = []
l = 0
# here the array of the fixed first search buffer used for decoding
while l <= search:
    decodedarray.append(arr[l])
    l += 1
start = 0
encoded_arr = []
while start+window <= len(arr):
    pointer = arr[window+start-lookahead]
    pointerindex=window+start-lookahead
    start_searchbuffer = window+start-lookahead-1
    best_distance = 0
    i = start_searchbuffer
    distance = 0
    length = 0
    d = 0
    counter = 0
    check = 0
    char = pointer
    while i >= start:
        distance += 1
        if pointer == arr[i]:
            length = 1
            d = distance
            # if the matching is just the number only then take the nearest one
            if counter == 0:
                best_distance = distance
                counter += 1
            j = i+1
            while arr[j] == arr[pointerindex+1]:
                check = 1
                length = length +1
                j += 1
                pointerindex += 1
                char = arr[pointerindex+1]
        i -= 1
    if check == 0:
        d = best_distance
    encoded_arr.append(d)
    encoded_arr.append(length)
    encoded_arr.append(char)
    start = start+length+1


Encode = np.array(encoded_arr, dtype=np.uint8)
np.save("EncodedFile", Encode)

# p is a pointer at the end of the fixed search buffer
p = decodedarray[search]
c = 0
while c < len(encoded_arr):
    distance = encoded_arr[c]
    l = encoded_arr[c+1]
    c = c + 2
    if distance == 0:
        decodedarray.append(encoded_arr[c])
        # to move the end of the fixed buffer to the new element added
        search += 1
        c = c+1
        p = decodedarray[search]
    else:
        search = search-distance+1
        u = 0
        while u < l:
            decodedarray.append(decodedarray[search])
            search += 1
            u += 1
        search = search + (distance - l) + l
        decodedarray.append(encoded_arr[c])
        c += 1

if len(decodedarray) < len(arr):
    counter = len(decodedarray)
    while counter < len(arr):
        decodedarray.append(0)
        counter += 1


npbacktooriginal = np.array(decodedarray, dtype=np.uint8)
npbacktooriginal = npbacktooriginal.reshape(height, width)
cv2.imshow('image', npbacktooriginal)
cv2.waitKey(0)
cv2.destroyAllWindows()





