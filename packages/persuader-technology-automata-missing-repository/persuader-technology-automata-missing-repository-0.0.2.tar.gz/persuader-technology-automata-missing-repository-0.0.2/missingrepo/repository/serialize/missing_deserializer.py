from core.market.Market import Market
from core.missing.Context import Context
from utility.json_utility import as_data

from missingrepo.Missing import Missing


def deserialize_missing(missing) -> Missing:
    missing_info = as_data(missing, 'missing')
    context = obtain_context(as_data(missing, 'context'))
    market = obtain_market(as_data(missing, 'market'))
    description = as_data(missing, 'description')
    return Missing(missing_info, context, market, description)


def obtain_context(value):
    result = [member for name, member in Context.__members__.items() if member.value == value]
    return result[0]


def obtain_market(value):
    result = [member for name, member in Market.__members__.items() if member.value == value]
    return result[0]
