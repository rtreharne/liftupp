from format import *
from collections import Counter

def decide_staff(df, students):
    student_staff = {}
    for student in students:
        student_df = df[df["Student #"]==student]
        staff_list = create_set("Staff", student_df, list=True)
        staff_member = Counter(staff_list).most_common(1)[0][0]
        student_staff[student] = staff_member
    return student_staff

def split_by_staff(scores, student_staff):

    cols = scores.columns.tolist()
    cols.insert(0, cols.pop(cols.index('Student Name')))
    scores = scores.reindex(columns=cols)

    scores['Staff'] = scores.index.map(student_staff)
    scores_by_staff = []

    staff_list = create_set("Staff", scores)
    for staff in staff_list:
        scores_by_staff.append(scores[scores["Staff"]==staff])

    return scores_by_staff

def _color_red_or_green(val):
    color = 'red'# if type(val) is str else 'green'
    return 'color: %s' % color

def df_to_sheets(filename, dfs):
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    workbook = writer.book
    red_format = workbook.add_format({'bg_color': 'red'})
    for i, df in enumerate(dfs):
        staff_name = df.iloc[0]["Staff"]
        df.to_excel(writer, sheet_name=staff_name)
        worksheet = writer.sheets[staff_name]

        worksheet.conditional_format('C2:J100', {'type': 'text',
                                               'criteria': 'containing',
                                               'value': '(0)',
                                               'format': red_format})
        worksheet.conditional_format('C2:J100', {'type': 'text',
                                                 'criteria': 'containing',
                                                 'value': '(1)',
                                                 'format': red_format})
        worksheet.conditional_format('C2:J100', {'type': 'text',
                                                 'criteria': 'containing',
                                                 'value': '(2)',
                                                 'format': red_format})

    writer.save()

if __name__ == "__main__":
    df = concat_csv(sys.argv[1])
    students = create_set("Student #", df)
    student_staff = decide_staff(df, students)
    section_dict = create_section_dict(create_set("Section", df), df)
    scores = get_student_scores(students, section_dict, df)
    scores_by_staff = split_by_staff(scores, student_staff)
    df_to_sheets('test.xlsx', scores_by_staff)
