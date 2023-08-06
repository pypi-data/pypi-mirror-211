# +
import logging
from typing import Union

from pydantic import Field, PrivateAttr

from xopt.generators.bayesian.bax.acquisition import ExpectedInformationGain
from xopt.generators.bayesian.bax.algorithms import GridMinimize

from xopt.generators.bayesian.bayesian_generator import BayesianGenerator
from xopt.generators.bayesian.options import AcqOptions, BayesianOptions

from xopt.pydantic import XoptBaseModel
from xopt.vocs import VOCS

logger = logging.getLogger()


class AlgorithmOptions(XoptBaseModel):
    """Options for defining the algorithm in BAX"""

    _AlgoClass = PrivateAttr()  # pass desired Algorithm class as an arg

    # n_samples is a field universal to all BAX algorithms
    n_samples: int = Field(
        20, description="number of posterior samples on which to execute the algorithm"
    )

    @property
    def AlgoClass(self):
        return self._AlgoClass


class GridMinimizeOptions(AlgorithmOptions):
    _AlgoClass = PrivateAttr(GridMinimize)

    # add fields specific to this algorithm
    n_steps_sample_grid: Union[int, list[int]] = Field(
        25, description="number of steps to use per dimension for the sample grid scans"
    )


class BayesianAlgorithmExecutionOptions(AcqOptions):
    """Options for defining the acquisition function in BO"""

    algo: AlgorithmOptions = GridMinimizeOptions()


class BaxOptions(BayesianOptions):
    acq = BayesianAlgorithmExecutionOptions()


class BaxGenerator(BayesianGenerator):
    alias = "BAX"

    def __init__(
        self,
        vocs: VOCS,
        options: BaxOptions = None,
    ):
        """
        Generator that uses Expected Information Gain acquisition function
        constructed via Bayesian Algorithm Execution.
        For more information, see:
        https://arxiv.org/pdf/2104.09460.pdf

        Parameters
        ----------
        vocs: dict
            Standard vocs dictionary for xopt

        options: BayesianOptions
            Specific options for this generator
        """
        options = options or BaxOptions()
        if not isinstance(options, BaxOptions):
            raise ValueError("options must be a BaxOptions object")

        if vocs.n_objectives != 1:
            raise ValueError("vocs must have one objective for optimization")

        super().__init__(vocs, options)

    @staticmethod
    def default_options() -> BayesianOptions:
        return BaxOptions()

    def _get_acquisition(self, model):
        single_task_model = model.models[0]
        algo = self.construct_algo()
        eig = ExpectedInformationGain(single_task_model, algo)
        self.algo_results = eig.algo_results
        return eig

    def construct_algo(self):
        algo_options = self.options.acq.algo.dict()
        return self.options.acq.algo.AlgoClass(
            domain=self.vocs.bounds.T, **algo_options, tkwargs=self._tkwargs
        )
