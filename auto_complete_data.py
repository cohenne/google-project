
class AutoCompleteData:
    def __init__(self, complete_sentence, source_text, offset, score):
        self.complete_sentence = complete_sentence
        self.source_text = source_text
        self.offset = offset
        self.score = score

    def get_complete_sentence(self):
        return self.complete_sentence

    def get_source_text(self):
        return self.source_text


