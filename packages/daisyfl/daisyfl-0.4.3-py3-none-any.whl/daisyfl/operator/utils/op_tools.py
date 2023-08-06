from typing import Dict, List, Optional, Tuple, Union, Callable
from queue import Queue
from daisyfl.common import (
    Code,
    Task,
    Report,
    CURRENT_ROUND,
    EVALUATE,
    TIMEOUT,
    FIT_SAMPLES,
    EVALUATE_SAMPLES,
    LOSS,
    METRICS,
    DisconnectRes,
    EvaluateIns,
    EvaluateRes,
    FitIns,
    FitRes,
    Parameters,
    ReconnectIns,
    Scalar,
    CheckResults,
    CurrentReturns,
)
from daisyfl.common.logger import log
from daisyfl.common.typing import GetParametersIns
from daisyfl.server.server import Server
from daisyfl.server.client_proxy import ClientProxy
from daisyfl.operator.strategy import Strategy
from threading import Condition

FitResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, FitRes]],
    List[Union[Tuple[ClientProxy, FitRes], BaseException]],
]
EvaluateResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, EvaluateRes]],
    List[Union[Tuple[ClientProxy, EvaluateRes], BaseException]],
]
ReconnectResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, DisconnectRes]],
    List[Union[Tuple[ClientProxy, DisconnectRes], BaseException]],
]


def get_configure_fit(
    strategy: Strategy,
    server_round: int,
    parameters: Parameters,
    server: Server,
    config: Dict,
    credential: str,
) -> List[Tuple[ClientProxy, FitIns]]:
    client_instructions = strategy.configure_fit(
        server_round=server_round,
        parameters=parameters,
        server=server,
        credential=credential,
    )
    for i in range(len(client_instructions)):
        client_instructions[i][1].config = config.copy()
    return client_instructions

def get_configure_evaluate(
    strategy: Strategy,
    server_round: int,
    parameters: Parameters,
    server: Server,
    config: Dict,
    credential: str,
) -> List[Tuple[ClientProxy, EvaluateIns]]:
    client_instructions = strategy.configure_evaluate(
        server_round=server_round,
        parameters=parameters,
        server=server,
        credential=credential,
    )
    for i in range(len(client_instructions)):
        client_instructions[i][1].config = config.copy()
    return client_instructions

def aggregate_fit(
    strategy: Strategy,
    server_round: int,
    results: List[Tuple[ClientProxy, FitRes]],
    failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]],
) -> Tuple[Optional[Parameters], int, Dict[str, Scalar]]:
    """Aggregate fit results using weighted average."""
    results_for_aggregate = [(
        client, type('',(object,),{
            "parameters": res.parameters,
            "prime": res.parameters,
            "num_examples": res.config[FIT_SAMPLES],
            "metrics": res.config[METRICS],
            "config": res.config,
        })()
    ) for client, res in results]

    # Aggregate training results
    parameters, metrics = strategy.aggregate_fit(server_round, results_for_aggregate, failures)
    # num_examples
    num_examples = int(sum([res.config[FIT_SAMPLES] for _, res in results]) / len(results))
    return parameters, num_examples, metrics

def aggregate_evaluate(
    strategy: Strategy,
    server_round: int,
    results: List[Tuple[ClientProxy, EvaluateRes]],
    failures: List[Union[Tuple[ClientProxy, EvaluateRes], BaseException]],
) -> Tuple[Optional[float], int, Dict[str, Scalar]]:
    """Aggregate evaluation losses using weighted average."""
    results_for_aggregate = [(
        client, type('',(object,),{
            "loss": res.config[LOSS],
            "num_examples": res.config[EVALUATE_SAMPLES],
            "metrics": res.config[METRICS],
            "config": res.config,
        })()
    ) for client, res in results]
    
    # Aggregate the evaluation results
    loss, metrics = strategy.aggregate_evaluate(server_round, results_for_aggregate, failures)
    # num_examples
    num_examples = int(sum([res.config[EVALUATE_SAMPLES] for _, res in results]) / len(results))
    return loss, num_examples, metrics

def generate_fit_report(
    server_round: int,
    samples: int,
    metrics_aggregated: Dict[str, Scalar],
)-> Report:
    # (parameters, num_examples, metrics) -> Parameters, Report
    return Report(config={
        CURRENT_ROUND: server_round,
        FIT_SAMPLES: samples,
        METRICS: metrics_aggregated,
    })

def generate_evaluate_report(
    server_round: int,
    samples: int,
    loss_aggregated: Optional[float],
    metrics_aggregated: Dict[str, Scalar],
) -> Report:
    # (loss, num_examples, metrics) -> Report
    return Report(config={
        CURRENT_ROUND: server_round,
        LOSS: loss_aggregated,
        EVALUATE_SAMPLES: samples,
        METRICS: metrics_aggregated,
    })

def wait_for_results(
    strategy: Strategy, current_returns: CurrentReturns,
) -> bool:
    cnd = current_returns.cnd
    with cnd:
        cnd.wait_for(lambda: strategy.check_results(current_returns) in [CheckResults.OK, CheckResults.FAIL])
    if strategy.check_results(current_returns) == CheckResults.OK:
        return True
    return False
