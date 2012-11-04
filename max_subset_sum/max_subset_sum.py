def largest_sum(nums):
        max_sum = 0
        current_sum = 0
        for num in nums:
                new_sum = current_sum + num
                if new_sum > num:
                        # continue with current sublist
                        current_sum = new_sum
                else:
                        # is better to restart the sublist
                        current_sum = num
                if current_sum > max_sum:
                        max_sum = current_sum
        return max_sum

def tests():
        # exercise example
        assert largest_sum([1, -3, 2, 3, 10, -5, 8, -12, 6]) == 18

        # adding some zeroes
        assert largest_sum([1, 0, -3, 2, 0, 3, 10, -5, 8, -12, 6]) == 18

        # test empty string
        assert largest_sum([]) == 0

        # test non numeric input
        try:
                largest_sum([1, 2, 3, 'a'])
                # As in the previous exercise, if no stated in the requirements
                # is better to let the exception bubble up
                assert False
        except TypeError:
                pass

        print "done."

if __name__ == '__main__':
    tests()
