from __future__ import annotations

import inspect
import typing as typ

from dataclasses import dataclass, field

import jijmodeling as jm
import numpy as np

from jijzept.client import JijZeptClient
from jijzept.config.path_type import PATH_TYPE
from jijzept.exception.exception import (
    JijZeptSolvingFailedError,
    JijZeptSolvingUnknownError,
    JijZeptSolvingValidationError
)
from jijzept.instance_translator.instance_translator import InstanceTranslator
from jijzept.post_api import post_instance_and_query
from jijzept.response.base import APIStatus
from jijzeptlab.response import JijZeptLabResponse


@dataclass
class InputData:
    """input data for specifing problem, instance_data, and fixed_variables"""

    problem: jm.Problem
    instance_data: dict[str, list | np.ndarray] = field(default_factory=dict)
    fixed_variables: dict[str, dict[tuple[int, ...], int]] = field(default_factory=dict)


class JijZeptLabClient:
    def __init__(
        self,
        token: str | None = None,
        url: str | None = None,
        proxy: str | None = None,
        config: PATH_TYPE | None = None,
        config_env: str = "default",
    ):
        """Sets token and url.
        If you do not set any arguments, JijZept configuration file is used.
        If you set the url or token here, that will be used as the priority setting for connecting to the API.
        See JijZeptClient for details.
        Args:
            token (str | None, optional): Token string. Defaults to None.
            url (str | None, optional): API URL. Defaults to None.
            proxy (str | None, optional): Proxy URL. Defaults to None.
            config (str | None, optional): Config file path. Defaults to None.
            config_env (str, optional): configure environment name. Defaults to 'default'.
        Raises:
            TypeError: `token`, `url`, or `config` is not str.
        """
        self.client = JijZeptClient(
            url=url, token=token, proxy=proxy, config=config, config_env=config_env
        )

    def submit(
        self,
        code_string: str,
        result_variables: list[str],
        input_data: typ.Optional[InputData] = None,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str = "jijzeptlabsolver",
    ) -> JijZeptLabResponse:
        """submit job to the server

        Args:
            code_string (str): Code string.
            result_variables (list[str]): Result variables. This variables are returned as a result.
            input_data (Optional[InputData], optional): Input data for specifing problem, instance_data, and fixed_variables. Defaults to None.
            max_wait_time (int | float | None, optional): Max wait time. Defaults to None.
            sync (bool, optional): Sync. Defaults to True.
            queue_name (str, optional): Queue name. Defaults to "jijzeptlabsolver".

        Returns:
            JijZeptLabResponse: JijZeptLabResponse
        """
        instance: dict[str, typ.Any] = {
            "python_source": code_string,
        }

        if input_data is not None:
            problem = input_data.problem
            instance_data = input_data.instance_data
            fixed_variables = input_data.fixed_variables

            instance["problem"] = jm.to_serializable(problem)

            instance["instance_data"] = InstanceTranslator.instance_translate(
                instance_data
            )

            instance["fixed_variables"] = jm.utils.serialize_fixed_var(fixed_variables)

        response = post_instance_and_query(
            JijZeptLabResponse,
            client=self.client,
            instance_type="PythonCode",
            instance=instance,
            queue_name=queue_name,
            solver="JijZeptLabSolver",
            parameters={"result": result_variables},
            timeout=max_wait_time,
            sync=sync,
        )

        # Raise error if the problem is not solved.
        if response.status == APIStatus.FAILED:
            raise JijZeptSolvingFailedError(
                response.error_message.get("message", "The problem is not solved.")
            )
        elif response.status == APIStatus.UNKNOWNERROR:
            raise JijZeptSolvingUnknownError(
                response.error_message.get("message", "The problem is not solved.")
            )
        elif response.status == APIStatus.VALIDATIONERROR:
            raise JijZeptSolvingValidationError(
                response.error_message.get("message", "The problem is not solved.")
            )

        return response

    def submit_func(
        self,
        func: typ.Callable,
        result_variables: list[str],
        input_data: typ.Optional[InputData] = None,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str = "jijzeptlabsolver",
    ) -> JijZeptLabResponse:
        """submit job to the server (with function)

        Args:
            func (typ.Callable): Function.
            result_variables (list[str]): Result variables. This variables are returned as a result.
            input_data (Optional[InputData], optional): Input data for specifing problem, instance_data, and fixed_variables. Defaults to None.
            max_wait_time (int | float | None, optional): Max wait time. Defaults to None.
            sync (bool, optional): Sync. Defaults to True.
            queue_name (str, optional): Queue name. Defaults to "jijzeptlabsolver".

        Returns:
            JijZeptLabResponse: JijZeptLabResponse

        """

        # get source code
        source_lines = inspect.getsource(func).split("\n")
        # remove first and last line
        body_lines = source_lines[1:-1]
        # remove indent
        body_lines = [line.strip() for line in body_lines]
        # convert to string
        code_string = "\n".join(body_lines)
        return self.submit(
            code_string, result_variables, input_data, max_wait_time, sync, queue_name
        )

    def submit_file(
        self,
        filepath: str,
        result_variables: list[str],
        input_data: typ.Optional[InputData] = None,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str = "jijzeptlabsolver",
    ):
        """submit job to the server (with source code file)

        Args:
            filepath (str): _description_
            result_variables (list[str]): _description_
            input_data (typ.Optional[InputData], optional): _description_. Defaults to None.
            max_wait_time (int | float | None, optional): _description_. Defaults to None.
            sync (bool, optional): _description_. Defaults to True.
            queue_name (str, optional): _description_. Defaults to "jijzeptlabsolver".

        Returns:
            JijZeptLabResponse: JijZeptLabResponse
        """
        code_string: str = ""
        with open(filepath, "r") as f:
            code_string = f.read()

        return self.submit(
            code_string, result_variables, input_data, max_wait_time, sync, queue_name
        )
