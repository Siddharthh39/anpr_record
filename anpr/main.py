from ANPR import create_plot
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QButtonGroup)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class ANPRVisualizationUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize attributes first
        self.current_graph = "Processing Time"
        self.current_weather = "All"
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("ANPR Performance Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Graph type buttons
        graph_group = QButtonGroup(self)
        graph_layout = QHBoxLayout()
        
        self.time_btn = QPushButton("Processing Time")
        self.fp_btn = QPushButton("False Positives")
        self.fn_btn = QPushButton("False Negatives")
        
        # Configure buttons
        buttons = [
            (self.time_btn, "Processing Time"),
            (self.fp_btn, "False Positives"),
            (self.fn_btn, "False Negatives")
        ]
        
        for btn, graph_type in buttons:
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 8px;
                    min-width: 120px;
                }
                QPushButton:checked {
                    background-color: #1E90FF;
                    color: white;
                }
            """)
            btn.clicked.connect(lambda _, gt=graph_type: self.set_graph_type(gt))
            graph_group.addButton(btn)
            graph_layout.addWidget(btn)
        
        self.time_btn.setChecked(True)
        
        # Weather condition buttons
        weather_group = QButtonGroup(self)
        weather_layout = QHBoxLayout()
        
        self.all_btn = QPushButton("All Conditions")
        self.sunny_btn = QPushButton("Sunny")
        self.rainy_btn = QPushButton("Rainy")
        self.harsh_btn = QPushButton("Harsh")
        
        # Configure weather buttons
        weather_buttons = [
            (self.all_btn, "All"),
            (self.sunny_btn, "Sunny"),
            (self.rainy_btn, "Rainy"),
            (self.harsh_btn, "Harsh")
        ]
        
        for btn, weather in weather_buttons:
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 8px;
                    min-width: 100px;
                }
                QPushButton:checked {
                    background-color: #FF6347;
                    color: white;
                }
            """)
            btn.clicked.connect(lambda _, w=weather: self.set_weather(w))
            weather_group.addButton(btn)
            weather_layout.addWidget(btn)
        
        self.all_btn.setChecked(True)
        
        # Add button panels to main layout
        layout.addWidget(QLabel("<b>Graph Type:</b>"))
        layout.addLayout(graph_layout)
        layout.addWidget(QLabel("<b>Weather Conditions:</b>"))
        layout.addLayout(weather_layout)
        
        # Matplotlib canvas
        self.figure, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Initial plot
        self.update_plot()
    
    def set_graph_type(self, graph_type):
        self.current_graph = graph_type
        self.update_plot()
    
    def set_weather(self, weather):
        self.current_weather = weather
        self.update_plot()
    
    def update_plot(self):
        self.ax.clear()
        create_plot(
            graph_type=self.current_graph,
            weather_filter=self.current_weather,
            ax=self.ax
        )
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication([])
    window = ANPRVisualizationUI()
    window.show()
    app.exec()