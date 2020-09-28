double_list = [[], []]
#double_list[0][0] = 'nul nul'
double_list[0].append('1st element')
double_list[0].append('2nd element')
double_list[0].append('3nd element')
double_list[1].append('111')
double_list[1].append('222')



print(double_list)
print(len(double_list))
print(len(double_list[0]))
print(double_list[1].pop(0))
print(double_list)
