# Training
python D:\ML\tensorflow-master\tensorflow\examples\image_retraining\retrain.py --bottleneck_dir=tf_files\bottlenecks --how_many_training_steps 3 --model_dir=YouTube_Model\tf_files\inception --output_graph=YouTube_Model\tf_files\retrained_graph.pb --output_labels=YouTube_Model\tf_files\retrained_labels.txt --image_dir D:\TrainingData
#
#import label_dir as ld
#v = ld.images_predictions('D:\\ML\\l2')
for ss in v:
   print(ss[0][-8:-4], ss[1][0][0], ss[1][0][1], ss[1][0][2], ss[1][0][3])
