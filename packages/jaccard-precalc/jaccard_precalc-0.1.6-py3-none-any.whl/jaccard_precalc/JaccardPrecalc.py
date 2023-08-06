class JaccardPrecalc:
    def __init__(self, lexicon, case_sensitive = False):
        self.lexicon = set(lexicon)
        self.case_sensitive = case_sensitive
        self.precalc()

    def precalc(self):
        self.mapping = {}
        for word in self.lexicon:
            if not self.case_sensitive:
                lower = word.lower()
                self.mapping[word] = self.transform_to_dict(lower)
            else:
                self.mapping[word] = self.transform_to_dict(word)

    def transform_to_dict(self, word):
        elements = {}
        for start in range(len(word)):
            for end in range(start+1, len(word)+1):
                try:
                    elements[word[start:end]] += 1
                except:
                    elements[word[start:end]] = 1
        return elements

    def search(self, query, number_of_results = 10):
        if not self.case_sensitive:
            query = query.lower()
        query = self.transform_to_dict(query)
        results = [[self.compare(query, self.mapping[word]), word]
                   for word in self.mapping.keys()]
        results.sort(reverse=True)
        return [{elem[1]:elem[0]} for elem in results[:number_of_results]]
    
    def compare(self, dict1, dict2):
        reward = 0
        penalty = 0
        for key in dict1:
            if key in dict2:
                reward += dict1[key] * 2
            else:
                penalty += 1
        for key in dict2:
            if key in dict1:
                reward += dict2[key] * 2
            else:
                penalty += 1
        return reward / (reward + penalty)
