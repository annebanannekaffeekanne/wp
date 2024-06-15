from shared import app
import methods
from flask import Flask, render_template, request, redirect, url_for, abort
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

page_size = 50
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/patients")
def patient_list():
    page = request.args.get("page", 0, type=int)
    patients = methods.get_data(page)
    last_page = methods.get_last_page()
    return render_template("patient_list.html", patients=patients, page=page, last_page=last_page)

@app.route("/patients/<int:patient_id>")
def patient_detail(patient_id):
    patient = methods.get_patient((patient_id))
    return render_template("patient_detail.html", patient=patient)

@app.route("/delete/<int:patient_id>")
def delete_patient(patient_id):
    if methods.delete_patient(patient_id):
        return redirect(url_for("patient_list"))
    else:
        abort(404)

@app.route("/edit/<int:patient_id>", methods=["GET", "POST"])
def edit_patient(patient_id):
    if request.method == "POST":
        updated_data = request.form.to_dict()
        updated_data["ID"] = patient_id
        methods.update(updated_data)
        return redirect(url_for("patient_list"))
    else:
        patient = methods.get_patient(patient_id)
        return render_template("edit_patient.html", patient=patient)



@app.route("/select_features")
def select_features():
    features = methods.get_features()
    return render_template("select_features.html", features=features)

@app.route("/submit_features", methods=["POST"])
def submit_features():
    selected_features = request.form.getlist("selected_features")
    selected_feature_df = methods.select_features(selected_features)
    return redirect(url_for("show_histograms", selected_features=",".join(selected_features)))

@app.route("/show_histograms")
def show_histograms():
    selected_features = request.args.get("selected_features").split(",")
    selected_feature_df = methods.select_features(selected_features)
    plots = methods.plot_histograms(selected_feature_df, selected_features)
    return render_template("visualize_features.html", plots=plots)

@app.route("/data_analysis")
def data_analysis():
    chart_url = methods.plot_piechart()
    return render_template("data_analysis.html", chart_url=chart_url)