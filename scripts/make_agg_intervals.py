def make_interval(depth, depth_integer_multiplier, num, step_num, start_val):

    all_groups_str = "[\n"

    for n in range(num):
        all_groups_str += "\t["
        for d in range(depth):
            val = str(start_val * pow(depth_integer_multiplier, d))
            if d == depth - 1:
                if n == num - 1:
                    all_groups_str += "%s]\n" % val
                else:
                    all_groups_str += "%s],\n" % val
            else:
                all_groups_str += "%s, " % val

        start_val += step_num

    all_groups_str += "]\n"

    return all_groups_str

print(make_interval(12, 2, 10, 10, 10))
