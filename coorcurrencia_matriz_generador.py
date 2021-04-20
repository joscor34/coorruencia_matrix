import cv2
import math

#Define the maximum number of gray levels
gray_level = 16

def maxGrayLevel(img):
    max_gray_level=0
    (height,width)=img.shape
    print ("The height and width of the image are: height, width",height,width)
    for y in range(height):
        for x in range(width):
            if img[y][x] > max_gray_level:
                max_gray_level = img[y][x]
    print("max_gray_level:",max_gray_level)
    return max_gray_level+1

def getGlcm(input,d_x,d_y):
    srcdata=input.copy()
    ret=[[0.0 for i in range(gray_level)] for j in range(gray_level)]
    (height,width) = input.shape

    max_gray_level=maxGrayLevel(input)
    #If the number of gray levels is greater than gray_level, reduce the gray level of the image to gray_level and reduce the size of the gray level co-occurrence matrix
    if max_gray_level > gray_level:
        for j in range(height):
            for i in range(width):
                srcdata[j][i] = srcdata[j][i]*gray_level / max_gray_level

    for j in range(height-d_y):
        for i in range(width-d_x):
            rows = srcdata[j][i]
            cols = srcdata[j + d_y][i+d_x]
            ret[rows][cols]+=1.0

    for i in range(gray_level):
        for j in range(gray_level):
            ret[i][j]/=float(height*width)

    return ret

def feature_computer(p):
    #con: Contrast reflects the sharpness of the image and the depth of the grooves in the texture. The sharper the texture, the greater the contrast, the greater the contrast.
    #eng: Entropy (Entropy, ENT) measures the randomness of the amount of information contained in an image and expresses the complexity of the image. When all the values ​​in the co-occurrence matrix are equal or the pixel values ​​show the greatest randomness, the entropy is the largest.
    #agm: Angle second moment (energy), a measure of the uniformity of the image gray distribution and the thickness of the texture. When the image texture is uniform and regular, the energy value is large; on the contrary, the element values ​​of the gray-level co-occurrence matrix are similar, and the energy value is small.
    #idm: The inverse difference matrix is ​​also called the inverse variance, which reflects the clarity and regularity of the texture. The texture is clear, regular, easy to describe, and has a larger value.
    Con=0.0
    Eng=0.0
    Asm=0.0
    Idm=0.0
    for i in range(gray_level):
        for j in range(gray_level):
            Con+=(i-j)*(i-j)*p[i][j]
            Asm+=p[i][j]*p[i][j]
            Idm+=p[i][j]/(1+(i-j)*(i-j))
            if p[i][j]>0.0:
                Eng+=p[i][j]*math.log(p[i][j])
    return Asm,Con,-Eng,Idm

def test(image_name):
    img = cv2.imread(image_name)
    try:
        img_shape=img.shape
    except:
        print ('imread error')
        return

    #If you use ‘/’ here, an error will be reported TypeError: integer argument expected, got float
    #In fact, the main error is because the parameter in cv2.resize is required to be an integer
    img=cv2.resize(img,(img_shape[1]//2,img_shape[0]//2),interpolation=cv2.INTER_CUBIC)

    img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    glcm_0=getGlcm(img_gray, 1,0)
    #glcm_1=getGlcm(src_gray, 0,1)
    #glcm_2=getGlcm(src_gray, 1,1)
    #glcm_3=getGlcm(src_gray, -1,1)
    print(glcm_0)

    asm,con,eng,idm=feature_computer(glcm_0)

    return [asm,con,eng,idm]

if __name__=='__main__':
    # Aquí cambiar la ruta donde se guarde la imagen
    result = test("/Users/josecor34/Documents/code/python/descarga.png")
    print(result)

