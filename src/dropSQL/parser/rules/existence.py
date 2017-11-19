from typing import *

from dropSQL.parser.expected import Expected
from dropSQL.parser.tokens import *
from dropSQL.generic import *

from dropSQL.ast import *

from . import *

__all__ = (
    'Existence',
    'NonExistence',
)


class Existence(Rule[Optional[IfExists]]):
    """
    existence
        : /* empty */
        | "if" "exists"
        ;
    """

    @classmethod
    def parse(cls, ts: TokenStream) -> Result[Optional[IfExists], Expected]:
        t = ts.gettok().and_then(caster(If))
        if not t:
            ts.ungettok()
            return Ok(None)

        t = ts.gettok().and_then(caster(Exists))
        if not t: return Err(t.err())

        return Ok(IfExists())


class NonExistence(Rule[Optional[IfNotExists]]):
    """
    non_existence
        : /* empty */
        | "if" "not" "exists"
        ;
    """

    @classmethod
    def parse(cls, ts: TokenStream) -> Result[Optional[IfNotExists], Expected]:
        t = ts.gettok().and_then(caster(If))
        if not t:
            ts.ungettok()
            return Ok(None)

        t = ts.gettok().and_then(caster(Not))
        if not t: return Err(t.err())

        t = ts.gettok().and_then(caster(Exists))
        if not t: return Err(t.err())

        return Ok(IfNotExists())
