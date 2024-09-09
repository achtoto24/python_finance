import requests
import hashlib
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

url = 'https://lumiere-a.akamaihd.net/v1/images/501st-stormtroopers-main_525e6786.jpeg?region=0%2C0%2C1281%2C720'
r = requests.get(url, stream = True).raw


img = Image.open(r)
img.show()
img.save('501st.jpg')
print(img.get_format_mimetype)

BUF_SIZE = 1024
with open('501st.jpg', 'rb') as sf, open('copy_501st.jpg', 'wb') as df :
    while True :
        data = sf.read(BUF_SIZE)
        if not data :
            break
        df.write(data)

sha_501st = hashlib.sha256()
sha_copy_501st = hashlib.sha256()

with open('501st.jpg', 'rb') as sf, open('copy_501st.jpg', 'rb') as df :
    sha_501st.update(sf.read())
    sha_copy_501st.update(df.read())

#print('{}'.format(sha_501st.hexdigest()))
#print('{}'.format(sha_copy_501st.hexdigest()))
#
#dst_img = mpimg.imread('501st.jpg')
#print(dst_img)
#print("=======================================")
#pseudo_img = dst_img [:,:,0]    #second dimension is printed
#print(pseudo_img)

plt.suptitle('Image Processing', fontsize = 18)
plt.subplot(1, 2, 1)    #fist row : second column : first image
plt.title('Original Image')
plt.imshow(mpimg.imread('501st.jpg'))

plt.subplot(122)    #first row : second column : second image without comma
plt.title('Pseudocolor Image')
#dst_img = mpimg.imread('copy_501st.jpg')
#pseudo_img = dst_img [:, :, 0]
#plt.imshow(pseudo_img)
plt.imshow(mpimg.imread('copy_501st.jpg')[:,:,0])
plt.show()

