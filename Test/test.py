from mnist import load_mnist

(x_train,t_train),(x_test,y_test) = load_mnist(flatten = True,normalize = False,one_hot_label = True)
print(x_train.shape)