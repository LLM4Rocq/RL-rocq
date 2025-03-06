import os
from dataclasses import dataclass
from abc import ABC, abstractmethod
from pathlib import Path

from typing import Optional
from pytanque import Pytanque, PetanqueError, Opts

@dataclass
class Response():
    """ Possible responses from the proof assistant. """
    error: str = ""
    warning: str = ""
    information: str = ""

    def is_error(self) -> bool:
        """ Tell if a response contains an error or not. """
        return len(self.error) > 0

class Interface(ABC):
    """ Abstract class for a language interface. """

    @abstractmethod
    def __init__(self, workspace: str):
        """ Initialize the interface in some workspace. """
        pass

    @abstractmethod
    def type_check(self, code: str) -> Response:
        """ Check if some code type-check. """
        pass

    @abstractmethod
    def prove(self, file: str, theorem: str, proof: str) -> Response:
        """ Try the proof `proof` for the theorem `theorem` in the file `file`. """
        pass

class RocqInterface(Interface):
    """ Rocq interface. """

    def __init__(self, workspace: str, address: str, port: str, context: bool = False, opts: Optional[Opts] = None, timeout: int = 10):
        self.workspace = workspace
        self.pet = Pytanque(address, port)
        self.pet.connect()
        self.pet.set_workspace(False, str(self.workspace))
        self.context = context
        self.timeout = timeout
        self.opts = opts

        # In some functions, type_check for example, a blank state is needed.
        # This blank state is obtained by creating a new file in the workspace and extracting its root state.
        name = "blank"
        path = Path(self.workspace, name + ".v")
        while os.path.exists(path):
            name += "0"
            path = Path(self.workspace, name + ".v")
        self.blank_state = self.pet.get_root_state(path, opts=self.opts)

    def type_check(self, code) -> Response:
        try:
            self.pet.run_tac(self.blank_state, code, opts=self.opts)
            return Response()
        except PetanqueError as err:
            return Response(error=err.message)

    def prove(self, file, theorem, proof) -> Response:
        path = Path(self.workspace, file)
        s = self.pet.start(path, theorem)
        try:
            s = self.pet.run_tac(s, proof, opts=self.opts, timeout=self.timeout)
            self.pet.run_tac(s, "Qed.")
            return Response()
        except PetanqueError as err:
            return Response(error=err.message)
