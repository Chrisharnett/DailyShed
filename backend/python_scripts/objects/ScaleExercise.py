from objects.Exercise import Exercise

class ScaleExercise(Exercise):
    def __init__(self, scale):
        super().__init__(scale.tonic, scale.mode, notePattern=scale.pattern, holdLastNote=True, repeatMe=True)
        self.__scale = scale

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, scale):
        self.__scale = scale


    # def findTwoSum(self, nums, target):
    #     seen = {}
    #     for num in nums:
    #         complement = target - num
    #         if complement in seen:
    #             return (complement, num)
    #         seen[num] = True
    #     return None
    #
    # def findRepeatedSum(self, nums, target):
    #     for i in range(len(nums)):
    #         repeated_num = nums[i]
    #         j = 1
    #         while repeated_num * j < target:
    #             remainder = target - repeated_num * j
    #             if remainder in nums and remainder != repeated_num:
    #                 return (repeated_num, remainder)
    #             j += 1
    #     return None


