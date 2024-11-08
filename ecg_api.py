from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import wfdb
import os
import json
from typing import Dict, List
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import seaborn as sns
from io import BytesIO

app = FastAPI()

class ECGPlotter:
    def __init__(self, record, num_parts=12, samples_per_part=5000):
        self.record = record
        self.total_samples = record.p_signal.shape[0]
        self.num_parts = num_parts
        self.samples_per_part = samples_per_part
        self.part_size = self.total_samples // self.num_parts
    
    def plot_segments(self):
        sns.set(style="whitegrid")
        graph_data = {}

        for i in range(self.num_parts):
            segment_start = i * self.part_size
            segment_end = segment_start + self.samples_per_part
            if segment_end > self.total_samples:
                segment_end = self.total_samples

            ecg_segment = self.record.p_signal[segment_start:segment_end, 0]
            sample_rate = 250
            peaks, _ = find_peaks(ecg_segment, distance=sample_rate*0.6)

            graph_data[f"Segment_{i + 1}"] = {
                "ecg_segment": ecg_segment.tolist(),
                "peaks": peaks.tolist()
            }

            plt.figure(figsize=(12, 6))
            plt.plot(ecg_segment, color='b', label=f'Segmento {i + 1}')
            plt.plot(peaks, ecg_segment[peaks], "rx", label='Picos R', markersize=8)
            plt.title(f"Segmento {i + 1} - Sinal ECG", fontsize=16)
            plt.xlabel("Amostras", fontsize=12)
            plt.ylabel("Amplitude (mV)", fontsize=12)
            plt.grid(True)
            plt.legend(loc='upper right', fontsize=12)
            plt.tight_layout()
            plt.axhline(0, color='k', linestyle='--', linewidth=1)
            plt.ylim(np.min(ecg_segment) - 0.2, np.max(ecg_segment) + 0.2)

            # Save the plot to a byte stream
            img_stream = BytesIO()
            plt.savefig(img_stream, format='png')
            img_stream.seek(0)
            plt.close()

            # Add the image to the data dictionary
            graph_data[f"Segment_{i + 1}"]['plot_image'] = img_stream.read()

        # Save the graph data to a JSON file
        with open('ecg_graph_data.json', 'w') as json_file:
            json.dump(graph_data, json_file, indent=4)

        return graph_data

    def calculate_metrics(self):
        ecg_signal = self.record.p_signal[:, 0]
        sample_rate = 250
        peaks, _ = find_peaks(ecg_signal, distance=sample_rate*0.6)
        rr_intervals = np.diff(peaks) / sample_rate
        heart_rate = 60 / np.mean(rr_intervals)
        pr_interval = np.mean(rr_intervals) * 0.2
        qt_interval = np.mean(rr_intervals) * 0.4
        qrs_duration = 0.1
        hrv = np.std(rr_intervals)
        r_peak_amplitude = np.max(ecg_signal[peaks]) - np.min(ecg_signal)

        metrics = {
            "Heart Rate": heart_rate,
            "PR Interval": pr_interval,
            "QT Interval": qt_interval,
            "QRS Duration": qrs_duration,
            "HRV": hrv,
            "R Peak Amplitude": r_peak_amplitude
        }

        with open('ecg_metrics.json', 'w') as json_file:
            json.dump(metrics, json_file, indent=4)

        return metrics

@app.post("/upload_ecg/")
async def upload_ecg(file: UploadFile = File(...)):
    """
    Receives the ECG file, processes it, and returns the segments and metrics.
    """
    # Save the uploaded ECG file
    ecg_path = f"uploaded_{file.filename}"
    with open(ecg_path, "wb") as f:
        f.write(await file.read())

    # Load the ECG signal using wfdb
    record = wfdb.rdrecord(ecg_path)

    # Create an instance of ECGPlotter
    ecg_plotter = ECGPlotter(record)

    # Plot the segments and save the data
    graph_data = ecg_plotter.plot_segments()

    # Calculate the metrics
    metrics = ecg_plotter.calculate_metrics()

    return {
        "graph_data": graph_data,
        "metrics": metrics
    }

if __name__ == "__main__":
    # To run the FastAPI app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
