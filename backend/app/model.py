"""Wraps River's BernoulliNB model for online (incremental) learning."""

from river import naive_bayes


class RecipeRecommenderModel:
    """A small wrapper around River's BernoulliNB.

    We wrap it so the rest of the codebase doesn't need to know any
    River-specific details — it just calls learn() and
    predict_like_probability().
    """

    def __init__(self) -> None:
        self.model = naive_bayes.BernoulliNB(alpha=1.0)
        self.has_learned = False

    def learn(self, features: dict[str, bool], liked: bool) -> None:
        """Incrementally updates the model with one piece of feedback.

        This is the "Online Learning" requirement: we never retrain from
        scratch, we just call learn_one() with the new example.
        """
        self.model.learn_one(features, liked)
        self.has_learned = True

    def predict_like_probability(self, features: dict[str, bool]) -> float:
        """Returns the probability (0.0 - 1.0) that the user will like
        a recipe with these features.
        """
        if not self.has_learned:
            # The model hasn't seen any feedback yet, so we can't make
            # an informed prediction. 0.5 means "no opinion yet".
            return 0.5

        probabilities = self.model.predict_proba_one(features)
        return probabilities.get(True, 0.5)