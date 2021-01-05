import os
from datetime import date
from fpdf import FPDF

LOG_FILE_PATH = "data/logs/daily_log_"
GRAPH_FILE_PATH = "data/graphs/risks_graph_"
BACKGROUND_FILE_PATH = "data/images/background.jpg"
CALIBRI_BOLD_FILE_PATH = "data/fonts/calibri_bold.ttf"
CALIBRI_LIGHT_FILE_PATH = "data/fonts/calibri_light.ttf"
LOG_TITLE = "WAF Daily Log"
GRAPH_TITLE = "Risks Found In The Last Day"


class LogComposer:
    _daily_log = FPDF()

    def __init__(self):
        """
        This function will initialize the pdf log document and will set the title
        """
        self._daily_log.add_page()
        self._load_calibri_font(CALIBRI_BOLD_FILE_PATH, CALIBRI_LIGHT_FILE_PATH)
        self._set_main_page(LOG_TITLE)

    def _load_calibri_font(self, calibri_bold_file_path, calibri_light_file_path):
        self._remove_calibri_font_configuration(calibri_bold_file_path, calibri_light_file_path)
        if os.path.exists(calibri_bold_file_path) and os.path.exists(calibri_light_file_path):
            self._daily_log.add_font("Calibri", 'B', calibri_bold_file_path, uni=True)
            self._daily_log.add_font("Calibri Light", "", calibri_light_file_path, uni=True)
        else:
            raise FileNotFoundError

    def _remove_calibri_font_configuration(self, calibri_bold_file_path, calibri_light_file_path):
        calibri_bold_file_path = calibri_bold_file_path.replace(".ttf", ".pkl")
        calibri_light_file_path = calibri_light_file_path.replace(".ttf", ".pkl")
        if os.path.exists(calibri_bold_file_path):
            os.remove(calibri_bold_file_path)
        if os.path.exists(calibri_light_file_path):
            os.remove(calibri_light_file_path)

    def _set_main_page(self, log_title):
        """
        This function will write the log's main page date, title and background
        :param log_title: the title of the main page
        :type log_title: string
        """
        self._daily_log.image(BACKGROUND_FILE_PATH, x=0, y=0, w=200, h=300)
        self._daily_log.set_font("Calibri Light", size=12)
        self._daily_log.cell(w=190, h=5, txt=date.today().strftime("%d/%m/%Y"), ln=1, align='R')
        self._daily_log.set_font("Calibri", 'B', size=72)
        self._daily_log.cell(w=200, h=250, txt=log_title, ln=1, align='C')

    def write_log(self, info):
        """
        This function will write all the attacks information
        into the daily log file and will save it
        :param info: all the attacks information
        :type info: dict
        """
        for attack_name, attack_info in info.items():
            self._daily_log.add_page()
            self._set_page_header(attack_name)
            self._daily_log.set_font("Calibri Light", size=14)
            for detail in attack_info.split('\n'):
                self._daily_log.cell(w=200, h=12, txt=detail, ln=2, align='L')
        self._add_graph(GRAPH_FILE_PATH + date.today().strftime("%d/%m/%Y").replace('/', '_') + ".png")
        self._daily_log.output(LOG_FILE_PATH + date.today().strftime("%d/%m/%Y").replace('/', '_') + ".pdf")

    def _set_page_header(self, title):
        """
        This function will write the the log's page date, title and background
        :param title: the title of the page
        :type title: string
        """
        self._daily_log.image(BACKGROUND_FILE_PATH, x=0, y=0, w=200, h=300)
        self._daily_log.set_font("Calibri Light", size=12)
        self._daily_log.cell(w=190, h=5, txt=date.today().strftime("%d/%m/%Y"), ln=1, align='R')
        self._daily_log.set_font("Calibri", "BU", size=32)
        self._daily_log.cell(w=200, h=20, txt=title, ln=1, align='C')

    def _add_graph(self, graph_file_path):
        """
        This function will add the risks graph to the daily log
        :param graph_file_path: the graph's file path
        :type graph_file_path: string
        """
        self._daily_log.add_page()
        self._set_page_header(GRAPH_TITLE)
        self._daily_log.image(graph_file_path, x=-10, y=35, w=240, h=230)