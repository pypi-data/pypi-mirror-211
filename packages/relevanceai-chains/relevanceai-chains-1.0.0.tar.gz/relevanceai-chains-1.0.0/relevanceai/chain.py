import json
import requests
from relevanceai._request import handle_response
from relevanceai import config
from relevanceai.auth import Auth
from relevanceai.params import Parameters


def create(name, description="", parameters={}, auth=None):
    chain = Chain(name=name, description=description, parameters=parameters, auth=auth)
    return chain


def load(id, auth=None):
    if auth is None:
        auth = config.auth
    response = requests.get(
        f"https://api-{config.auth.region}.stack.tryrelevance.com/latest/studios/{config.auth.project}/{id}",
        json={
            "filters": [
                {
                    "field": "studio_id",
                    "condition": "==",
                    "condition_value": id,
                    "filter_type": "exact_match",
                },
                {
                    "field": "project",
                    "condition": "==",
                    "condition_value": config.auth.project,
                    "filter_type": "exact_match",
                },
            ]
        },
    )
    res = handle_response(response)
    chain = Chain(name="", description="", parameters={}, id=id, auth=auth)
    return chain


def load_from_json(filepath):
    with open(filepath, "r") as f:
        chain_json = json.load(f)
    chain = Chain(
        name=chain_json["title"],
        description=chain_json["description"],
        parameters=chain_json["params_schema"]["properties"],
        id=chain_json["studio_id"],
    )
    chain.add(chain_json["transformations"]["steps"])
    return chain


class Chain:
    def __init__(
        self,
        name: str,
        description: str = "",
        parameters={},
        id: str = "test",
        auth: Auth = None,
    ):
        self.name = name
        self.description = description
        self._parameters = parameters
        self.steps = []
        self.id = id
        self.auth: Auth = config.auth if auth is None else auth

    @property
    def parameters(self):
        return Parameters(self._parameters)

    params = parameters

    def add(self, steps):
        if isinstance(steps, list):
            self.steps.extend(steps)
        else:
            self.steps.append(steps)

    def _transform_steps(self, steps):
        chain_steps = [step.steps[0] for step in steps]
        unique_ids = []
        for step in chain_steps:
            if step["name"] in unique_ids:
                raise ValueError(
                    f"Duplicate step name {step['name']}, please rename the step name with Step(step_name=step_name)."
                )
            unique_ids.append(step["name"])
        return chain_steps

    def _trigger_json(
        self, values: dict = {}, return_state: bool = True, public: bool = False
    ):
        data = {
            "return_state": return_state,
            "studio_override": {
                "public": public,
                "transformations": {"steps": self._transform_steps(self.steps)},
                "params_schema": {"properties": self.parameters.to_json()},
            },
            "params": values,
        }
        data["studio_id"] = self.id
        data["studio_override"]["studio_id"] = self.id
        return data

    def run(self, parameters={}, full_response: bool = False):
        url = f"https://api-{self.auth.region}.stack.tryrelevance.com/latest/studios/{self.auth.project}"
        response = requests.post(
            f"{url}/trigger",
            json=self._trigger_json(parameters),
            headers=self.auth.headers,
        )
        res = handle_response(response)
        if isinstance(res, dict):
            if ("errors" in res and res["errors"]) or full_response:
                return res
            elif "output" in res:
                return res["output"]
        return res

    def _json(self):
        data = {
            "title": self.name,
            "description": self.description,
            "version": "latest",
            "project": self.auth.project,
            "public": False,
            "params_schema": {"properties": self.parameters.to_json()},
            "transformations": {"steps": self.steps},
        }
        data["studio_id"] = self.id
        return data

    def deploy(self):
        url = f"https://api-{self.auth.region}.stack.tryrelevance.com/latest/studios"
        response = requests.post(
            f"{url}/bulk_update",
            json={"updates": [self._json()]},
            headers=self.auth.headers,
        )
        return handle_response(response)

    def to_json(self, filepath):
        with open(filepath, "w") as f:
            json.dump(self._json(), f)

    def reset(self):
        self.steps = []
