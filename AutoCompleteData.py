
class AutoCompleteData:
    def __init__(self, complete_sentence, source_text):
        self.complete_sentence = complete_sentence
        self.source_text = source_text
        self.offset = 0
        self.score = 0

    def get_complete_sentence(self):
        return self.complete_sentence

