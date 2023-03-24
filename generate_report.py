#import dataframe tools
import pandas as pd
import json

#import matplotlib and pylab
import matplotlib as mpl
import matplotlib.pyplot as plt
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig

#import PDF tools
from fpdf import FPDF

#import datetime
from datetime import datetime, date, timedelta
format = '%Y-%m-%d'

class student:
    # define the student class to handle json input
    def __init__(self, json): 
        self.id = json["id"]
        self.first_name = json["first_name"]
        self.last_name = json["last_name"]
        self.full_name = self.first_name + " " + self.last_name
        self.performance = pd.DataFrame(json["statuses_stats"])
        self.performance["total_count"] = self.performance["correct_count"] + self.performance["incorrect_count"]
        self.performance["percent_correct"] = self.performance["correct_count"] / self.performance["total_count"]
        self.performance["percent_correct100"] = self.performance["percent_correct"] *100
        self.performance["percent_correct100int"] = self.performance["percent_correct100"].astype(int)
        datel = []
        for i in self.performance["submitted_at"] :
            datel.append(datetime.strptime(i, format).date())
        self.performance["datetime"] = datel

def generateReport(json_data):
    with open(json_data) as f:
        student_data = json.load(f)
    
    #initialize the instance of the student
    student1 = student(student_data)

    #break out time series of performance by the relevant segment, which is previous 2 months
    performance = student1.performance
    performance.sort_values(by="datetime", inplace=True)

    #Get today's date and set up string of today and month for future use
    tod = date.today()
    tod_str = tod.strftime("%Y-%m-%d")
    tod_month = tod.strftime("%B").capitalize()

    #Extract last day of previous month
    this_first = date.today().replace(day=1)
    prev_last = this_first - timedelta(days=1)
    prev_first = prev_last.replace(day=1)

    prev = (performance['datetime'] >= prev_first) & (performance['datetime'] <= prev_last)

    df1=performance.loc[performance["datetime"]>prev_last]
    df2=performance.loc[prev]
    df3=performance.loc[performance["datetime"]>=prev_first]


    totalsolved_this = sum(df1["total_count"])
    totalcorrect_this = sum(df1["correct_count"])
    try:
        percentcorrect_this = int((totalcorrect_this / totalsolved_this)*100)
    except:
        percentcorrect_this = "n.a."
        
    totalsolved_prev = sum(df2["total_count"])
    totalcorrect_prev = sum(df2["correct_count"])
    try:
        percentcorrect_prev = int((totalcorrect_prev / totalsolved_prev)*100)
    except:
        percentcorrect_prev = "n.a."

    #get sums of the total cumulative sessions and questions
    prepbox_sessions = max(performance.index)
    prepbox_questions = sum(performance["total_count"])

    #convert dates to string
    join_date = min(performance["datetime"])
    join_date_str = join_date.strftime("%Y-%m-%d")
    join_date_str

    #generate graph
    fig, ax1 = plt.subplots(1, 1, figsize=(5, 3))
    ax2 = ax1.twinx()

    x= df3["submitted_at"]
    y1=df3["total_count"]
    y2=df3["percent_correct100"]

    ax1.plot(x, y1, label="Number of Problems Solved",color="orange")
    ax2.bar(x, y2, 0.5, label="Percentage Correct")
    ax1.set_xlabel('Date of Session')
    ax1.set_ylabel('Number of Problems Solved')
    ax2.set_ylabel('Perentage Correct')
    fig.savefig('performance.png')

    #Cell(float w [, float h [, string txt [, mixed border [, int ln [, string align [, boolean fill [, mixed link]]]]]]])
    pdf = FPDF()
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font('arial', 'B', 12)
    pdf.image('Prepbox_logo2.png', x = 15, y = 10, w = 40, h = 0, type = '', link = '')
    pdf.ln(26)
    pdf.cell(190, 10, "PrepBox Bi-weekly Report for "+ student1.full_name +" for "+ tod_month + " " + str(tod.year), 0, 1, 'C')
    pdf.set_font('arial', 'B', 11)
    pdf.ln(3)
    pdf.cell(7)
    pdf.cell(100, 10, "Student summary", 0, 1, "L")
    pdf.set_font('arial', '', 11)
    pdf.cell(7)
    pdf.cell(70, 7, "Student Join Date:", 0, 0, 'L')
    pdf.cell(30, 7, join_date_str, 0, 1, 'R')
    pdf.cell(7)
    pdf.cell(70, 7, "Total PrepBox Sessions to Date:", 0, 0, 'L')
    pdf.cell(30, 7, str(prepbox_sessions), 0, 1, 'R')
    pdf.cell(7)
    pdf.cell(70, 7, "Total PrepBox Questions Solved:", 0, 0, 'L')
    pdf.cell(30, 7, str(prepbox_questions), 0, 1, 'R')
    pdf.ln(5)
    pdf.set_font('arial', 'B', 11)
    pdf.cell(7)
    pdf.cell(100, 10, "Student activity for current and previous month", 0, 1, "L")
    pdf.ln(1)
    pdf.cell(8)
    pdf.set_font('arial', '', 11)
    pdf.cell(60, 7, "Category", 1, 0, 'L')
    pdf.cell(30, 7, str("This month"), 1, 0, "R")
    pdf.cell(30, 7, str("Last month"), 1, 1, "R")
    pdf.cell(8)
    pdf.cell(60, 7, "Questions solved", 1, 0, 'L')
    pdf.cell(30, 7, str(totalsolved_this), 1, 0, "R")
    pdf.cell(30, 7, str(totalsolved_prev), 1, 1, "R")
    pdf.cell(8)
    pdf.cell(60, 7, "Questions solved correctly", 1, 0, 'L')
    pdf.cell(30, 7, str(totalcorrect_this), 1, 0, "R")
    pdf.cell(30, 7, str(totalcorrect_prev), 1, 1, "R")
    pdf.cell(8)
    pdf.cell(60, 7, "Percentage correct", 1, 0, 'L')
    pdf.cell(30, 7, str(percentcorrect_this), 1, 0, "R")
    pdf.cell(30, 7, str(percentcorrect_prev), 1, 1, "R")
    pdf.ln(3)
    # pdf.cell(2.5)
    # pdf.cell(190, 10, "Summary chart for the previous two months", 0, 1, 'C')
    pdf.image('performance.png' )
    return pdf