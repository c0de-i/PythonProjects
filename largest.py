my_list = [3,13,46,79,4,6,17,57]
largest = my_list[0]
for i in range(1, len(my_list)):
    if(my_list[i]>largest):
        largest = my_list[i]
print(largest)