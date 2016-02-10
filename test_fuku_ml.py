#encoding=utf8

import os
import unittest
import FukuML.PLA as pla
import FukuML.PocketPLA as pocket
import FukuML.LinearRegression as linear_regression
import FukuML.LogisticRegression as logistic_regression
import FukuML.Utility as utility


class FukuMLTestCase(unittest.TestCase):

    def test_pla_binary_classifier(self):

        #------------------------------------------------------------

        pla_bc = pla.BinaryClassifier()
        pla_bc.load_train_data()
        pla_bc.init_W()
        W = pla_bc.train()

        print("\n訓練得出權重模型：")
        print(W)
        print("W 更新次數：")
        print(pla_bc.tune_times)
        print('-'*70)

        test_data = '0.97681 0.10723 0.64385 0.29556 1'
        prediction = pla_bc.prediction(test_data)
        self.assertEqual(prediction['input_data_y'], prediction['prediction'])

        print("測試資料 x：")
        print(prediction['input_data_x'])
        print("測試資料 y：")
        print(prediction['input_data_y'])
        print("預測結果：")
        print(prediction['prediction'])
        print('-'*70)

        test_data = '0.15654 0.75584 0.01122 0.42598 -1'
        prediction = pla_bc.prediction(test_data)
        self.assertEqual(prediction['input_data_y'], prediction['prediction'])

        print("測試資料 x：")
        print(prediction['input_data_x'])
        print("測試資料 y：")
        print(prediction['input_data_y'])
        print("預測結果：")
        print(prediction['prediction'])
        print('-'*70)

        #------------------------------------------------------------

        print("使用 Linear Regression 加速器：")

        pla_bc = pla.BinaryClassifier()
        pla_bc.load_train_data()
        pla_bc.init_W('linear_regression_accelerator')
        W = pla_bc.train()

        print("\n訓練得出權重模型：")
        print(W)
        print("W 更新次數：")
        print(pla_bc.tune_times)
        print('-'*70)

        test_data = '0.97681 0.10723 0.64385 0.29556 1'
        prediction = pla_bc.prediction(test_data)
        self.assertEqual(prediction['input_data_y'], prediction['prediction'])

        print("測試資料 x：")
        print(prediction['input_data_x'])
        print("測試資料 y：")
        print(prediction['input_data_y'])
        print("預測結果：")
        print(prediction['prediction'])
        print('-'*70)

        #------------------------------------------------------------

        input_train_data_file = os.path.join(os.path.join(os.getcwd(), os.path.dirname(__file__)), 'FukuML/dataset/pla_binary_train.dat')
        pla_bc.load_train_data(input_train_data_file)
        pla_bc.init_W()
        W = pla_bc.train()
        print("測試載入 Custom Dataset")
        print("訓練得出權重模型：")
        print(W)
        print('-'*70)

        #------------------------------------------------------------

        print("使用 Random Cycle：")

        pla_bc.init_W()
        W = pla_bc.train('random')

        print("訓練得出權重模型：")
        print(W)
        print("W 更新次數：")
        print(pla_bc.tune_times)
        print('-'*70)

        test_data = '0.97681 0.10723 0.64385 0.29556 1'
        prediction = pla_bc.prediction(test_data)
        self.assertEqual(prediction['input_data_y'], prediction['prediction'])

        print("測試資料 x：")
        print(prediction['input_data_x'])
        print("測試資料 y：")
        print(prediction['input_data_y'])
        print("預測結果：")
        print(prediction['prediction'])
        print('-'*70)

        #------------------------------------------------------------

        print("使用 Random Cycle alpha=0.5 step correction：")

        pla_bc.init_W()
        W = pla_bc.train('random', 0.5)

        print("訓練得出權重模型：")
        print(W)
        print("W 更新次數：")
        print(pla_bc.tune_times)
        print('-'*70)

        test_data = '0.97681 0.10723 0.64385 0.29556 1'
        prediction = pla_bc.prediction(test_data)
        self.assertEqual(prediction['input_data_y'], prediction['prediction'])

        print("測試資料 x：")
        print(prediction['input_data_x'])
        print("測試資料 y：")
        print(prediction['input_data_y'])
        print("預測結果：")
        print(prediction['prediction'])
        print('-'*70)

        serialized_pla_bc = utility.Serializer.serialize(pla_bc)
        deserialized_pla_bc = utility.Serializer.deserialize(serialized_pla_bc)
        self.assertTrue((pla_bc.train_X == deserialized_pla_bc.train_X).all())

    def test_pocket_pla_binary_classifier(self):

        #------------------------------------------------------------

        input_train_data_file = os.path.join(os.path.join(os.getcwd(), os.path.dirname(__file__)), 'FukuML/dataset/pocket_pla_binary_train.dat')
        input_test_data_file = os.path.join(os.path.join(os.getcwd(), os.path.dirname(__file__)), 'FukuML/dataset/pocket_pla_binary_test.dat')

        pla_bc = pla.BinaryClassifier()
        pla_bc.load_train_data(input_train_data_file)
        pla_bc.init_W()
        W = pla_bc.train()
        pla_bc.load_test_data(input_test_data_file)

        print("\n訓練得出權重模型：")
        print(W)
        print("W 更新次數：")
        print(pla_bc.tune_times)
        print("Dataset 不是線性可分的，所以要使用 Pocket PLA.")
        print("W 平均錯誤率：")
        print(pla_bc.calculate_avg_error(pla_bc.test_X, pla_bc.test_Y, W))
        print('-'*70)

        #------------------------------------------------------------

        pocket_bc = pocket.BinaryClassifier()
        pocket_bc.load_train_data()
        pocket_bc.init_W()
        W = pocket_bc.train(50)
        pocket_bc.load_test_data()

        print("訓練得出權重模型：")
        print(W)
        print("W 更新次數：")
        print(pocket_bc.tune_times)
        print("W 效果改善次數：")
        print(pocket_bc.put_in_pocket_times)
        print("W 平均錯誤率：")
        print(pocket_bc.calculate_avg_error(pocket_bc.test_X, pocket_bc.test_Y, W))
        print('-'*70)

        test_data = '0.62771 0.11513 0.82235 0.14493 -1'
        prediction = pocket_bc.prediction(test_data)
        self.assertEqual(prediction['input_data_y'], prediction['prediction'])

        print("測試資料 x：")
        print(prediction['input_data_x'])
        print("測試資料 y：")
        print(prediction['input_data_y'])
        print("預測結果：")
        print(prediction['prediction'])
        print('-'*70)

        serialized_pocket_bc = utility.Serializer.serialize(pocket_bc)
        deserialized_pocket_bc = utility.Serializer.deserialize(serialized_pocket_bc)
        self.assertTrue((pocket_bc.train_X == deserialized_pocket_bc.train_X).all())

        #------------------------------------------------------------

        print("使用 Linear Regression 加速器：")

        pocket_bc = pocket.BinaryClassifier()
        pocket_bc.load_train_data()
        pocket_bc.init_W('linear_regression_accelerator')
        W = pocket_bc.train()
        pocket_bc.load_test_data()

        print("訓練得出權重模型：")
        print(W)
        print("W 更新次數：")
        print(pocket_bc.tune_times)
        print("W 效果改善次數：")
        print(pocket_bc.put_in_pocket_times)
        print("W 平均錯誤率：")
        print(pocket_bc.calculate_avg_error(pocket_bc.test_X, pocket_bc.test_Y, W))
        print('-'*70)

    def test_linear_regression(self):

        #------------------------------------------------------------

        linear = linear_regression.LinearRegression()
        linear.load_train_data()
        linear.load_test_data()
        linear.init_W()
        W = linear.train()

        print("\n訓練得出權重模型：")
        print(W)

        test_data = '0.62771 0.11513 0.82235 0.14493 -1'
        prediction = linear.prediction(test_data)

        print("測試資料 x：")
        print(prediction['input_data_x'])
        print("測試資料 y：")
        print(prediction['input_data_y'])
        print("預測結果：")
        print(prediction['prediction'])
        print("錯誤評估：")
        print(linear.error_function(prediction['prediction'], prediction['input_data_y']))
        print("W 平均錯誤值：")
        print(linear.calculate_avg_error(linear.test_X, linear.test_Y, W))
        print('-'*70)

    def test_linear_regression_binary_classifier(self):

        #------------------------------------------------------------

        linear = linear_regression.BinaryClassifier()
        linear.load_train_data()
        linear.load_test_data()
        linear.init_W()
        W = linear.train()

        print("\n訓練得出權重模型：")
        print(W)

        test_data = '0.62771 0.11513 0.82235 0.14493 -1'
        prediction = linear.prediction(test_data)

        self.assertEqual(prediction['input_data_y'], prediction['prediction'])

        print("測試資料 x：")
        print(prediction['input_data_x'])
        print("測試資料 y：")
        print(prediction['input_data_y'])
        print("預測結果：")
        print(prediction['prediction'])
        print("W 平均錯誤率：")
        print(linear.calculate_avg_error(linear.test_X, linear.test_Y, W))
        print('-'*70)

    def test_logistic_regression(self):

        #------------------------------------------------------------

        logistic = logistic_regression.LogisticRegression()
        logistic.load_train_data()
        logistic.load_test_data()
        logistic.init_W()
        W = logistic.train()

        print("\n訓練得出權重模型：")
        print(W)

        test_data = '0.26502 0.5486 0.971 0.19333 0.12207 0.81528 0.46743 0.45889 0.31004 0.3307 0.43078 0.50661 0.57281 0.052715 0.50443 0.78686 0.20099 0.85909 0.26772 0.13751 1'
        prediction = logistic.prediction(test_data)

        print("測試資料 x：")
        print(prediction['input_data_x'])
        print("測試資料 y：")
        print(prediction['input_data_y'])
        print("預測結果：")
        print(prediction['prediction'])
        print("錯誤評估：")
        print(logistic.error_function(prediction['input_data_x'], prediction['input_data_y'], W))
        print("W 平均錯誤值：")
        print(logistic.calculate_avg_error(logistic.test_X, logistic.test_Y, W))
        print('-'*70)

        #------------------------------------------------------------

        print("使用 Linear Regression 加速器：")

        logistic = logistic_regression.LogisticRegression()
        logistic.load_train_data()
        logistic.load_test_data()
        logistic.init_W('linear_regression_accelerator')
        W = logistic.train()

        print("\n訓練得出權重模型：")
        print(W)

        test_data = '0.26502 0.5486 0.971 0.19333 0.12207 0.81528 0.46743 0.45889 0.31004 0.3307 0.43078 0.50661 0.57281 0.052715 0.50443 0.78686 0.20099 0.85909 0.26772 0.13751 1'
        prediction = logistic.prediction(test_data)

        print("測試資料 x：")
        print(prediction['input_data_x'])
        print("測試資料 y：")
        print(prediction['input_data_y'])
        print("預測結果：")
        print(prediction['prediction'])
        print("錯誤評估：")
        print(logistic.error_function(prediction['input_data_x'], prediction['input_data_y'], W))
        print("W 平均錯誤值：")
        print(logistic.calculate_avg_error(logistic.test_X, logistic.test_Y, W))
        print('-'*70)

    def test_logistic_regression_binary_classifier(self):

        #------------------------------------------------------------

        logistic = logistic_regression.BinaryClassifier()
        logistic.load_train_data()
        logistic.load_test_data()
        logistic.init_W()
        W = logistic.train()

        print("\n訓練得出權重模型：")
        print(W)

        test_data = '0.26502 0.5486 0.971 0.19333 0.12207 0.81528 0.46743 0.45889 0.31004 0.3307 0.43078 0.50661 0.57281 0.052715 0.50443 0.78686 0.20099 0.85909 0.26772 0.13751 1'
        prediction = logistic.prediction(test_data)

        self.assertEqual(prediction['input_data_y'], prediction['prediction'])

        print("測試資料 x：")
        print(prediction['input_data_x'])
        print("測試資料 y：")
        print(prediction['input_data_y'])
        print("預測結果：")
        print(prediction['prediction'])
        print("W 平均錯誤率：")
        print(logistic.calculate_avg_error(logistic.test_X, logistic.test_Y, W))
        print('-'*70)

        print("隨機梯度下降：")
        logistic.init_W()
        W = logistic.train(2000, 'stochastic', 0.1)
        print("訓練得出權重模型：")
        print(W)
        print("W 平均錯誤率：")
        print(logistic.calculate_avg_error(logistic.test_X, logistic.test_Y, W))
        print('-'*70)

    def test_logistic_regression_multi_classifier(self):

        #------------------------------------------------------------

        logistic = logistic_regression.MultiClassifier()
        logistic.load_train_data()
        logistic.load_test_data()
        logistic.init_W()
        W = logistic.train()

        print("\n訓練得出權重模型：")
        print(W)

        test_data = '0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 00 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 00 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 00 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 00 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 00 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 00 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 00 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 00 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 00 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 00 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 00 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 00 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 00 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 00 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 00 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 00 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 00 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 00 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 00 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 00 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 00 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 00 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 00 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 00 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 00 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 00 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 00 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 00 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 00 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 00 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 00 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0'
        prediction = logistic.prediction(test_data)

        self.assertEqual(float(prediction['input_data_y']), float(prediction['prediction']))

        print("測試資料 x：")
        print(prediction['input_data_x'])
        print("測試資料 y：")
        print(prediction['input_data_y'])
        print("預測結果：")
        print(prediction['prediction'])
        print("所有類型機率值：")
        print(prediction['prediction_list'])
        print("W 平均錯誤率：")
        print(logistic.calculate_avg_error(logistic.test_X, logistic.test_Y, W))
        print('-'*70)

        print("隨機梯度下降：")
        logistic.init_W()
        W = logistic.train(2000, 'stochastic', 0.126)
        print("訓練得出權重模型：")
        print(W)
        print("W 平均錯誤率：")
        print(logistic.calculate_avg_error(logistic.test_X, logistic.test_Y, W))
        print('-'*70)


if __name__ == '__main__':

    unittest.main(verbosity=2)
