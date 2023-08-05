from decimal import Decimal
from typing import Optional, Type, TypeVar

import yaml

from . import logger
from .nameddps import (
    CompositeNamedDP,
    Connection,
    ModelFunctionality,
    ModelResource,
    NodeFunctionality,
    NodeResource,
    SimpleWrap,
)
from .posets import FinitePoset, Numbers, Poset, PosetProduct
from .primitivedps import (
    AmbientConversion,
    CatalogueDP,
    Constant,
    DPLoop2,
    DPSeries,
    EntryInfo,
    IdentityDP,
    JoinNDP,
    Limit,
    M_Ceil_DP,
    M_FloorFun_DP,
    M_Fun_AddConstant_DP,
    M_Fun_AddMany_DP,
    M_Fun_MultiplyConstant_DP,
    M_Fun_MultiplyMany_DP,
    M_Power_DP,
    M_Res_AddConstant_DP,
    M_Res_AddMany_DP,
    M_Res_DivideConstant_DP,
    M_Res_MultiplyConstant_DP,
    M_Res_MultiplyMany_DP,
    MeetNDualDP,
    Mux,
    ParallelDP,
    PrimitiveDP,
    UnitConversion,
    ValueFromPoset,
)
from .solution_interface import Interval, LowerSet, UpperSet

loaders = {}

__all__ = [
    "load_repr1",
    "loader_for",
    "parse_yaml_value",
]


def loader_for(classname: str):
    def dc(f):
        if classname in loaders:
            msg = f"Already registered loader for {classname!r}"
            raise ValueError(msg)
        loaders[classname] = f
        return f

    return dc


@loader_for("PosetProduct")
def load_PosetProduct(ob: dict):
    subs = []
    for p in ob["subs"]:
        p = load_repr1(p, Poset)
        subs.append(p)

    return PosetProduct(subs=subs)


def _load_DP_fields(ob: dict) -> dict:
    description = ob["$schema"].get("description", None)
    F = load_repr1(ob["F"], Poset)
    R = load_repr1(ob["R"], Poset)
    fields = dict(description=description, F=F, R=R)

    if "vu" in ob:
        fields["vu"] = load_repr1(ob["vu"], ValueFromPoset)
    if "c" in ob:
        fields["c"] = load_repr1(ob["c"], ValueFromPoset)
    if "opspace" in ob:
        fields["opspace"] = load_repr1(ob["opspace"], Poset)
    if "common" in ob:
        fields["common"] = load_repr1(ob["common"], Poset)
    if "C" in ob:
        fields["opspace"] = load_repr1(ob["C"], Poset)
    if "factor" in ob:
        from fractions import Fraction

        fields["factor"] = Fraction(ob["factor"])
    return fields


@loader_for("ValueFromPoset")
def load_ValueFromPoset(ob: dict):
    poset = load_repr1(ob["poset"], Poset)
    value = ob["value"]
    value = parse_yaml_value(poset, value)
    return ValueFromPoset(value=value, poset=poset)


@loader_for("CatalogueDP")
def load_CatalogueDP(ob: dict):
    fields = _load_DP_fields(ob)
    entries = fields["entries"] = {}
    for k, v in ob["entries"].items():
        entries[k] = EntryInfo(**v)
    return CatalogueDP(**fields)


@loader_for("M_Res_MultiplyConstant_DP")
def load_M_Res_MultiplyConstant_DP(ob: dict):
    fields = _load_DP_fields(ob)
    return M_Res_MultiplyConstant_DP(**fields)


@loader_for("M_Res_DivideConstant_DP")
def load_M_Res_DivideConstant_DP(ob: dict):
    fields = _load_DP_fields(ob)
    return M_Res_DivideConstant_DP(**fields)


@loader_for("IdentityDP")
def load_Identity_DP(ob: dict):
    fields = _load_DP_fields(ob)
    return IdentityDP(**fields)


@loader_for("Mux")
def load_Mux(ob: dict):
    fields = _load_DP_fields(ob)
    fields["coords"] = ob["coords"]
    return Mux(**fields)


@loader_for("DPLoop2")
def load_DPLoop2(ob: dict):
    fields = _load_DP_fields(ob)
    fields["dp"] = load_repr1(ob["dp1"], PrimitiveDP)
    return DPLoop2(**fields)


@loader_for("M_Fun_MultiplyConstant_DP")
def load_M_Fun_MultiplyConstant_DP(ob: dict):
    fields = _load_DP_fields(ob)
    return M_Fun_MultiplyConstant_DP(**fields)


@loader_for("M_Res_AddConstant_DP")
def load_M_Res_AddConstant_DP(ob: dict):
    fields = _load_DP_fields(ob)
    return M_Res_AddConstant_DP(**fields)


@loader_for("M_Fun_AddMany_DP")
def load_M_Fun_AddMany_DP(ob: dict):
    fields = _load_DP_fields(ob)
    return M_Fun_AddMany_DP(**fields)


@loader_for("M_Res_AddMany_DP")
def load_M_Res_AddMany_DP(ob: dict):
    fields = _load_DP_fields(ob)
    return M_Res_AddMany_DP(**fields)


@loader_for("M_Res_MultiplyMany_DP")
def load_M_Res_MultiplyMany_DP(ob: dict):
    fields = _load_DP_fields(ob)
    return M_Res_MultiplyMany_DP(**fields)


@loader_for("M_Fun_MultiplyMany_DP")
def load_M_Fun_MultiplyMany_DP(ob: dict):
    fields = _load_DP_fields(ob)

    return M_Fun_MultiplyMany_DP(**fields)


@loader_for("M_Power_DP")
def load_M_Power_DP(ob: dict):
    fields = _load_DP_fields(ob)

    return M_Power_DP(**fields, num=ob["num"], den=ob["den"])


@loader_for("M_Ceil_DP")
def load_M_Ceil_DP(ob: dict):
    fields = _load_DP_fields(ob)

    return M_Ceil_DP(**fields)


@loader_for("M_FloorFun_DP")
def load_M_FloorFun_DP(ob: dict):
    fields = _load_DP_fields(ob)

    return M_FloorFun_DP(**fields)


@loader_for("Conversion")
def load_Conversion(ob: dict):
    fields = _load_DP_fields(ob)

    raise NotImplementedError(ob)
    return PrimitiveDP(**fields)


@loader_for("SeriesN")
def load_SeriesN(ob: dict):
    fields = _load_DP_fields(ob)

    subs = []
    for dp in ob["dps"]:
        dp = load_repr1(dp, PrimitiveDP)
        subs.append(dp)

    return DPSeries(**fields, subs=subs)


@loader_for("ParallelN")
def load_ParallelN(ob: dict):
    fields = _load_DP_fields(ob)

    subs = []
    for dp in ob["dps"]:
        dp = load_repr1(dp, PrimitiveDP)
        subs.append(dp)

    return ParallelDP(**fields, subs=subs)


#
# @loader_for('M_Ceil_DP')
# def load_M_Ceil_DP(ob: dict):
#     F = load_repr1(ob['F'], Poset)
#     R = load_repr1(ob['R'], Poset)
#
#     return PrimitiveDP(F=F, R=R)


@loader_for("M_Fun_AddConstant_DP")
def load_M_Fun_AddConstant_DP(ob: dict):
    fields = _load_DP_fields(ob)

    return M_Fun_AddConstant_DP(**fields)


@loader_for("AmbientConversion")
def load_AmbientConversion(ob: dict):
    fields = _load_DP_fields(ob)

    return AmbientConversion(**fields)


@loader_for("UnitConversion")
def load_UnitConversion(ob: dict):
    fields = _load_DP_fields(ob)
    return UnitConversion(**fields)


@loader_for("JoinNDP")
def load_JoinNDP(ob: dict):
    fields = _load_DP_fields(ob)
    return JoinNDP(**fields)


@loader_for("MeetNDualDP")
def load_MeetNDualDP(ob: dict):
    fields = _load_DP_fields(ob)
    return MeetNDualDP(**fields)


@loader_for("Limit")
def load_Limit(ob: dict):
    fields = _load_DP_fields(ob)
    return Limit(**fields)


@loader_for("Constant")
def load_Constant(ob: dict):
    fields = _load_DP_fields(ob)
    return Constant(**fields)


#
# @loader_for('M_Fun_MultiplyConstant_DP')
# def load_M_Fun_MultiplyConstant_DP(ob: dict):
#     F = load_repr1(ob['F'], Poset)
#     R = load_repr1(ob['R'], Poset)
#
#     return PrimitiveDP(F=F, R=R)


@loader_for("CompositeNamedDP")
def load_CompositeNamedDP(ob: dict):
    functionalities = ob["functionalities"]
    resources = ob["resources"]

    functionalities = {k: load_repr1(v, Poset) for k, v in functionalities.items()}
    resources = {k: load_repr1(v, Poset) for k, v in resources.items()}
    loaded_nodes = {}
    nodes = ob["nodes"]
    for k, v in nodes.items():
        node = load_repr1(v)
        loaded_nodes[k] = node
    connections = []

    for c in ob["connections"]:
        source = c["from"]
        target = c["to"]
        if "node" in source:
            source = NodeResource(source["node"], source["node_resource"])
        else:
            source = ModelFunctionality(source["functionality"])

        if "node" in target:
            target = NodeFunctionality(target["node"], target["node_functionality"])
        else:
            target = ModelResource(target["resource"])

        connections.append(Connection(source=source, target=target))

    return CompositeNamedDP(
        functionalities=functionalities, resources=resources, nodes=loaded_nodes, connections=connections
    )


@loader_for("SimpleWrap")
def load_SimpleWrap(ob: dict):
    functionalities = {}
    for k, v in ob["functionalities"].items():
        functionalities[k] = load_repr1(v, Poset)
    resources = {}
    for k, v in ob["resources"].items():
        resources[k] = load_repr1(v, Poset)
    dp = load_repr1(ob["dp"], PrimitiveDP)
    return SimpleWrap(functionalities=functionalities, resources=resources, dp=dp)


@loader_for("FinitePoset")
def load_FinitePoset(ob: dict):
    elements = ob["elements"]
    relations = ob["relations"]
    relations = set(tuple(x) for x in relations)
    elements = set(elements)
    return FinitePoset(elements=elements, relations=relations)


@loader_for("Interval")
def load_Interval(ob: dict):
    pessimistic = load_repr1(ob["pessimistic"])
    optimistic = load_repr1(ob["optimistic"])
    return Interval(pessimistic=pessimistic, optimistic=optimistic)


@loader_for("LowerSet")
def load_LowerSet(ob: dict):
    maximals = ob["maximals"]
    return LowerSet(maximals=maximals)


@loader_for("UpperSet")
def load_UpperSet(ob: dict):
    minimals = ob["minimals"]
    return UpperSet(minimals=minimals)


@loader_for("Numbers")
def load_Numbers(ob: dict):
    bottom = Decimal(ob["bottom"])
    top = Decimal(ob["top"])
    units = ob.get("units", "")
    step = Decimal(ob.get("step", 0))
    return Numbers(bottom=bottom, top=top, step=step, units=units)


# write the implementation for `loader_for` that allows to  register
# a function for a given class name

X = TypeVar("X")


def load_repr1(data: dict, T: Optional[Type[X]] = None) -> X:
    if "$schema" not in data:
        raise ValueError("Missing $schema")
    schema = data["$schema"]
    title = schema.get("title", None)
    if title not in loaders:
        msg = f"Cannot find loader for {title!r}: known are {list(loaders)}"
        raise ValueError(msg)
    loader = loaders[title]
    try:
        return loader(data)
    except Exception as e:
        datas = yaml.dump(data, allow_unicode=True)
        logger.exception("Error while loading %r\n%s", title, datas, exc_info=e)
        msg = f"Error while loading {title!r}:"
        raise ValueError(msg) from e


def parse_yaml_value(poset: Poset, ob: object) -> object:
    match poset:
        case Numbers():
            if not isinstance(ob, (int, str, float, bool)):
                msg = "For Poset of numbers, expected string or int, got %s" % type(ob)
                raise ValueError(msg)
            return Decimal(ob)
        case FinitePoset():
            return ob
        case PosetProduct(subs):
            if not isinstance(ob, list):
                msg = "Expected list, got %s" % type(ob)
                raise ValueError(msg)
            val = []
            for el, sub in zip(ob, subs):
                el = parse_yaml_value(sub, el)
                val.append(el)
            return tuple(val)
        case _:
            raise NotImplementedError(type(poset))
