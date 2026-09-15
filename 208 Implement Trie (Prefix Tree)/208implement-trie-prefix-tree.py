class Node:
    def __init__(self, value):
        self.value = value
        self.children = []


class Trie:
    def __init__(self):
        self.graph = Node("start")

    def insert(self, word: str) -> None:
        curr = self.graph
        for char in word:
            child = next(
                (child for child in curr.children if child.value == char),
                None
            )
            if child:
                curr = child
            else:
                new = Node(char)
                curr.children.append(new)
                curr = new

        if not any(child.value is None for child in curr.children):
            end = Node(None)
            curr.children.append(end)

    def search(self, word: str, prefixSearch: bool = False) -> bool:
        curr = self.graph
        for char in word:
            child = next(
                (child for child in curr.children if child.value == char),
                None
            )
            if not child:
                return False
            curr = child

        return prefixSearch or any(
            child.value is None for child in curr.children
        )

    def startsWith(self, prefix: str) -> bool:
        return self.search(prefix, True)
