import tensorflow as tf
import sys

# change this as you see fit
# image_path = sys.argv[1]

# Read in the image_data
# image_data = tf.gfile.FastGFile(image_path, 'rb').read()
import os
import shutil
from os import listdir
from os import mkdir
from os.path import isfile, join

varPath = 'D:\\ML\\l2\\'
#destDir = "scanned"
def images_predictions(imagePath, labels_file="D:\\ML\\tf_tv\\tf_files\\retrained_labels.txt", graph_file="D:\\ML\\tf_tv\\tf_files\\retrained_graph.pb"):
    imgFiles = [f for f in listdir(imagePath) if isfile(join(imagePath, f))]

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile(labels_file)]

    ret = []
    # Unpersists graph from file
    with tf.gfile.FastGFile(graph_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        for imageFile in imgFiles:
            f_name, ext = os.path.splitext(imageFile)
            if ext != '.jpg' and ext != '.JPG':
                print('skip file:' + imageFile)
                continue
            image_data = tf.gfile.FastGFile(join(imagePath,imageFile), 'rb').read()

            print(join(imagePath,imageFile))
            predictions = sess.run(softmax_tensor, \
                                   {'DecodeJpeg/contents:0': image_data})

            ret.append((imageFile, predictions))

    return ret

#images_predictions(varPath)
