class EntitySpecificationNotFoundException(Exception):
    """The entity specification can not be found."""


class AgentSpecificationNotFoundException(Exception):
    """The agent specification can not be found."""


class ActivitySpecificationNotFoundException(Exception):
    """The activity specification can not be found."""


class InvalidEntitySpecificationException(Exception):
    """The entity specification is invalid."""


class InvalidActivitySpecificationException(Exception):
    """The activity specification is invalid."""


class PrimaryKeyAttributeNotDefinedException(Exception):
    """The primary key attribute has no value."""


class InvalidRuleSpecificationException(Exception):
    """The rule specification is invalid."""


class NoRuleFoundException(Exception):
    """The rule for the event type can not be found."""


class InvalidRuleResultException(Exception):
    """The rule do not return an activity."""


class InvalidActivityException(Exception):
    """The activity is invalid."""


class ActivityAlreadyDefinedException(Exception):
    """The activity is already defined."""


class EntityAlreadyDefinedException(Exception):
    """The entity is already defined."""


class InvalidSpecificationException(Exception):
    """The specification is neither an entity nor an activity specification."""
