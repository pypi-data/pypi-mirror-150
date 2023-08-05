# Copyright 2021 AIPlan4EU project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from fractions import Fraction
import warnings
import unified_planning as up
import unified_planning.solvers as solvers
from unified_planning.plan import Plan, ActionInstance
from unified_planning.model import ProblemKind
from unified_planning.exceptions import UPException
from unified_planning.solvers.results import LogLevel, PlanGenerationResultStatus
from typing import IO, Callable, Dict, List, Optional, Tuple, cast
from multiprocessing import Process, Queue


class Parallel(solvers.solver.Solver):
    """Create a parallel instance of multiple Solvers."""

    def __init__(self, solvers: List[Tuple[type, Dict[str, str]]]):
        self.solvers = solvers

    @property
    def name(self) -> str:
        return 'Parallel'

    @staticmethod
    def is_oneshot_planner() -> bool:
        raise UPException('The Parallel solver type depends on its actual solvers')

    @staticmethod
    def is_plan_validator() -> bool:
        raise UPException('The Parallel solver type depends on its actual solvers')

    @staticmethod
    def supports(problem_kind: 'ProblemKind') -> bool:
        raise UPException('The Parallel supported features depends on its actual solvers')

    def _run_parallel(self, fname, *args):
        signaling_queue = Queue()
        processes = []
        for idx, (solver_class, opts) in enumerate(self.solvers):
            options = opts
            _p = Process(name=str(idx),
                         target=_run,
                         args=(idx, solver_class, options,
                               signaling_queue, fname, *args))
            processes.append(_p)
            _p.start()
        processes_alive = len(processes)
        results: List[up.solvers.PlanGenerationResult] = []
        planners_final_status: List[str] = []
        definitive_result_found: bool = False
        optimality_required: bool = len(args[0].quality_metrics) > 0 # Require optimality if the problem has at least one quality metric.
        while True:
            if processes_alive == 0: # Every planner gave a result
                break
            (idx, res) = signaling_queue.get(block=True)
            processes_alive -= 1
            if isinstance(res, BaseException):
                raise res
            else:
                assert isinstance(res, up.solvers.PlanGenerationResult)
                # If the planner is sure about the result (optimality of the result or impossibility of the problem or the problem does not need optimality) exit the loop
                if res.status == PlanGenerationResultStatus.SOLVED_OPTIMALLY or res.status == PlanGenerationResultStatus.UNSOLVABLE_PROVEN or (res.status == PlanGenerationResultStatus.SOLVED_SATISFICING and not optimality_required):
                    definitive_result_found = True
                    break
                else:
                    planners_final_status.append(f'{res.planner_name}: {res.status_as_str()}')
                    if res.plan is not None:
                        results.append(res)
        for p in processes:
            p.terminate()
        if definitive_result_found: # A planner found a definitive result
            return res
        else:
            result_order: List[int] = [  PlanGenerationResultStatus.SOLVED_SATISFICING,  # List containing the results in the order we prefer them
                                         PlanGenerationResultStatus.TIMEOUT,
                                         PlanGenerationResultStatus.MEMOUT,
                                         PlanGenerationResultStatus.INTERNAL_ERROR]
            logs = up.solvers.LogMessage(LogLevel.INFO, ', '.join(planners_final_status))
            for ro in result_order:
                for r in results:
                    if r.status == ro:
                        return r # NOTE Here we may want to append the logs variable to log_messages
            # if no results are given by the planner, we create a default one
            return up.solvers.PlanGenerationResult(PlanGenerationResultStatus.UNSOLVABLE_INCOMPLETELY,
                                                    None, self.name, log_messages=[logs])


    def solve(self, problem: 'up.model.Problem',
                    callback: Optional[Callable[['up.solvers.results.PlanGenerationResult'], None]] = None,
                    timeout: Optional[float] = None,
                    output_stream: Optional[IO[str]] = None) -> 'up.solvers.results.PlanGenerationResult':
        if callback is not None:
            warnings.warn('Parallel solvers do not support the callback system.', UserWarning)
        if output_stream is not None:
            warnings.warn('Parallel solvers do not support the output stream system.', UserWarning)
        final_report = self._run_parallel('solve', problem, None, timeout, None)
        new_plan = self.convert_plan(final_report.plan, problem)
        return up.solvers.results.PlanGenerationResult(final_report.status, new_plan, final_report.planner_name, final_report.metrics, final_report.log_messages)

    def convert_plan(self, plan: 'up.plan.Plan', problem: 'up.model.Problem')-> 'up.plan.Plan':
        objects = {}
        for ut in problem.user_types:
            for obj in problem.objects(ut):
                objects[obj.name] = obj
        em = problem.env.expression_manager
        actions: List[ActionInstance] = []
        if isinstance(plan, up.plan.SequentialPlan):
            actions = plan.actions
        elif isinstance(plan, up.plan.TimeTriggeredPlan):
            actions = [a for _, a, _ in plan.actions]
        else:
            raise NotImplementedError
        new_actions: List[ActionInstance] = []
        for a in actions:
            new_a = problem.action(a.action.name)
            params = []
            for p in a.actual_parameters:
                if p.is_object_exp():
                    obj = objects[p.object().name]
                    params.append(em.ObjectExp(obj))
                elif p.is_bool_constant():
                    params.append(em.Bool(p.is_true()))
                elif p.is_int_constant():
                    params.append(em.Int(cast(int, p.constant_value())))
                elif p.is_real_constant():
                    params.append(em.Real(cast(Fraction, p.constant_value())))
                else:
                    raise
            new_actions.append(ActionInstance(new_a, tuple(params)))
        if isinstance(plan, up.plan.SequentialPlan):
            return up.plan.SequentialPlan(new_actions)
        elif isinstance(plan, up.plan.TimeTriggeredPlan):
            return up.plan.TimeTriggeredPlan([(t, a, d) for (t, _, d), a in zip(plan.actions, new_actions)])
        else:
            raise NotImplementedError

    def validate(self, problem: 'up.model.Problem', plan: Plan) -> bool:
        return self._run_parallel('validate', problem, plan)

    def destroy(self):
        pass


def _run(idx: int, SolverClass: type, options: Dict[str, str], signaling_queue: Queue, fname: str, *args):
    with SolverClass(**options) as s:
        try:
            local_res = getattr(s, fname)(*args)
        except Exception as ex:
            signaling_queue.put((idx, ex))
            return
        signaling_queue.put((idx, local_res))
