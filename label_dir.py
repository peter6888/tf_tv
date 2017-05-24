import tensorflow as tf
import numpy as np

# change this as you see fit
# image_path = sys.argv[1]

# Read in the image_data
# image_data = tf.gfile.FastGFile(image_path, 'rb').read()
import os
import shutil
from os import listdir
from os import mkdir
from os.path import isfile, isdir, join

varPath = 'D:\\YouTube\\0090'
modelPath = 'C:\\tensorflow_tv\\tf_tv\YouTube_Model\\tf_files'
#
#sess = None#
#softmax_tensor = None
#destDir = "scanned"
def images_predictions(imagePath, binarySearchType=None, labels="retrained_labels.txt", graph="retrained_graph.pb"):
    imgFiles    = [f for f in listdir(imagePath) if isfile(join(imagePath, f))]
    labels_file = join(modelPath, labels)
    graph_file  = join(modelPath, graph)
    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile(labels_file)]

    ret = []
    

    # Unpersists graph from file
    with tf.gfile.FastGFile(graph_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
    sess = tf.Session()

    # tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

    if binarySearchType:
        return binarySearch(binarySearchType, imagePath, imgFiles, ret, sess, softmax_tensor)
    for imageFile in imgFiles:
        f_name, ext = os.path.splitext(imageFile)
        if ext != '.jpg' and ext != '.JPG':
            print('skip file:' + imageFile)
            continue
        image_data = tf.gfile.FastGFile(join(imagePath,imageFile), 'rb').read()

        print(join(imagePath,imageFile))
        predictions = sess.run(softmax_tensor, \
                               {'DecodeJpeg/contents:0': image_data})

        ret.append((join(imagePath,imageFile), predictions))

    return ret


def binarySearch(binarySearchType, imagePath, imgFiles, ret, sess, softmax_tensor):
    type_ord = [4, 0, 1, 3, 2]
    target_index = type_ord.index(binarySearchType)
    s, e = 0, len(imgFiles) - 1
    if e < 400:
        return None
    while (s < e):
        s_f_name, s_ext = os.path.splitext(imgFiles[s])
        while s_ext != '.jpg' and s_ext != '.JPG' and s < e:
            s += 1
            s_f_name, s_ext = os.path.splitext(imgFiles[s])

        e_f_name, e_ext = os.path.splitext(imgFiles[e])
        while e_ext != '.jpg' and e_ext != '.JPG' and s < e:
            e -= 1
            e_f_name, e_ext = os.path.splitext(imgFiles[e])

        if s >= e:
            return None

        m = (s + e) // 2
        m_f_name, m_ext = os.path.splitext(imgFiles[m])
        if m_ext != '.jpg' and m_ext != '.JPG':
            s = m
            continue

        image_data = tf.gfile.FastGFile(join(imagePath, imgFiles[m]), 'rb').read()
        m_type = label_image(sess, softmax_tensor, image_data)
        if m_type == binarySearchType:
            return join(imagePath, imgFiles[m])
        m_index = type_ord.index(m_type)
        print(m_index, m_type, imgFiles[m])
        if m_index < target_index:
            s = m + 1
        else:  # inf m_index > target_index
            e = m - 1
    return ret


def label_image(sess, softmax_tensor, image_data):
    predictions = sess.run(softmax_tensor, \
                           {'DecodeJpeg/contents:0': image_data})
    return np.argmax(predictions[0])

def pick_one_by_subfolder(rootFolder, targetType=3, moveto='D:\\TrainingData\\TextLoaded'):
    subfolders = [join(rootFolder,f) for f in listdir(rootFolder) if isdir(join(rootFolder,f))]
    labels = "retrained_labels.txt"
    graph = "retrained_graph.pb"
    labels_file = join(modelPath, labels)
    graph_file  = join(modelPath, graph)
        # Unpersists graph from file
    with tf.gfile.FastGFile(graph_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
    sess = tf.Session()

    # tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

    for sf in subfolders:
        print(sf)
        ret = []
        imgFiles    = [f for f in listdir(sf) if isfile(join(sf, f))]
        v = binarySearch(3, sf, imgFiles, ret, sess, softmax_tensor)
        print(v)

#images_predictions(varPath)
