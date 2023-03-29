import csv
field_names = ['a']
data_dict = {}
data_dict['a'] = 'bbb'
with open('user_profile.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerow(data_dict)
    # writer.writerows(data_dict)