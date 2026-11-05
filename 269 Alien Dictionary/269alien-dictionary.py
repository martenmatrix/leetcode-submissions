from collections import defaultdict

# abc, aba

class Solution:
    def alienOrder(self, words: list[str]) -> str:
        precedence = defaultdict(list)
        
        # save each used char
        # maybe could also skip this skip and instead just use the defaultdict in the other loop
        for word in words:
            for char in word:
                # use set instead of maps here to make space o(1) as our lists can have multiple letters twice and therefore this is not limited to o(26) because of 26 chars
                precedence[char] = []

        # compare all word next to each other
        for index in range(len(words) - 1):
            # could also call them prev and next word
            left_word = words[index]
            right_word = words[index + 1]

            # while char are equal skip, as this does not tell us anything
            char_index = 0

            while char_index < min(len(left_word), len(right_word)) and left_word[char_index] == right_word[char_index]:
                char_index += 1

            # that condition is not true, if we found a new differing char, ab or ab, abc (c differs but we dont know where to put it)
            if char_index == min(len(left_word), len(right_word)):
                # is the second string longer than the first one => that would mean they dont differ before that and are invalid
                if len(left_word) > len(right_word):
                    return ""
                continue

            # chars differ, so we know the first different char shows the precedence, so left comes before right
            precedence[left_word[char_index]].append(right_word[char_index])


        # dfs search and append after traversing one path so after the recursion call returns
        alphabet = []
        # chars already in the alphabet
        visited = set()

        # cycles are invalid, e.g. lets say we got [a, b, a], this contradicts
        visiting = set()
        def dfs(char):
            if char in visiting:
                # we have a cycle
                return True

            if char in visited:
                return False

            visiting.add(char)

            for adj in precedence[char]:
                if dfs(adj):
                    # pass cycle back up to the caller
                    return True
            
            visiting.remove(char)
            visited.add(char)
            alphabet.append(char)
            return False

        for char in precedence:
            if dfs(char):
                return ""

        # we append letters after finishing its neighbors, but c->[a] means c comes before a and not after it
        return "".join(reversed(alphabet))