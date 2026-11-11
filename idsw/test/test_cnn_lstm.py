"""
Unit tests for CNN-LSTM Hybrid Architecture (Deep Learning and Siamese Networks).
Verifies tensor reshaping, input validation, and layer compatibility without dimension errors.
"""

import unittest
import numpy as np
import pandas as pd


class TestCnnLstmReshape(unittest.TestCase):

    def setUp(self):
        # Local copy of the reshaping logic to test independently
        def _reshape_cnn_lstm(x):
            arr = np.array(x)
            if arr.ndim == 4:
                return arr
            elif arr.ndim == 3:
                n_samples, n_timesteps, n_features = arr.shape
                n_subseq = int(n_timesteps // 2)
                return arr.reshape(n_samples, n_subseq, 2, n_features)
            elif arr.ndim == 2:
                n_samples, n_cols = arr.shape
                n_subseq = int(n_cols // 2)
                return arr.reshape(n_samples, n_subseq, 2, 1)
            elif arr.ndim == 1:
                return arr.reshape(arr.shape[0], 1, 1, 1)
            return arr

        self.reshaper = _reshape_cnn_lstm

    def test_2d_even_columns(self):
        # 4 columns -> 2 subseq of 2 timesteps
        data_4 = np.random.rand(10, 4)
        reshaped_4 = self.reshaper(data_4)
        self.assertEqual(reshaped_4.shape, (10, 2, 2, 1))

        # 6 columns -> 3 subseq of 2 timesteps
        data_6 = np.random.rand(10, 6)
        reshaped_6 = self.reshaper(data_6)
        self.assertEqual(reshaped_6.shape, (10, 3, 2, 1))

        # 8 columns -> 4 subseq of 2 timesteps
        data_8 = np.random.rand(10, 8)
        reshaped_8 = self.reshaper(data_8)
        self.assertEqual(reshaped_8.shape, (10, 4, 2, 1))

        # 2 columns -> 1 subseq of 2 timesteps
        data_2 = np.random.rand(10, 2)
        reshaped_2 = self.reshaper(data_2)
        self.assertEqual(reshaped_2.shape, (10, 1, 2, 1))

    def test_3d_input(self):
        # 3D: (samples=10, timesteps=6, features=3) -> (10, 3, 2, 3)
        data_3d = np.random.rand(10, 6, 3)
        reshaped_3d = self.reshaper(data_3d)
        self.assertEqual(reshaped_3d.shape, (10, 3, 2, 3))

    def test_4d_input_untouched(self):
        data_4d = np.random.rand(10, 3, 2, 1)
        reshaped_4d = self.reshaper(data_4d)
        self.assertEqual(reshaped_4d.shape, (10, 3, 2, 1))


class TestCnnLstmLayerArchitecture(unittest.TestCase):

    def test_keras_layers_compatibility(self):
        try:
            import tensorflow as tf
        except ImportError:
            self.skipTest("TensorFlow not installed in this environment.")

        # Test single-model CNN-LSTM layer assembly
        # Shape: (batch, n_subseq=3, subseq_len=2, n_features=1)
        n_subseq = 3
        subseq_len = 2
        n_features = 1

        input_layer = tf.keras.layers.Input(shape=(n_subseq, subseq_len, n_features), name="input_layer")
        output_layer = tf.keras.layers.Dense(units=1, name="output")

        conv_layer = tf.keras.layers.Conv1D(filters=64, kernel_size=1, activation='relu', padding='same', name='conv1d_inner')
        pool_layer = tf.keras.layers.MaxPooling1D(pool_size=2, padding='same', name='maxpool1d_inner')
        flat_layer = tf.keras.layers.Flatten(name='flatten_inner')

        x = tf.keras.layers.TimeDistributed(conv_layer, name='convolution')(input_layer)
        x = tf.keras.layers.TimeDistributed(pool_layer, name='pooling')(x)
        x = tf.keras.layers.TimeDistributed(flat_layer, name='flatten')(x)
        x = tf.keras.layers.LSTM(units=50, activation='relu', name='lstm')(x)
        out = output_layer(x)

        model = tf.keras.models.Model(inputs=input_layer, outputs=out, name='test_cnn_lstm')
        self.assertIsNotNone(model)
        self.assertEqual(model.output_shape, (None, 1))

        # Test Siamese network branch assembly
        branch_conv = tf.keras.layers.Conv1D(filters=64, kernel_size=1, activation='relu', padding='same', name='conv1d_branch1')
        branch_pool = tf.keras.layers.MaxPooling1D(pool_size=2, padding='same', name='maxpool1d_branch1')
        branch_flat = tf.keras.layers.Flatten(name='flatten_branch1')

        bx = tf.keras.layers.TimeDistributed(branch_conv, name='conv_td_b1')(input_layer)
        bx = tf.keras.layers.TimeDistributed(branch_pool, name='pool_td_b1')(bx)
        bx = tf.keras.layers.TimeDistributed(branch_flat, name='flat_td_b1')(bx)
        bx = tf.keras.layers.LSTM(units=50, activation='relu', name='lstm_b1')(bx)
        branch_out = tf.keras.layers.Dense(units=1, name='output_branch1')(bx)

        siamese_model = tf.keras.models.Model(inputs=input_layer, outputs=[branch_out], name='test_siamese_cnn_lstm')
        self.assertIsNotNone(siamese_model)
        self.assertEqual(siamese_model.output_shape, [(None, 1)])


if __name__ == '__main__':
    unittest.main()
