import os

import numpy
import h5py
import keras
from keras.datasets import cifar100

from examples import utils


hdf5_file = 'cifar100.hdf5'
batch_size = 32
num_classes = 100


def create_dataset_metadata():
    url = 'http://localhost:8080/api/v1/dataset'

    dataset_meta = {
        "is_public": True,
        "title": "cifar100",
        "description": "Dataset of 50,000 32x32 color training images, labeled over 100 categories, and 10,000 test images.",
        "category": "classification"
    }

    r = utils.post(url, json=dataset_meta)
    print('Create dataset metadata: ', r.status_code, 'data:', r.text)
    
    if r.status_code == 200:
        return r.json()['id']

    raise RuntimeError('Status_code', r.status_code, r.text)


def cifar100_to_hdf5(file_name):
    if os.path.exists(file_name):
        return
    
    (x_train, y_train), (x_test, y_test) = cifar100.load_data()

    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    x_train /= 255
    x_test /= 255

    x = numpy.concatenate((x_train, x_test))
    y = numpy.concatenate((y_train, y_test))

    numpy.random.shuffle(x)
    numpy.random.shuffle(y)

    with h5py.File(file_name, 'w') as f:
        f.create_dataset('x',data=x, compression='gzip')
        f.create_dataset('y',data=y, compression='gzip')


if __name__ == '__main__':
    cifar100_to_hdf5(hdf5_file)
    id = create_dataset_metadata()
    utils.upload(id, hdf5_file)

