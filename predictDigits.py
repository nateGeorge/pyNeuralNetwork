#from LogisticRegression.logisticRegression import *
from LogisticRegression.logisticRegressionGPU import *
#import Training.training as training
import random
import matplotlib.pyplot as plt
from datasets.digits import *
from Logger.graphLogger import *
from Logger.consoleLogger import *
from Logger.compositeLogger import *
#from Training.teacher import *
from Training.teacherGPU import *

import numpy as np
import gnumpy as gpu

if __name__ == '__main__':
   training_set_X, training_set_Y = load_digits('/home/dana/Research/DeepLearning/datasets/data/digits_train.txt')
   test_set_X, test_set_Y = load_digits('/home/dana/Research/DeepLearning/datasets/data/digits_test.txt')

   training_set_X = np.array(training_set_X)
   training_set_Y = np.array(training_set_Y)
   test_set_X = np.array(test_set_X)
   test_set_Y = np.array(test_set_Y)

   training_set_X = gpu.garray(training_set_X)
   training_set_Y = gpu.garray(training_set_Y)
   test_set_X = gpu.garray(test_set_X)
   test_set_Y = gpu.garray(test_set_Y)


   # How many variables?
   numVariables = 196 

   # Create the model
   LR = LogisticRegressionModel(numVariables, 10, SOFTMAX)
   LR.randomize_weights()

#   graphLogger = GraphLogger(LR, (training_set_X, training_set_Y), (test_set_X, test_set_Y))
   consoleLogger = ConsoleLogger(LR, (training_set_X, training_set_Y), (test_set_X, test_set_Y))
   logger = CompositeLogger()
#   logger.add_logger(graphLogger)
#   logger.add_logger(consoleLogger)

   # Train the model
   teacher = Teacher(LR, logger)
   teacher.add_weight_update(0.9, gradient_descent)
   teacher.add_weight_update(0.1, momentum)
   teacher.add_weight_update(0.001, weight_decay)
   teacher.train_batch(training_set_X, training_set_Y, stopping_criteria)

   # Output the final results
   logger.log_results()