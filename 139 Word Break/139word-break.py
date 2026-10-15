class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        dp = [False] * (len(s) + 1)
        dp[-1] = True

        for i in range(len(s) - 1, -1, -1):
            for w in wordDict:
                wordFits = i + len(w) <= len(s)
                if not wordFits:
                    continue
                    
                wordExists = (w == s[i:i + len(w)])
                stringAfterWordMatchesElsewhere = dp[i + len(w)]
                if wordExists and stringAfterWordMatchesElsewhere:
                    dp[i] = True
        
        return dp[0]
        