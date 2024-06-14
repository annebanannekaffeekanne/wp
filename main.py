from flask import Flask, render_template, redirect, url_for
from methods.relevant_features import *
from methods.data_analysis import *
from methods.visualization import *
from methods.hyperparameter_tuning import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate')
def generate():
    return render_template('generate.html')


@app.route('/results')
def results():
    return render_template('results.html')


@app.route('/data_analysis')
def data_analysis():
    return render_template('data_analysis.html')


@app.route('/generate_analysis', methods=['POST'])
def generate_analysis():
    try:
        # 0. Load dataframe
        train_df = pd.read_csv(
            '/Users/anne/PycharmProjects/Semester4/machine_learning/semester_project/breast-cancer_train.csv')

        # 1. Data Analysis
        norm_df = load_and_normalize_data(
            '/Users/anne/PycharmProjects/Semester4/machine_learning/semester_project/breast-cancer_train.csv')
        norm_train_df, norm_valid_df = split_data(norm_df, validation_size=0.33)

        max_val, min_val, mean_val = get_statistics(train_df)
        print(f"Max: {max_val}, Min: {min_val}, Mean: {mean_val}")

        # 2. Select relevant features and create new dataframes
        relevant_features = get_relevant_features(norm_train_df, threshold=45)
        relevant_feature_df = get_relevant_feature_dfs(norm_train_df, relevant_features)
        relevant_valid_feature_df = get_relevant_feature_dfs(norm_valid_df, relevant_features)

        X, y = separate_data(relevant_feature_df)
        X_val, y_val = separate_data(relevant_valid_feature_df)

        # 3. Tune hyperparameter (learning rate)
        best_eta, best_epoch, accuracy = tune_eta_and_epochs(X, y, X_val, y_val)

        # 4. Apply algorithm to train the model with best learning rate
        w1, w0, error_list = gradient_descent(X, y, best_eta, best_epoch)

        y_val_pred = predict(X_val, w1, w0)
        y_val_pred_class = (np.where(y_val_pred >= 0, 1, -1))
        val_error = error_function(X_val, y_val, w1, w0)
        val_accuracy = np.mean(y_val_pred_class == y_val)

        print(f"Lowest error of validation data: {val_error}")

        result_df = pd.DataFrame({"actual_diagnosis": y_val, "predicted_diagnosis": y_val_pred_class})

        # 5. Visualize relevant results
        generate_pie_chart(norm_df)
        generate_heatmaps(norm_train_df, relevant_feature_df)
        generate_heatmaps(relevant_feature_df, relevant_valid_feature_df)
        plot_relevant_features(relevant_feature_df, relevant_features)
        generate_error_plot(error_list)
        generate_bar_chart(result_df)

        # 6. Apply on test data
        test_df = pd.read_csv(
            '/Users/anne/PycharmProjects/Semester4/machine_learning/semester_project/breast-cancer_test.csv')
        norm_test_df = load_and_normalize_data(
            '/Users/anne/PycharmProjects/Semester4/machine_learning/semester_project/breast-cancer_test.csv')

        max_val, min_val, mean_val = get_statistics(test_df)
        print(f"Max: {max_val}, Min: {min_val}, Mean: {mean_val}")

        relevant_test_feature_df = get_relevant_feature_dfs(norm_test_df, relevant_features)
        X_test, y_test = separate_data(relevant_test_feature_df)

        y_test_pred = predict(X_test, w1, w0)
        y_test_pred_class = (np.where(y_test_pred >= 0, 1, -1))
        test_error = error_function(X_test, y_test, w1, w0)
        test_accuracy = np.mean(y_test_pred_class == y_test)

        print(f"Lowest error of the test data: {test_error}.")
        print(f"Accuracy of the test data: {test_accuracy}.")

        test_result_df = pd.DataFrame({"actual_diagnosis": y_test, "predicted_diagnosis": y_test_pred_class})

        generate_pie_chart(norm_test_df)
        generate_bar_chart(test_result_df)

        return redirect(url_for('results'))

    except Exception as e:
        print(f"An error occurred: {e}")
        return redirect(url_for('data_analysis'))


if __name__ == '__main__':
    app.run(debug=True)
