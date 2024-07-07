def calculate_gpa(num_subjects, marks_list, hours_list):
    total = 0
    total_hours = 0
    for i in range(num_subjects):
        marks = marks_list[i]
        hours = hours_list[i]
        total += marks * hours
        total_hours += hours
    final_gpa = total / total_hours
    return final_gpa
