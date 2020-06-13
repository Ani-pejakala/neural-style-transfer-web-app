import imutils
import cv2
import os
import time

UPLOAD_PATH = 'static/uploads/images/'
MODEL_PATH = 'static/models/'
STYLE_PATH = 'static/uploads/style_images/'
MAX_WIDTH=500
MAX_HEIGHT=600

def forward_pass(model_name, image_name, style):
    filesToRemove = [os.path.join(STYLE_PATH, f) for f in os.listdir(STYLE_PATH)]
    for f in filesToRemove:
        os.remove(f)
    model = cv2.dnn.readNetFromTorch(MODEL_PATH + model_name)
    image = cv2.imread(UPLOAD_PATH + image_name)

    if image.shape[1] > MAX_WIDTH:
        image = imutils.resize(image, width=MAX_WIDTH)
    if image.shape[0] > MAX_HEIGHT:
        image = imutils.resize(image, height=MAX_HEIGHT)
    print(image.shape)
    (h, w) = image.shape[:2]

    blob_image = cv2.dnn.blobFromImage(image, 1.0, size=(w, h), mean=(103.939, 116.779, 123.680), swapRB=False,
                                       crop=False)

    model.setInput(blob_image)
    start = time.time()
    output = model.forward()
    end = time.time()
    print(end-start)
    output = output.reshape(3, output.shape[2], output.shape[3])
    output[0] += 103.939
    output[1] += 116.779
    output[2] += 123.680
    # output/=255.0
    output = output.transpose(1, 2, 0)
    # cv2.imshow("out",output)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # out=cv2.convertScaleAbs(output, alpha=(255.0))
    filename, file_extension = os.path.splitext(image_name)
    cv2.imwrite(STYLE_PATH + filename +'_'+ style.split('.')[0] + file_extension, output)
    return output
