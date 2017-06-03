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

type_ord = [3, 4, 2, 0, 1] # the loading orders of types [0]->[1]->[2]->[3]->[4]
type_order_name = ['textloaded', 'imageloaded', 'spinloading', 'whitescreen', 'logo']

def binarySearch(binarySearchType, imagePath, imgFiles, sess, softmax_tensor):
    '''
    Use binary search to go through images in folder to get specified image
    
    Arguments:
        binarySearchType: type order is defined in type_ord
        imagePath: the path for the images
        imgFiles: list of image files (without path)
        sess: Tensorflow session
        softmax_tensor: Tensorflow tensor for softmax
        
    Returns:
        None: not found
        (imagefiles, index): the full path filename of located image, the index in the imgFiles
    '''
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
            return (join(imagePath, imgFiles[m]), m)
        m_index = type_ord.index(m_type)
        print(m, type_order_name[m_type], imgFiles[m])
        if m_index < target_index:
            s = m + 1
        else:  # inf m_index > target_index
            e = m - 1
    return None


def label_image(sess, softmax_tensor, image_data):
    predictions = sess.run(softmax_tensor, \
                           {'DecodeJpeg/contents:0': image_data})
    return np.argmax(predictions[0])

def pick_one_by_subfolder(rootFolder, targetType=3, moveto='D:\\TrainingData\\TextLoaded'):
    subfolders = [join(rootFolder,f) for f in listdir(rootFolder) if isdir(join(rootFolder,f))]
    sess, softmax_tensor = get_session_softmaxtensor()

    ret = []
    for sf in subfolders:
        print(sf)
        imgFiles    = [f for f in listdir(sf) if isfile(join(sf, f))]
        v, _ = binarySearch(3, sf, imgFiles, sess, softmax_tensor)
        print(v)
        ret.append(v)

    return ret

def get_session_softmaxtensor():
    labels = "retrained_labels.txt"
    graph = "retrained_graph.pb"
    labels_file = join(modelPath, labels)
    graph_file = join(modelPath, graph)
    # Unpersists graph from file
    with tf.gfile.FastGFile(graph_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
    sess = tf.Session()
    # tf.Session() as sess:
    # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    return sess, softmax_tensor

def get_performance(folder, session, softmax_tensor):
    ret = np.random.randint(200, 300)
    startframe, endframe = 0, 0
    imgFiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    for searchLogoFrame in imgFiles:
        m_f_name, m_ext = os.path.splitext(searchLogoFrame)
        if m_ext != '.jpg' and m_ext != '.JPG':
            continue
        image_data = tf.gfile.FastGFile(join(folder, searchLogoFrame), 'rb').read()
        m_type = label_image(session, softmax_tensor, image_data)
        if type_ord.index(m_type)==1: #The Logo frame
            startframe = get_frame_number(searchLogoFrame)
            print('Logo frame is at {}'.format(startframe))
            break

    if startframe==0:
        return 0 # error get performance

    textLoadedFrame = binarySearch(0, folder, imgFiles, session, softmax_tensor)
    print(textLoadedFrame)
    if textLoadedFrame==None:
        return 0 # error get performance

    _, frame_index = textLoadedFrame
    for i in range(frame_index, len(imgFiles)):
        m_f_name, m_ext = os.path.splitext(imgFiles[i])
        if m_ext != '.jpg' and m_ext != '.JPG':
            continue
        image_data = tf.gfile.FastGFile(join(folder, imgFiles[i]), 'rb').read()
        m_type = label_image(session, softmax_tensor, image_data)
        if type_ord.index(m_type) == 4:  # The ImageLoaded frame
            endframe = get_frame_number(imgFiles[i])
            print('First Image Loaded Frame is {}'.format(endframe))
            break

    ret = endframe - startframe
    print("{} performance is {}".format(folder, ret))
    return ret

'''
19_05_2017_15_08_16_0421.jpg --> 421
'''
def get_frame_number(filename):
    return int(filename[-8:-4])
'''
Meature the performance, based on epsilon and batch size. 
i.e. if the batch's 'batch_loading' in range of loading time ['loading' - 0.1, 'loading' + 0.1]
'''
def meature_performance(rootFolder, epsilon=0.1, batchsize=5, initbatch=10):
    subfolders = [join(rootFolder, f) for f in listdir(rootFolder) if isdir(join(rootFolder, f))]
    sess, softmax_tensor = get_session_softmaxtensor()
    performances = []
    i = 0
    for folder in subfolders:
        perf = get_performance(folder, sess, softmax_tensor)
        if perf==0:
            print('Not able to get performance value for {}'.format(folder))
            continue
        i = i + 1
        performances.append(perf)
        if i >= initbatch:
            if i%batchsize==0:
                current_perf = np.median(performances) / 60.0
                batch_perf = np.median(performances[-5:]) / 60.0
                print('------------------')
                print('--Total Perf:{}------Batch Perf:{}-----'.format(current_perf, batch_perf))
                if np.abs(current_perf-batch_perf) < epsilon:
                    return (current_perf, performances)

def meature_performance_all(rootFolder):
    subfolders = [join(rootFolder, f) for f in listdir(rootFolder) if isdir(join(rootFolder, f))]
    sess, softmax_tensor = get_session_softmaxtensor()
    performances = []
    for i, folder in enumerate(subfolders):
        if i > 2600:
            break
        perf = get_performance(folder, sess, softmax_tensor)
        if perf==0:
            print('Not able to get performance value for {}'.format(folder))
            continue
        performances.append(perf)

    return (np.median(performances) / 60.0, performances)

