class Score:

    def __init__(self, score_type, score, run):
        self.score_type = score_type
        self.score = score
        self.run = run

    def get_score_type(self):
        return self.score_type

    def get_score(self):
        return self.score

    def get_run(self):
        return self.run


def score_creator(info_dict: dict, run: int = None) -> Score:
    return Score(score_type=info_dict["ScoreTypeID"], score=info_dict["Score"],
                 run=run)


def scores_creator(info_dict: dict, run: int = None) -> list:
    if info_dict is None:
        return None
    scores = list()
    for score_info in info_dict:
        scores.append(score_creator(info_dict=score_info, run = run))
    return scores
