from ANPR import create_plot
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QComboBox, QPushButton, QLabel)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class ANPRVisualizationUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("ANPR Performance Visualizer")
        self.setGeometry(100, 100, 1000, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Controls panel
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        
        # Graph type selector
        self.graph_type = QComboBox()
        self.graph_type.addItems([
            "Processing Time",
            "False Positives",
            "False Negatives"
        ])
        controls_layout.addWidget(QLabel("Graph Type:"))
        controls_layout.addWidget(self.graph_type)
        
        # Weather filter
        self.weather_filter = QComboBox()
        self.weather_filter.addItems(["All", "Sunny", "Rainy", "Harsh"])
        controls_layout.addWidget(QLabel("Weather Filter:"))
        controls_layout.addWidget(self.weather_filter)
        
        # Refresh button
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.update_plot)
        controls_layout.addWidget(self.refresh_btn)
        
        layout.addWidget(controls)
        
        # Matplotlib canvas
        self.figure, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Initial plot
        self.update_plot()
    
    def update_plot(self):
        graph_type = self.graph_type.currentText()
        weather = self.weather_filter.currentText()
        
        create_plot(
            graph_type=graph_type,
            weather_filter=weather,
            ax=self.ax
        )
        
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication([])
    window = ANPRVisualizationUI()
    window.show()
    app.exec()