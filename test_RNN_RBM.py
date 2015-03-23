from RNNRBM_GB.RNNRBM import *
import numpy as np

import matplotlib.pyplot as plt

# Simple RNN-RBM with 3 visible, 4 hidden and 2 rnn units
r = RNNRBM(3,10,10)


# Create a sample sequence
#visible = [[0.0, 0.0, 1.0],
#           [0.0, 1.0, 0.0],
#           [1.0, 0.0, 0.0],
#           [1.0, 1.0, 0.0],
#           [1.0, 0.0, 1.0]]

# Create a sample sequence
visible = [[-1.001, -0.805,  1.670],
           [-1.194,  1.757, -0.592],
           [ 1.502, -0.622, -0.765],
           [ 0.539,  0.476, -0.939],
           [ 0.154, -0.805,  0.626]]
visible_sequence = [np.array([v]).transpose() for v in visible]

# How many elements in the sequence?
N = len(visible_sequence)

print "Visible Sequence: "
for i in range(N):
   print i, '-'
   print visible_sequence[i]

print

initial_rnn = np.zeros((10,1))

print "Initial RNN hidden layer: "
print initial_rnn
print


# Does the train_sequence function break?
l = -0.01

ground_truth = np.array(visible)



for i in range(10000):
   print 'Iteration', i
   dWhv, dWuh, dWuv, dWuu, dWvu, dbv, dbh, dbu, du0 = r.train_sequence(visible_sequence, initial_rnn)

   r.update_weights(l*dWhv, l*dWuh, l*dWuv, l*dWuu, l*dWvu, l*dbv, l*dbh, l*dbu)
   initial_rnn = initial_rnn + l*du0

   v_gen = []
   v_guess = np.zeros((3,1))
   prior_rnn = initial_rnn
   for i in range(N):
      v_next = r.generate_visible(prior_rnn, v_guess, 20)
      prior_rnn = r.get_rnn(v_next, prior_rnn)
      v_gen.append(v_next)
      v_guess = v_next

#   for j in range(N):
#      print j, '-', v_gen[j].transpose().tolist()
#      print j, '-',
#      for k in range(3):
#         print "%.2f\t" % v_gen[j][k,0],
#      print

   M = 10 # Number of samples to figure out statistics
   # Get some samples to figure out the mean and std-dev of reconstructed signals
   samples = [np.zeros((3,M)), np.zeros((3,M)), np.zeros((3,M)), np.zeros((3,M)), np.zeros((3,M))]
   for i in range(M):
      prior_rnn = initial_rnn
      v_guess = np.zeros((3,1))
      for j in range(N):
         v_next = r.generate_visible(prior_rnn, v_guess, 20)
         prior_rnn = r.get_rnn(v_next, prior_rnn)
         v_guess = np.array([visible[j]]).transpose()
         samples[j][0,i]=v_next[0,0]
         samples[j][1,i]=v_next[1,0]
         samples[j][2,i]=v_next[2,0]
       
   means = [np.mean(samples[0],1), np.mean(samples[1],1), np.mean(samples[2],1), np.mean(samples[3],1), np.mean(samples[4],1)]
   stds = [np.std(samples[0],1), np.std(samples[1],1), np.std(samples[2],1), np.std(samples[3],1), np.std(samples[4],1)]

   mean_0 = [means[0][0], means[1][0], means[2][0], means[3][0], means[4][0]]
   mean_1 = [means[0][1], means[1][1], means[2][1], means[3][1], means[4][1]]
   mean_2 = [means[0][2], means[1][2], means[2][2], means[3][2], means[4][2]]

   std_0 = [stds[0][0], stds[1][0], stds[2][0], stds[3][0], stds[4][0]]
   std_1 = [stds[0][1], stds[1][1], stds[2][1], stds[3][1], stds[4][1]]
   std_2 = [stds[0][2], stds[1][2], stds[2][2], stds[3][2], stds[4][2]]

   hi_0 = [mean_0[0] + std_0[0], mean_0[1] + std_0[1], mean_0[2] + std_0[2], mean_0[3] + std_0[3], mean_0[4] + std_0[4]]
   hi_1 = [mean_1[0] + std_1[0], mean_1[1] + std_1[1], mean_1[2] + std_1[2], mean_1[3] + std_1[3], mean_1[4] + std_1[4]]
   hi_2 = [mean_2[0] + std_2[0], mean_2[1] + std_2[1], mean_2[2] + std_2[2], mean_2[3] + std_2[3], mean_2[4] + std_2[4]]

   lo_0 = [mean_0[0] - std_0[0], mean_0[1] - std_0[1], mean_0[2] - std_0[2], mean_0[3] - std_0[3], mean_0[4] - std_0[4]]
   lo_1 = [mean_1[0] - std_1[0], mean_1[1] - std_1[1], mean_1[2] - std_1[2], mean_1[3] - std_1[3], mean_1[4] - std_1[4]]
   lo_2 = [mean_2[0] - std_2[0], mean_2[1] - std_2[1], mean_2[2] - std_2[2], mean_2[3] - std_2[3], mean_2[4] - std_2[4]]

   f = plt.figure(1)
   plt.hold(False)
   plt.plot([1,2,3,4,5], ground_truth[:,0], '-r', linewidth=2)
   plt.hold(True)
   plt.plot([1,2,3,4,5], ground_truth[:,1], '-g', linewidth=2)
   plt.plot([1,2,3,4,5], ground_truth[:,2], '-b', linewidth=2)
   plt.plot([1,2,3,4,5], mean_0, '-r')
   plt.plot([1,2,3,4,5], mean_1, '-g')
   plt.plot([1,2,3,4,5], mean_2, '-b')
  
   plt.plot([1,2,3,4,5], hi_0, '--r')
   plt.plot([1,2,3,4,5], hi_1, '--g')
   plt.plot([1,2,3,4,5], hi_2, '--b')

   plt.plot([1,2,3,4,5], lo_0, '--r')
   plt.plot([1,2,3,4,5], lo_1, '--g')
   plt.plot([1,2,3,4,5], lo_2, '--b')

   plt.draw()
   f.show()


   err = 0.0
   for i in range(N):
      err = err + (mean_0[i] - visible[i][0])**2
      err = err + (mean_1[i] - visible[i][1])**2
      err = err + (mean_2[i] - visible[i][2])**2

   print 'RMS error = ', err

#   if i%1000 == 0:
#      l = l + 0.05
print

print 'Whv'
print r.Whv
print

print 'Wuh'
print r.Wuh
print

print 'Wuv'
print r.Wuv
print

print 'Wuu'
print r.Wuu
print

print 'Wvu'
print r.Wvu
print

print 'bias visible -',
print r.bias_visible.transpose().tolist()
print

print 'bias hidden -',
print r.bias_hidden.transpose().tolist()
print

print 'bias rnn -',
print r.bias_rnn.transpose().tolist()
print
