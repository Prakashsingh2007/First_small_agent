class AgentError(Exception):
    """The agent could not finish, and the message says why in plain words."""


class BrainUnavailable(AgentError):
    """The model behind a brain cannot be reached."""


class BrainGaveUp(AgentError):
    """The brain kept returning invalid replies."""