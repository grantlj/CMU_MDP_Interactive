#test the usage of Matlab python interface for MDP interactive train
import mdp_interactive_train

seq_base_path='D:\\Matlab\\ImageProcess\\MDP_Interactive\\MDP_Labeler\\92-2_demo_2_null\\'
input_tracker_filepath='D:\\Matlab\\ImageProcess\\MDP_Interactive\\MDP_Labeler\\train_ALL_tracker.mat'
seq_num=int(326)
iteration=int(1)
my_trainer=mdp_interactive_train.initialize()
number_of_new_samples=my_trainer.MDP_interactive_train(seq_base_path,input_tracker_filepath,seq_num,iteration)
my_trainer.terminate()
pass
