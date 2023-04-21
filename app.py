from flask import Flask, render_template, request, redirect, url_for
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from io import BytesIO,StringIO
import base64
import control
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bode_plot_input')
def bode_plot_form():
    return render_template('bode_plot_input.html')


@app.route('/bode_plot', methods=['POST'])
def bode_plot():
    num = list(map(float, request.form['num'].split(',')))
    den = list(map(float, request.form['den'].split(',')))
    sys = signal.TransferFunction(num, den)
    w, mag, phase = signal.bode(sys)
    transfer_fn = control.tf(num,den)
    gm, pm, pcf,gcf = control.margin(transfer_fn)
    
    plt.figure()
    plt.semilogx(w, mag)
    plt.figure()
    plt.semilogx(w, phase)
    
    # Save plot to a buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Encode plot to base64
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return render_template('bode_plot.html', plot_url=plot_url, gm=gm, pm=pm, pcf=pcf, gcf=gcf)

@app.route("/nyquist_plot", methods=["GET", "POST"])
def nyquist_plot():
    if request.method == "POST":
        numerator = np.array(list(map(int, request.form['numerator'].split(','))))
        denominator = np.array(list(map(int, request.form['denominator'].split(','))))
        sys = control.tf(numerator, denominator)
        plt.figure()
        plt.grid(True)
        plt.title('Nyquist Plot')
        plt.xlabel('Real Axis')
        plt.ylabel('Imaginary Axis')
        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        control.nyquist_plot(sys)
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
        return render_template('nyquist_plot.html', plot_url=plot_url)
    return render_template("nyquist_input.html")


@app.route("/root_locus", methods=["GET", "POST"])
def root_locus():
    if request.method == "POST":
        numerator = np.array(list(map(int, request.form['numerator'].split(','))))
        denominator = np.array(list(map(int, request.form['denominator'].split(','))))
        sys = control.tf(numerator, denominator)
        plt.figure()
        plt.grid(True)
        plt.title('Root Locus Plot')
        plt.xlabel('Real Axis')
        plt.ylabel('Imaginary Axis')
        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        rlocus = control.root_locus(sys, kvect=np.linspace(0, 10, 1000))
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
        return render_template('root_locus.html', plot_url=plot_url)
    return render_template("root_locus_input.html")


if __name__ == '__main__':
    app.run()
