
class Model():

    def __init__(self, dataset, task, parameters):
        pass

    # Train the model.

    # Evaluate the model.

    # Load a user model.

    # Load a user model from Pytorch.

    # Load a user model from Tensorflow.

    # Load a preset Pytorch model from hub.

    # Run LazyPredict or LazyRegression and return the model with the best performance. 

    # Save a trained model.

    # Initialize the experiment logging information.

    # Return the LazyPredict/Regressor model table in a file.

    # def init_experiment(config):
    #     dataset = config['dataset']
    #     timestamp = time.strftime("%Y-%m-%d_%H-%M")
    #     dir = "./experiments/{}_{}/".format(
    #         dataset, timestamp)

    #     if not os.path.exists(dir):
    #         os.makedirs(dir)
    #         os.makedirs(dir + '/plots/')
    #     return dir


