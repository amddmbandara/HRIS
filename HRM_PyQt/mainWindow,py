import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QFont, QPainter, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtChart import (
    QChart, QChartView, QBarSet, QBarSeries,
    QPieSeries, QBarCategoryAxis
)


class HRMMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HRM System - Dashboard")
        self.setFixedSize(1200, 750)
        self.setStyleSheet("background-color: #f4f6f9;")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ================= Sidebar =================
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e3a5f,
                    stop:1 #2b6cb0
                );
            }
            QPushButton {
                color: white;
                background: transparent;
                border: none;
                padding: 14px 18px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.15);
                border-left: 4px solid #fbbf24;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 20)
        sidebar_layout.setSpacing(5)

        # ===== LOGO SECTION =====
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 10, 0, 20)

        logo_label = QLabel()
        try:
            pixmap = QPixmap('fbsl_logo.png')
            if not pixmap.isNull():
                pixmap = pixmap.scaled(200, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(pixmap)
            else:
                logo_label.setText("FBSL")
                logo_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
                logo_label.setStyleSheet("color: white;")
        except Exception as e:
            logo_label.setText("FBSL")
            logo_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
            logo_label.setStyleSheet("color: white;")

        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)
        sidebar_layout.addWidget(logo_container)

        # Sidebar menu
        for name in ["Home", "Employee", "Attendance", "Salary", "Leave", "Loan"]:
            sidebar_layout.addWidget(QPushButton(name))

        sidebar_layout.addStretch()

        # ================= Main Content =================
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(20)

        header = QLabel("Dashboard Overview")
        header.setFont(QFont("Segoe UI", 22, QFont.Bold))
        header.setStyleSheet("color: #2d3748;")
        content_layout.addWidget(header)

        # ================= Cards =================
        card_layout = QHBoxLayout()
        card_layout.setSpacing(20)

        def create_card(title, value, color):
            card = QFrame()
            card.setMinimumWidth(200)
            card.setMaximumWidth(300)
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: white;
                    border-radius: 15px;
                    border-left: 8px solid {color};
                    padding: 15px;
                }}
            """)
            v = QVBoxLayout(card)
            v.setContentsMargins(10, 10, 10, 10)

            t = QLabel(title)
            t.setFont(QFont("Segoe UI", 11))
            t.setStyleSheet("color: #718096;")

            val = QLabel(value)
            val.setFont(QFont("Segoe UI", 28, QFont.Bold))
            val.setStyleSheet("color: #2d3748;")

            v.addWidget(t)
            v.addStretch()
            v.addWidget(val)
            return card

        card_layout.addStretch()
        card_layout.addWidget(create_card("Total Employees", "120", "#4299e1"))
        card_layout.addWidget(create_card("Today Attendance", "98", "#48bb78"))
        card_layout.addWidget(create_card("Total Staff", "80", "#ed8936"))
        card_layout.addWidget(create_card("Total Labours", "40", "#9f7aea"))
        card_layout.addStretch()

        content_layout.addLayout(card_layout)

        # ================= Charts =================
        chart_layout = QHBoxLayout()
        chart_layout.setSpacing(20)

        # Attendance Bar Chart
        bar_set = QBarSet("Attendance")
        bar_set.append([75, 80, 78, 85, 90, 95])
        bar_set.setColor(Qt.darkBlue)

        bar_series = QBarSeries()
        bar_series.append(bar_set)

        bar_chart = QChart()
        bar_chart.addSeries(bar_series)
        bar_chart.setTitle("Monthly Attendance Overview")
        bar_chart.setTitleFont(QFont("Segoe UI", 12, QFont.Bold))
        bar_chart.setAnimationOptions(QChart.SeriesAnimations)
        bar_chart.legend().setVisible(False)
        bar_chart.setBackgroundRoundness(12)
        bar_chart.setBackgroundBrush(Qt.white)

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        axis_x = QBarCategoryAxis()
        axis_x.append(months)
        bar_chart.addAxis(axis_x, Qt.AlignBottom)
        bar_series.attachAxis(axis_x)

        bar_view = QChartView(bar_chart)
        bar_view.setRenderHint(QPainter.Antialiasing)

        # Employee Distribution Pie Chart
        pie_series = QPieSeries()
        pie_series.append("Staff", 80)
        pie_series.append("Labours", 40)

        pie_series.slices()[0].setBrush(Qt.darkCyan)
        pie_series.slices()[1].setBrush(Qt.darkMagenta)

        pie_chart = QChart()
        pie_chart.addSeries(pie_series)
        pie_chart.setTitle("Employee Distribution")
        pie_chart.setTitleFont(QFont("Segoe UI", 12, QFont.Bold))
        pie_chart.setBackgroundRoundness(12)
        pie_chart.setBackgroundBrush(Qt.white)

        pie_view = QChartView(pie_chart)
        pie_view.setRenderHint(QPainter.Antialiasing)

        chart_layout.addWidget(bar_view, 2)
        chart_layout.addWidget(pie_view, 1)

        content_layout.addLayout(chart_layout)
        content_layout.addStretch()

        # ================= Assemble =================
        main_layout.addWidget(sidebar)
        main_layout.addLayout(content_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = HRMMainWindow()
    window.show()
    sys.exit(app.exec_())
