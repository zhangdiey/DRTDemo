import cv2
import numpy as np
import re
import sys

font = cv2.FONT_HERSHEY_COMPLEX
fontScale = 0.4
fontColor = (0,0,0)
lineType = 1

p_r = re.compile("P([0-9]+)\($")
k_r = re.compile("K([0-9]+)\($")

special = ["DRS(","NOT(", "POS(", "NEC(", "OR(", "IMP(", "DUPLEX(","SDRS("]

def figure(height,width,tokens):
    img = np.zeros((height,width,3), np.uint8)
    img[:,:] = (255,255,255)
    pos = (0,10)
    index = 0
    token = tokens[index]
    index += 1
    if token != "DRS(":
    	print ("Wrong DRS input!")
    	return None
    else:
    	cv2.putText(img,token[:-1],pos,font,fontScale,fontColor,lineType)
    	sub = tree(pos,img,tokens[1:],0)
    	index += sub[0]
    if index == len(tokens):
    	width = sub[1]
    	height = sub[2]
    	resized_img = img[:height,:width]
    	return resized_img
    else:
    	print ("Wrong DRS input!")
    	return None

def tree(root,img,tokens,indent):
    index = 0
    width = 0
    height = 95
    pos = root
    pos = (indent,pos[1]+85)
    while index < len(tokens):
        token = tokens[index]
        index += 1
        if token == ")":
        	return (index,width,height)
        cv2.line(img, (pos[0]+totalSize(token),pos[1]-10), (root[0]+10, root[1]+5), (0,0,0), 1)
        if token in special or p_r.match(token) is not None or k_r.match(token) is not None:
        	cv2.putText(img,token[:-1],pos,font,fontScale,fontColor,lineType)
        	sub = tree(pos,img,tokens[index:],indent)
        	index += sub[0]
        	width += sub[1]
        	indent += sub[1]
        	height = max(height,sub[2]+95)
        	pos = (width,pos[1])
        else:
        	cv2.putText(img,token,pos,font,fontScale,fontColor,lineType)
        	pos = (pos[0]+len(token)*10,pos[1])
        	width += len(token)*10


def totalSize(tokens):
	size = 0
	for token in tokens:
		size = size + len(token)*1.5
	return int(size)

def refine(tokens):
    refined_tokens = []
    refine_token = ""
    for token in tokens:
        if token in special or p_r.match(token) is not None or k_r.match(token) is not None:
            refined_tokens.append(token)
        else:
            if refine_token == "":
                if token == ")":
                    refined_tokens.append(token)
                else:
                    refine_token = token
            else:
                refine_token = refine_token + token
                if token == ")":
                    refined_tokens.append(refine_token)
                    refine_token = ""

    return refined_tokens

if __name__ == "__main__":
	drs = "DRS( THING( X1 ) march( E1 ) THEME( E1 X1 ) house( X2 ) parliament( X3 ) of( X2 X3 ) from( E1 X2 ) rally( X4 ) to( E1 X4 ) hyde( X5 ) EQ( X6 X5 ) park( X6 ) in( E1 X6 ) )"
	height = 5000
	width = 5000
	img = figure(height,width,refine(drs.split()))
	if img is None:
		print ("Failed to construct an image!")
	else:
		cv2.imwrite("tree.png",img)
