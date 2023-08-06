import logging
import numpy as np
from .flipset import Flipset
from ..base import BaseRecourse


class ActionableRecourse(BaseRecourse):
    """
    Should work exactly as defined in the paper if the model is linear.
    Otherwise, an explainability model should be used to retrieve coefficients
    for each observation.

    Getting counterfactual is raising multiple warnings, this must be fixed
    later.

    NOTE: Initially only linear models will be considered

    https://arxiv.org/pdf/1809.06514.pdf
    """

    def __init__(
        self, model, threshold=0.5, flipset_size=100, discretize=False, sample=False
    ):
        self.model = model
        self.threshold = threshold
        self.flipset_size = flipset_size
        self.discretize = discretize
        self.sample = sample

    def _counterfactual(self, agent, action_set):
        factual = agent.values
        intercept, coefficients, model = self._get_coefficients()

        # Default counterfactual value if no action flips the prediction
        target_shape = factual.shape[0]
        empty = np.empty(target_shape)
        empty[:] = np.nan
        counterfactual = agent.copy()
        counterfactual.iloc[:] = empty

        # Align action set to coefficients
        action_set.set_alignment(coefficients=coefficients)

        # Build AR flipset
        fs = Flipset(
            x=factual,
            action_set=action_set,
            coefficients=coefficients,
            intercept=intercept,
        )
        try:
            fs_pop = fs.populate(total_items=self.flipset_size)
        except (ValueError, KeyError):
            logging.warning(
                "Actionable Recourse is not able to produce a counterfactual"
                " explanation for instance {}".format(agent.index)
            )
            logging.warning(factual)
            return counterfactual

        # Get actions to flip predictions
        actions = fs_pop.actions

        for action in actions:
            candidate_cf = agent + action

            # Check if candidate counterfactual really flipps the prediction of
            # ML model
            pred_cf = np.argmax(model.predict_proba(candidate_cf.to_frame().T))
            pred_f = np.argmax(model.predict_proba(agent.to_frame().T))
            if pred_cf != pred_f:
                counterfactual.iloc[:] = candidate_cf.squeeze()
                break

        return counterfactual
