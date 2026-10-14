from collections import defaultdict

class Solution:
    def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:
        graph = defaultdict(set)
        mail_to_name = {}

        for acc in accounts:
            # first@mail.com -> set([all mails from account, e.g. second@mail.com])
            # every mail from account -> set(first@mail.com)
            # so, that if we traverse e.g. the next account that also has second@mail.com, we know that it points to first@mail, and can just do a dfs on the set from first@mail
            for mail in acc[1:]:
                graph[acc[1]].add(mail)
                graph[mail].add(acc[1])

                mail_to_name[mail] = acc[0]

        res = []
        visited = set()

        for node in graph:
            if node in visited:
                continue

            stack = [node]
            visited.add(node)
            partial_res = set()

            while stack:
                curr_node = stack.pop()
                adjacent = graph[curr_node]
                partial_res.add(curr_node)

                for mail in adjacent:
                    if not mail in visited:
                        stack.append(mail)
                        visited.add(mail)
            
            name = mail_to_name[node]
            res.append([name] + sorted(list(partial_res)))

        return res