from datetime import date


class Period:
    def __init__(self, start_date, end_date):
        self.start_date: date = start_date
        self.end_date: date = end_date
