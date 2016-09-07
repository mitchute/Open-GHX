
months = 12
end_of_months = [31,28,31,30,31,30,31,31,30,31,30,31]
hours_in_day = 24

load = 10000

out_file = open("ghx_loads.csv", 'w')

cumulative_hour = 1

# out_file.write("Date-Time,Hour,Load\n")
out_file.write("Hour,Load\n")

for month in range(months):
    for day in range(end_of_months[month]):
        for hour in range(hours_in_day):
                # out_file.write("2016-%02d-%02d %02d:00:00,%d,%d\n" %(month+1, day+1, hour, cumulative_hour, load))
                out_file.write("%d,%d\n" %(cumulative_hour, load))
                cumulative_hour += 1

out_file.close()