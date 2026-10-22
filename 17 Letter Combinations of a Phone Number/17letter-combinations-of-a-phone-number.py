class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        num_to_chars = {
            2: ['a', 'b', 'c'],
            3: ['d', 'e', 'f'],
            4: ['g', 'h', 'i'],
            5: ['j', 'k', 'l'],
            6: ['m', 'n', 'o'],
            7: ['p', 'q', 'r', 's'],
            8: ['t', 'u', 'v'],
            9: ['w', 'x', 'y', 'z'],
        }

        prev = []
        res = []

        # prev = [a, b, c]
        # res = [ad, ae, af, b,]
        # 
        # starting this after 30min, coding and implementation is done, now doing a walktrough
        # walktrough finish after 10min now time and space
        # time n^2
        # space 2 times all combinations
        # some probabilty calculateion len(input) ^ biggest map of input the length (how do you call this, not squared right, and can you add this to anki)
        # no nevermind, space is O(2 * biggest_len_of_map_used ^ len of string)

        first_char = digits[0]
        # prob there is a cleaner way to do this in python but i dont know how, maybe even cleaner than the inline version
        for num in num_to_chars[int(first_char)]:
            res.append(num)

        if len(digits) == 1:
            # otherwise would get index out of bounds below
            return res

        # string copy is expensive, this i o n
        for num in digits[1:]: # O(n)
            prev = res
            res = []

            chars = num_to_chars[int(num)]
            
            for prev_comb in prev: # O(len(of input) times the longest char array in the map, so n)
                for char in chars: # O(constant, longest char of the map, e.g. here 4, for our 2-9 mappings)
                    # prob string addition also not that awesome for performance wise, but should be enough
                    new_comb = prev_comb + char
                    res.append(new_comb)

        # there can be no duplicates, as were always extending the length by one
        return res