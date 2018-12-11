import pandas as pd
import numpy as np
import os
import time
import sys

def create_df(fname):
    return  pd.read_csv(fname)

def create_set(label, data):
    temp_list = []

    for i, item in data.iterrows():
        temp_list.append(item[label])

    return set(temp_list)

def create_section_dict(sect_set, df):
    section_dict = {}
    for section in sect_set:
        section_df = df[df["Section"]==section]
        section_dict[section] = create_set("Question", section_df)
    return section_dict

def get_student_scores(students, section_dict, df):
    student_dict = {}
    for student in students:

        student_data = df[df["Student #"] == student]
        output_dict = {}
        output_dict["Student Name"] = student_data["Student"].tolist()[0]

        for section in section_dict.keys():
            section_data = student_data[student_data["Section"] == section]
            question_score = []
            question_list = []

            for question in section_dict[section]:

                try:
                    question_data = section_data[section_data["Question"] == question]

                    question_score.append(question_data["Rating"].mean())
                    question_list.append(len(question_data))

                except:
                    continue
            section_score = np.nanmean(question_score)

            #output_dict[section] = '{0:.1f} ({1})'.format(section_score, np.max(question_list))
            output_dict[section] = '{0:.1f}'.format(section_score, np.max(question_list))

            # print(student, section, section_score, np.max(question_list), '{0:.1f} ({1})'.format(section_score, np.max(question_list)))

            student_dict[student] = output_dict

    return student_dict

def get_csv_files(folder):
    path = folder
    dirs = os.listdir(path)
    file_list = []

    for file in dirs:
        if (file.find('.csv') and file.find('.~lock.')):
            file_list.append(file)

    return file_list

def concat_csv(folder):
    df_list = []
    files = get_csv_files(folder)
    for file in files:
        df_list.append(create_df(folder + '/' + file))

    return pd.concat(df_list)

if __name__ == "__main__":
    df = concat_csv(sys.argv[1])
    students = create_set("Student #", df)
    section_dict = create_section_dict(create_set("Section", df), df)
    scores = get_student_scores(students, section_dict, df)
    pd.DataFrame.from_dict(scores, orient='index').to_excel("gc_upload_" + str('{0:.0f}'.format(time.time())) + ".xlsx")


