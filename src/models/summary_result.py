class SummaryResult:
    def __init__(self, summary, topics):
        self.summary = summary
        self.topics = topics

    def get_topics_str(self):
        if isinstance(self.topics, list):
            return ", ".join(self.topics)
        return str(self.topics)
