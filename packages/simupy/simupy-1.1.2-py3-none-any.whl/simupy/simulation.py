import numpy as np
from simupy.utils import callable_from_trajectory
from scipy.integrate import ode
from scipy.optimize import brentq




DEFAULT_INTEGRATOR_CLASS = ode
DEFAULT_INTEGRATOR_OPTIONS = {
    "name": "dopri5",
    "rtol": 1e-6,
    "atol": 1e-12,
    "nsteps": 500,
    "max_step": 0.0,
}

DEFAULT_EVENT_FINDER = brentq
DEFAULT_EVENT_FIND_OPTIONS = {
    "xtol": 2e-12,
    "rtol": 8.8817841970012523e-16,
    "maxiter": 100,
}

nan_warning_message = (
    "BlockDiagram encountered NaN outputs and quit during"
    + " {}. This may have been intentional! NaN outputs at "
    + "time t={}, state x={}, output y={}"
)


class SimulationResult(object):
    """
    A simple class to collect simulation result trajectories.

    Attributes
    ----------
    t : array of times
    x : array of states
    y : array of outputs
    e : array of events
    """

    max_allocation = 2 ** 7

    def __init__(self, dim_states, dim_outputs, num_events, tspan, initial_size=0):
        if initial_size == 0:
            initial_size = tspan.size
        self.t = np.empty(initial_size)
        self.x = np.empty((initial_size, dim_states))
        self.y = np.empty((initial_size, dim_outputs))
        self.e = np.empty((initial_size, num_events))
        self.res_idx = 0
        self.tspan = tspan
        self.t0 = tspan[0]
        self.tF = tspan[-1]

    def allocate_space(self, t):
        more_rows = int((self.tF - t) * self.t.size / (t - self.t0)) + 1
        more_rows = max(min(more_rows, self.max_allocation), 1)

        self.t = np.r_[self.t, np.empty(more_rows)]
        self.x = np.r_[self.x, np.empty((more_rows, self.x.shape[1]))]
        self.y = np.r_[self.y, np.empty((more_rows, self.y.shape[1]))]
        self.e = np.r_[self.e, np.empty((more_rows, self.e.shape[1]))]

    def new_result(self, t, x, y, e=None):
        if self.res_idx >= self.t.size:
            self.allocate_space(t)
        self.t[self.res_idx] = t
        self.x[self.res_idx, :] = x
        self.y[self.res_idx, :] = y
        if e is not None:
            self.e[self.res_idx, :] = e
        else:
            self.e[self.res_idx, :] = np.zeros(self.e.shape[1])
        self.res_idx += 1

    def last_result(self, n=1, copy=False):
        n = np.clip(n, 1, self.res_idx)
        if copy:
            return (
                np.copy(self.t[self.res_idx - n]),
                np.copy(self.x[self.res_idx - n, :]),
                np.copy(self.y[self.res_idx - n, :]),
            )
        else:
            return (
                self.t[self.res_idx - n],
                self.x[self.res_idx - n, :],
                self.y[self.res_idx - n, :],
            )

class SimulationMixin:
    def computation_step(self, t, state, output=None, do_events=False):
        """
        callable to compute system outputs and state derivatives
        """
        # compute state equation for full systems,
        # x[t_k']=f(t_k,x[t_k],u[t_k])
        output = (
            output if output is not None else self.output_equation_function(t, state)
        )
        dxdt = self.state_equation_function(t, state, output)

        if do_events:
            events = self.event_equation_function(t, state, output)

            return dxdt, output, events

        return dxdt, output

    def simulate(
        self,
        tspan,
        integrator_class=DEFAULT_INTEGRATOR_CLASS,
        integrator_options=DEFAULT_INTEGRATOR_OPTIONS,
        event_finder=DEFAULT_EVENT_FINDER,
        event_find_options=DEFAULT_EVENT_FIND_OPTIONS,
    ):
        """
        Simulate the block diagram

        Parameters
        ----------
        tspan : list-like or float

            Argument to specify integration time-steps.

            If a single time is specified, it is treated as the final time.
            If two times are specified, they are treated as initial and
            final times. In either of these conditions, it is assumed that
            that every time step from a variable time-step integrator will
            be stored in the result.

            If more than two times are specified, these are the only times
            where the trajectories will be stored.

        integrator_class : class, optional
            Class of integrator to use. Defaults to ``scipy.integrate.ode``.
            Must provide the following subset of the ``scipy.integrate.ode``
            API:

                - ``__init__(derivative_callable(time, state))``
                - ``set_integrator(**kwargs)``
                - ``set_initial_value(state, time)``
                - ``set_solout(successful_step_callable(time, state))``
                - ``integrate(time)``
                - ``successful()``
                - ``y``, ``t`` properties

        integrator_options : dict, optional
            Dictionary of keyword arguments to pass to
            ``integrator_class.set_integrator``.
        event_finder : callable, optional
            Interval root-finder function. Defaults to
            ``scipy.optimize.brentq``, and must take the equivalent positional
            arguments, ``f``, ``a``, and ``b``, and return ``x0``, where
            ``a <= x0 <= b`` and ``f(x0)`` is the zero.
        event_find_options : dict, optional
            Dictionary of keyword arguments to pass to ``event_finder``. It
            must provide a key ``'xtol'``, and it is expected that the exact
            zero lies within ``x0 +/- xtol/2``, as ``brentq`` provides.
        """

        dense_output = True
        if np.isscalar(tspan):
            t0 = 0
            tF = tspan
        elif len(tspan) == 2:
            t0 = tspan[0]
            tF = tspan[1]
        else:
            dense_output = False
            t0 = tspan[0]
            tF = tspan[-1]

        if dense_output:
            tspan = np.array([t0, tF])
        else:
            tspan = np.array(tspan)

        """
        tspan is used to indicate which times must be computed
        these are end-points for continuous time simulations, meshed data 
        points for continuous.

        """

        if ("max_step" in integrator_options) and (
            integrator_options["max_step"] == 0.0
        ):
            integrator_options = integrator_options.copy()
            # TODO: find the harmonic to ensure no skipped steps?
            if self.dt != 0.0:
                integrator_options["max_step"] = self.dt

        # generate tresult arrays; initialize x0
        results = SimulationResult(
            self.dim_state,
            self.dim_output,
            self.num_events,
            tspan,
        )

        def continuous_time_integration_step(
            t, state, output=None, for_integrator=True
        ):
            """
            function to manipulate stored states and integrator state
            to pass to between computation_step and integrator
            """
            comp_result = self.computation_step(
                t, state.reshape(-1), output, do_events=not for_integrator
            )
            if not for_integrator:
                return (state,) + comp_result[1:]
            return comp_result[0]

        # store the results from each continuous integration step
        def collect_integrator_results(t, state):
            dxdt, output, events = continuous_time_integration_step(
                t, state, for_integrator=False
            )
            test_sel = results.res_idx - np.arange(3) - 1
            if (
                t in results.t[test_sel]
                and state in results.x[test_sel, :]
                and output in results.y[test_sel, :]
            ):
                return

            # check for events here -- before saving, because it is potentially
            # invalid
            prev_events = results.e[results.res_idx - 1, :]
            if np.any(np.sign(prev_events) != np.sign(events)) & (
                results.t[results.res_idx - 1] > 0
            ):
                return -1
            else:
                results.new_result(t, state, output, events)

            if np.any(np.isnan(output)):
                warnings.warn(
                    nan_warning_message.format(
                        "variable step-size collection", t, state, output
                    )
                )
                return -1

        x0 = self.initial_condition

        y0 = self.prepare_to_integrate(t0, x0)
        # initial condition computation, populate initial condition in results

        #
        # Initial event computation
        #

        # compute first output for stateful systems

        (
            dx_dt_0,
            y0,
            e0,
        ) = self.computation_step(  # TODO: this is where logic for events needs to happen
            t0, x0, y0, do_events=True
        )
        # initial_computation[0] is saved for the next round of selected DTs
        results.new_result(t0, x0, y0, e0)
        prev_event_t = t0

        # setup the integrator
        r = integrator_class(continuous_time_integration_step)
        r.set_integrator(**integrator_options)
        r.set_initial_value(x0, t0)
        if dense_output:
            r.set_solout(collect_integrator_results)

        # main simulation loop
        t_idx = 0
        next_t = tspan[1]
        # TODO: fix extra points being added to results
        while True:
            if np.any(np.isnan(results.y[: results.res_idx, :])):
                warnings.warn(
                    nan_warning_message.format(
                        "tspan iteration (after event or meshed time-step)",
                        tspan[t_idx - 1],
                        results.x[results.res_idx - 1, :],
                        results.y[results.res_idx - 1, :],
                    )
                )
                break

            # loop to integrate until next_t, while handling events
            try:
                r.integrate(next_t)
            except KeyboardInterrupt as kbi:
                break

            """
            possible branches:
                1. if dense:
                    a. event occured, process it                    
                    b. integration completed (to next_t), so exit
                    c. some other error, abort

                2. if meshed:
                    a. event occured, process it
                    b. mesh point achieved, no event
                        i. if next_t == tF, exit
                        ii. otherwise, do the next one.
                    c. some other error, abort

                1b, 2b, require adding the final point to the system (maybe not 1b)
                1a and 2a are the same, except if not dense, maybe don't save the point?? mesh should have fixed output datasize
                or, just don't allow meshed datapoints??
                1c and 2c are the same

                TODO: decide what to do about meshed data points, stiff solvers
                TODO: figure out how to run tests that don't involve those solvers
            """

            if dense_output:
                latest_t, latest_states, latest_outputs = results.last_result()
                if r.t == next_t or np.any(np.isnan(latest_outputs)):
                    break

            (
                check_states,
                check_outputs,
                check_events,
            ) = continuous_time_integration_step(r.t, r.y, for_integrator=False)

            if np.any(np.isnan(check_outputs)):
                warnings.warn(
                    nan_warning_message.format(
                        "tspan iteration after continuous integration",
                        r.t,
                        check_states,
                        check_outputs,
                    )
                )
                break

            if not dense_output and np.all(
                np.sign(results.e[results.res_idx - 1, :]) == np.sign(check_events)
            ):
                latest_states, latest_outputs, = (
                    check_states,
                    check_outputs,
                )
                break

            if not r.successful():
                warnings.warn("Integrator quit unsuccessfully.")
                break

            #
            # need to handle event
            #
            PRE_CROSS_MINIMUM = (
                3  # interpolant requires 4, I think, so 3 before the crossing
            )

            # results index from previous event crossing
            prev_event_idx = np.where(
                results.t[: results.res_idx, None] == prev_event_t
            )[0][-1]
            prev_event_idx = max(
                min(prev_event_idx, results.res_idx - PRE_CROSS_MINIMUM), 0
            )

            # find which system(s) crossed
            event_cross_check = np.sign(results.e[results.res_idx - 1, :]) != np.sign(
                check_events
            )
            event_index_crossed = np.where(event_cross_check)[0]

            # interpolate to find first t crossing
            # holds t's where event occured
            event_ts = np.zeros(self.num_events) + r.t

            ts_to_collect = np.r_[
                results.t[prev_event_idx : results.res_idx],
            ]

            unique_ts_to_collect, unique_ts_to_collect_idx = np.unique(
                ts_to_collect, return_index=True
            )

            ts_interpolant = np.r_[unique_ts_to_collect, r.t]

            state_values = np.r_[
                results.x[prev_event_idx : results.res_idx], r.y[None, :]
            ]
            state_traj_callable = callable_from_trajectory(ts_interpolant, state_values)

            output_values = np.r_[
                results.y[prev_event_idx : results.res_idx],
                self.output_equation_function(r.t, r.y)[None, :],
            ]
            output_traj_callable = callable_from_trajectory(
                ts_interpolant, output_values
            )

            left_bracket, right_bracket = ts_interpolant[-2:]

            for event_idx in event_index_crossed:
                event_ts[event_idx] = event_finder(
                    lambda t: self.event_equation_function(
                        t, state_traj_callable(t), output_traj_callable(t)
                    )[event_idx],
                    left_bracket,
                    right_bracket,
                    **event_find_options,
                )

            next_event_t = np.min(event_ts[event_index_crossed])
            left_t = next_event_t - event_find_options["xtol"] / 2
            left_x = state_traj_callable(left_t)

            new_states, new_outputs, new_events = continuous_time_integration_step(
                left_t, left_x, for_integrator=False
            )
            results.new_result(left_t, new_states, new_outputs, new_events)

            right_t = next_event_t + event_find_options["xtol"] / 2
            right_x = state_traj_callable(right_t).reshape(-1)
            if isinstance(self, BlockDiagram):
                right_y = output_traj_callable(right_t).reshape(-1)
                right_x = self.update_equation_function(
                    right_t,
                    right_x,
                    right_y,
                    event_channels=event_index_crossed,
                )
            else:
                right_x = self.update_equation_function(
                    right_t,
                    right_x,
                    event_channels=event_index_crossed,
                )
                right_y = self.output_equation_function(right_t, right_x)

            new_states, new_outputs, new_events = continuous_time_integration_step(
                right_t, right_x, right_y, False
            )
            results.new_result(right_t, new_states, new_outputs, new_events)

            # set x (r.y), store in result as t+epsilon? if not dense,
            # add extra 1=-0
            r.set_initial_value(right_x, right_t)
            prev_event_t = right_t
            # TODO: THIS IS WHERE PREVIOUS EVENT HANDLING LOOP ENDED

        results.t = results.t[: results.res_idx]
        results.x = results.x[: results.res_idx, :]
        results.y = results.y[: results.res_idx, :]
        results.e = results.e[: results.res_idx, :]
        return results



