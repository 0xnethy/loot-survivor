import asyncio
from datetime import datetime
from typing import List, NewType, Optional, Dict
import socket
import ssl

import strawberry
import aiohttp_cors
from aiohttp import web
from pymongo import MongoClient
from strawberry.aiohttp.views import GraphQLView
from indexer.indexer import LootSurvivorIndexer
from indexer.utils import felt_to_str, str_to_felt, get_key_by_value
from indexer.config import Config

config = Config()


def parse_hex(value):
    if not value.startswith("0x"):
        raise ValueError("invalid Hex value")
    return bytes.fromhex(value.replace("0x", ""))


def serialize_hex(value):
    return "0x" + value.hex()


def parse_felt(value):
    return value.to_bytes(32, "big")


def serialize_felt(value):
    return int.from_bytes(value, "big")


def parse_string(value):
    return value.encode("utf-8")


def serialize_string(value):
    return value.decode("utf-8").replace("\u0000", "")


def parse_class(value):
    felt = get_key_by_value(value, config.CLASSES)
    return felt.to_bytes(32, "big")


def serialize_class(value):
    felt = int.from_bytes(value, "big")
    return config.CLASSES.get(felt)


def parse_beast(value):
    felt = get_key_by_value(value, config.BEASTS)
    return felt.to_bytes(32, "big")


def serialize_beast(value):
    felt = int.from_bytes(value, "big")
    return config.BEASTS.get(felt)


def parse_adventurer_status(value):
    felt = get_key_by_value(value, config.ADVENTURER_STATUS)
    return felt.to_bytes(32, "big")


def serialize_adventurer_status(value):
    felt = int.from_bytes(value, "big")
    return config.ADVENTURER_STATUS.get(felt)


def parse_discovery(value):
    felt = get_key_by_value(value, config.DISCOVERY_TYPES)
    return felt.to_bytes(32, "big")


def serialize_discovery(value):
    felt = int.from_bytes(value, "big")
    return config.DISCOVERY_TYPES.get(felt)


def parse_sub_discovery(value):
    felt = get_key_by_value(value, config.SUB_DISCOVERY_TYPES)
    return felt.to_bytes(32, "big")


def serialize_sub_discovery(value):
    felt = int.from_bytes(value, "big")
    return config.SUB_DISCOVERY_TYPES.get(felt)


def parse_obstacle(value):
    felt = get_key_by_value(value, config.OBSTACLES)
    return felt.to_bytes(32, "big")


def serialize_obstacle(value):
    felt = int.from_bytes(value, "big")
    return config.OBSTACLES.get(felt)


def parse_attacker(value):
    felt = get_key_by_value(value, config.ATTACKERS)
    return felt.to_bytes(32, "big")


def serialize_attacker(value):
    felt = int.from_bytes(value, "big")
    return config.ATTACKERS.get(felt)


def parse_item(value):
    felt = get_key_by_value(value, config.ITEMS)
    return felt.to_bytes(32, "big")


def serialize_item(value):
    felt = int.from_bytes(value, "big")
    return config.ITEMS.get(felt)


def parse_material(value):
    felt = get_key_by_value(value, config.MATERIALS)
    return felt.to_bytes(32, "big")


def serialize_material(value):
    felt = int.from_bytes(value, "big")
    return config.MATERIALS.get(felt)


def parse_item_type(value):
    felt = get_key_by_value(value, config.ITEM_TYPES)
    return felt.to_bytes(32, "big")


def serialize_item_type(value):
    felt = int.from_bytes(value, "big")
    return config.ITEM_TYPES.get(felt)


def parse_special_2(value):
    felt = get_key_by_value(value, config.ITEM_NAME_PREFIXES)
    return felt.to_bytes(32, "big")


def serialize_special_2(value):
    felt = int.from_bytes(value, "big")
    if felt == 0:
        return None
    else:
        return config.ITEM_NAME_PREFIXES.get(felt)


def parse_special_3(value):
    felt = get_key_by_value(value, config.ITEM_NAME_SUFFIXES)
    return felt.to_bytes(32, "big")


def serialize_special_3(value):
    felt = int.from_bytes(value, "big")
    return config.ITEM_NAME_SUFFIXES.get(felt)


def parse_special_1(value):
    felt = get_key_by_value(value, config.ITEM_SUFFIXES)
    return felt.to_bytes(32, "big")


def serialize_special_1(value):
    felt = int.from_bytes(value, "big")
    return config.ITEM_SUFFIXES.get(felt)


def parse_item_status(value):
    felt = get_key_by_value(value, config.ITEM_STATUS)
    return felt.to_bytes(32, "big")


def serialize_item_status(value):
    felt = int.from_bytes(value, "big")
    return config.ITEM_STATUS.get(felt)


def parse_slot(value):
    felt = get_key_by_value(value, config.SLOTS)
    return felt.to_bytes(32, "big")


def serialize_slot(value):
    felt = int.from_bytes(value, "big")
    return config.SLOTS.get(felt)


def parse_adventurer(value):
    felt = get_key_by_value(value, config.ATTACKERS)
    return felt.to_bytes(32, "big")


def serialize_adventurer(value):
    felt = int.from_bytes(value, "big")
    return config.ATTACKERS.get(felt)


HexValue = strawberry.scalar(
    NewType("HexValue", bytes), parse_value=parse_hex, serialize=serialize_hex
)

FeltValue = strawberry.scalar(
    NewType("FeltValue", bytes), parse_value=parse_felt, serialize=serialize_felt
)

StringValue = strawberry.scalar(
    NewType("StringValue", bytes), parse_value=parse_string, serialize=serialize_string
)

BooleanValue = strawberry.scalar(
    NewType("BooleanValue", bytes), parse_value=parse_felt, serialize=serialize_felt
)

ClassValue = strawberry.scalar(
    NewType("ClassValue", bytes), parse_value=parse_class, serialize=serialize_class
)

BeastValue = strawberry.scalar(
    NewType("BeastValue", bytes), parse_value=parse_beast, serialize=serialize_beast
)

AdventurerStatusValue = strawberry.scalar(
    NewType("AdventurerStatusValue", bytes),
    parse_value=parse_adventurer_status,
    serialize=serialize_adventurer_status,
)

DiscoveryValue = strawberry.scalar(
    NewType("DiscoveryValue", bytes),
    parse_value=parse_discovery,
    serialize=serialize_discovery,
)

SubDiscoveryValue = strawberry.scalar(
    NewType("SubDiscoveryValue", bytes),
    parse_value=parse_sub_discovery,
    serialize=serialize_sub_discovery,
)

ObstacleValue = strawberry.scalar(
    NewType("ObstacleValue", bytes),
    parse_value=parse_obstacle,
    serialize=serialize_obstacle,
)

AttackerValue = strawberry.scalar(
    NewType("AttackerValue", bytes),
    parse_value=parse_attacker,
    serialize=serialize_attacker,
)

ItemValue = strawberry.scalar(
    NewType("ItemValue", bytes),
    parse_value=parse_item,
    serialize=serialize_item,
)

MaterialValue = strawberry.scalar(
    NewType("MaterialValue", bytes),
    parse_value=parse_material,
    serialize=serialize_material,
)

TypeValue = strawberry.scalar(
    NewType("TypeValue", bytes),
    parse_value=parse_item_type,
    serialize=serialize_item_type,
)

Special1Value = strawberry.scalar(
    NewType("Special1Value", bytes),
    parse_value=parse_special_1,
    serialize=serialize_special_1,
)

Special2Value = strawberry.scalar(
    NewType("Special2Value", bytes),
    parse_value=parse_special_2,
    serialize=serialize_special_2,
)

Special3Value = strawberry.scalar(
    NewType("Special3Value", bytes),
    parse_value=parse_special_3,
    serialize=serialize_special_3,
)

StatusValue = strawberry.scalar(
    NewType("StatusValue", bytes),
    parse_value=parse_item_status,
    serialize=serialize_item_status,
)

SlotValue = strawberry.scalar(
    NewType("SlotValue", bytes),
    parse_value=parse_slot,
    serialize=serialize_slot,
)

AttackerValue = strawberry.scalar(
    NewType("AttackerValue", bytes),
    parse_value=parse_adventurer,
    serialize=serialize_adventurer,
)


@strawberry.input
class StringFilter:
    eq: Optional[StringValue] = None
    _in: Optional[List[StringValue]] = None
    notIn: Optional[StringValue] = None
    lt: Optional[StringValue] = None
    lte: Optional[StringValue] = None
    gt: Optional[StringValue] = None
    gte: Optional[StringValue] = None
    contains: Optional[StringValue] = None
    startsWith: Optional[StringValue] = None
    endsWith: Optional[StringValue] = None


@strawberry.input
class HexValueFilter:
    eq: Optional[HexValue] = None
    _in: Optional[List[HexValue]] = None
    notIn: Optional[List[HexValue]] = None
    lt: Optional[HexValue] = None
    lte: Optional[HexValue] = None
    gt: Optional[HexValue] = None
    gte: Optional[HexValue] = None


@strawberry.input
class FeltValueFilter:
    eq: Optional[FeltValue] = None
    _in: Optional[List[FeltValue]] = None
    notIn: Optional[List[FeltValue]] = None
    lt: Optional[FeltValue] = None
    lte: Optional[FeltValue] = None
    gt: Optional[FeltValue] = None
    gte: Optional[FeltValue] = None


@strawberry.input
class DateTimeFilter:
    eq: Optional[datetime] = None
    _in: Optional[List[datetime]] = None
    notIn: Optional[List[datetime]] = None
    lt: Optional[datetime] = None
    lte: Optional[datetime] = None
    gt: Optional[datetime] = None
    gte: Optional[datetime] = None


@strawberry.input
class BooleanFilter:
    eq: Optional[bool] = None


@strawberry.input
class ClassFilter:
    eq: Optional[ClassValue] = None
    _in: Optional[List[ClassValue]] = None
    notIn: Optional[ClassValue] = None
    lt: Optional[ClassValue] = None
    lte: Optional[ClassValue] = None
    gt: Optional[ClassValue] = None
    gte: Optional[ClassValue] = None
    contains: Optional[ClassValue] = None
    startsWith: Optional[ClassValue] = None
    endsWith: Optional[ClassValue] = None


@strawberry.input
class BeastFilter:
    eq: Optional[BeastValue] = None
    _in: Optional[List[BeastValue]] = None
    notIn: Optional[BeastValue] = None
    lt: Optional[BeastValue] = None
    lte: Optional[BeastValue] = None
    gt: Optional[BeastValue] = None
    gte: Optional[BeastValue] = None
    contains: Optional[BeastValue] = None
    startsWith: Optional[BeastValue] = None
    endsWith: Optional[BeastValue] = None


@strawberry.input
class AdventurerStatusFilter:
    eq: Optional[AdventurerStatusValue] = None
    _in: Optional[List[AdventurerStatusValue]] = None
    notIn: Optional[AdventurerStatusValue] = None
    lt: Optional[AdventurerStatusValue] = None
    lte: Optional[AdventurerStatusValue] = None
    gt: Optional[AdventurerStatusValue] = None
    gte: Optional[AdventurerStatusValue] = None
    contains: Optional[AdventurerStatusValue] = None
    startsWith: Optional[AdventurerStatusValue] = None
    endsWith: Optional[AdventurerStatusValue] = None


@strawberry.input
class DiscoveryFilter:
    eq: Optional[DiscoveryValue] = None
    _in: Optional[List[DiscoveryValue]] = None
    notIn: Optional[DiscoveryValue] = None
    lt: Optional[DiscoveryValue] = None
    lte: Optional[DiscoveryValue] = None
    gt: Optional[DiscoveryValue] = None
    gte: Optional[DiscoveryValue] = None
    contains: Optional[DiscoveryValue] = None
    startsWith: Optional[DiscoveryValue] = None
    endsWith: Optional[DiscoveryValue] = None


@strawberry.input
class SubDiscoveryFilter:
    eq: Optional[SubDiscoveryValue] = None
    _in: Optional[List[SubDiscoveryValue]] = None
    notIn: Optional[SubDiscoveryValue] = None
    lt: Optional[SubDiscoveryValue] = None
    lte: Optional[SubDiscoveryValue] = None
    gt: Optional[SubDiscoveryValue] = None
    gte: Optional[SubDiscoveryValue] = None
    contains: Optional[SubDiscoveryValue] = None
    startsWith: Optional[SubDiscoveryValue] = None
    endsWith: Optional[SubDiscoveryValue] = None


@strawberry.input
class ObstacleFilter:
    eq: Optional[ObstacleValue] = None
    _in: Optional[List[ObstacleValue]] = None
    notIn: Optional[ObstacleValue] = None
    lt: Optional[ObstacleValue] = None
    lte: Optional[ObstacleValue] = None
    gt: Optional[ObstacleValue] = None
    gte: Optional[ObstacleValue] = None
    contains: Optional[ObstacleValue] = None
    startsWith: Optional[ObstacleValue] = None
    endsWith: Optional[ObstacleValue] = None


@strawberry.input
class AttackerFilter:
    eq: Optional[AttackerValue] = None


@strawberry.input
class ItemFilter:
    eq: Optional[ItemValue] = None
    _in: Optional[List[ItemValue]] = None
    notIn: Optional[ItemValue] = None
    lt: Optional[ItemValue] = None
    lte: Optional[ItemValue] = None
    gt: Optional[ItemValue] = None
    gte: Optional[ItemValue] = None
    contains: Optional[ItemValue] = None
    startsWith: Optional[ItemValue] = None
    endsWith: Optional[ItemValue] = None


@strawberry.input
class MaterialFilter:
    eq: Optional[MaterialValue] = None
    _in: Optional[List[MaterialValue]] = None
    notIn: Optional[MaterialValue] = None
    lt: Optional[MaterialValue] = None
    lte: Optional[MaterialValue] = None
    gt: Optional[MaterialValue] = None
    gte: Optional[MaterialValue] = None
    contains: Optional[MaterialValue] = None
    startsWith: Optional[MaterialValue] = None
    endsWith: Optional[MaterialValue] = None


@strawberry.input
class TypeFilter:
    eq: Optional[TypeValue] = None
    _in: Optional[List[TypeValue]] = None
    notIn: Optional[TypeValue] = None
    lt: Optional[TypeValue] = None
    lte: Optional[TypeValue] = None
    gt: Optional[TypeValue] = None
    gte: Optional[TypeValue] = None
    contains: Optional[TypeValue] = None
    startsWith: Optional[TypeValue] = None
    endsWith: Optional[TypeValue] = None


@strawberry.input
class Special1Filter:
    eq: Optional[Special1Value] = None
    _in: Optional[List[Special1Value]] = None
    notIn: Optional[Special1Value] = None
    lt: Optional[Special1Value] = None
    lte: Optional[Special1Value] = None
    gt: Optional[Special1Value] = None
    gte: Optional[Special1Value] = None
    contains: Optional[Special1Value] = None
    startsWith: Optional[Special1Value] = None
    endsWith: Optional[Special1Value] = None


@strawberry.input
class Special2Filter:
    eq: Optional[Special2Value] = None
    _in: Optional[List[Special2Value]] = None
    notIn: Optional[Special2Value] = None
    lt: Optional[Special2Value] = None
    lte: Optional[Special2Value] = None
    gt: Optional[Special2Value] = None
    gte: Optional[Special2Value] = None
    contains: Optional[Special2Value] = None
    startsWith: Optional[Special2Value] = None
    endsWith: Optional[Special2Value] = None


@strawberry.input
class Special3Filter:
    eq: Optional[Special3Value] = None
    _in: Optional[List[Special3Value]] = None
    notIn: Optional[Special3Value] = None
    lt: Optional[Special3Value] = None
    lte: Optional[Special3Value] = None
    gt: Optional[Special3Value] = None
    gte: Optional[Special3Value] = None
    contains: Optional[Special3Value] = None
    startsWith: Optional[Special3Value] = None
    endsWith: Optional[Special3Value] = None


@strawberry.input
class StatusFilter:
    eq: Optional[StatusValue] = None
    _in: Optional[List[StatusValue]] = None
    notIn: Optional[StatusValue] = None
    lt: Optional[StatusValue] = None
    lte: Optional[StatusValue] = None
    gt: Optional[StatusValue] = None
    gte: Optional[StatusValue] = None
    contains: Optional[StatusValue] = None
    startsWith: Optional[StatusValue] = None
    endsWith: Optional[StatusValue] = None


@strawberry.input
class SlotFilter:
    eq: Optional[SlotValue] = None
    _in: Optional[List[SlotValue]] = None
    notIn: Optional[SlotValue] = None
    lt: Optional[SlotValue] = None
    lte: Optional[SlotValue] = None
    gt: Optional[SlotValue] = None
    gte: Optional[SlotValue] = None
    contains: Optional[SlotValue] = None
    startsWith: Optional[SlotValue] = None
    endsWith: Optional[SlotValue] = None


@strawberry.input
class OrderByInput:
    asc: Optional[bool] = False
    desc: Optional[bool] = False


@strawberry.input
class AdventurersFilter:
    id: Optional[FeltValueFilter] = None
    lastAction: Optional[FeltValueFilter] = None
    owner: Optional[HexValueFilter] = None
    classType: Optional[ClassFilter] = None
    homeRealm: Optional[FeltValueFilter] = None
    name: Optional[StringFilter] = None
    health: Optional[FeltValueFilter] = None
    strength: Optional[FeltValueFilter] = None
    dexterity: Optional[FeltValueFilter] = None
    vitality: Optional[FeltValueFilter] = None
    intelligence: Optional[FeltValueFilter] = None
    wisdom: Optional[FeltValueFilter] = None
    charisma: Optional[FeltValueFilter] = None
    xp: Optional[FeltValueFilter] = None
    weapon: Optional[FeltValueFilter] = None
    chest: Optional[FeltValueFilter] = None
    head: Optional[FeltValueFilter] = None
    waist: Optional[FeltValueFilter] = None
    foot: Optional[FeltValueFilter] = None
    hand: Optional[FeltValueFilter] = None
    neck: Optional[FeltValueFilter] = None
    ring: Optional[FeltValueFilter] = None
    beastHealth: Optional[FeltValueFilter] = None
    statUpgrades: Optional[FeltValueFilter] = None
    gold: Optional[FeltValueFilter] = None
    createdTime: Optional[OrderByInput] = None
    lastUpdatedTime: Optional[DateTimeFilter] = None
    timestamp: Optional[DateTimeFilter] = None


@strawberry.input
class ScoresFilter:
    adventurerId: Optional[FeltValueFilter] = None
    address: Optional[HexValueFilter] = None
    rank: Optional[FeltValueFilter] = None
    xp: Optional[FeltValueFilter] = None
    txHash: Optional[HexValueFilter] = None
    scoreTime: Optional[DateTimeFilter] = None
    timestamp: Optional[DateTimeFilter] = None


@strawberry.input
class DiscoveriesFilter:
    adventurerId: Optional[FeltValueFilter] = None
    adventurerHealth: Optional[FeltValueFilter] = None
    disoveryType: Optional[StringFilter] = None
    subDiscoveryType: Optional[StringFilter] = None
    outputAmount: Optional[FeltValueFilter] = None
    obstacle: Optional[ObstacleFilter] = None
    obstacleLevel: Optional[FeltValueFilter] = None
    dodgedObstacle: Optional[BooleanFilter] = None
    damageTaken: Optional[FeltValueFilter] = None
    damageLocation: Optional[SlotFilter] = None
    xpEarnedAdventurer: Optional[FeltValueFilter] = None
    xpEarnedItems: Optional[FeltValueFilter] = None
    entity: Optional[FeltValueFilter] = None
    entityLevel: Optional[FeltValueFilter] = None
    entityHealth: Optional[FeltValueFilter] = None
    special1: Optional[Special1Filter] = None
    special2: Optional[Special2Filter] = None
    special3: Optional[Special3Filter] = None
    seed: Optional[HexValueFilter] = None
    ambushed: Optional[OrderByInput] = None
    discoveryTime: Optional[DateTimeFilter] = None
    timestamp: Optional[DateTimeFilter] = None
    txHash: Optional[HexValueFilter] = None


@strawberry.input
class BeastsFilter:
    beast: Optional[BeastFilter] = None
    adventurerId: Optional[FeltValueFilter] = None
    seed: Optional[HexValueFilter] = None
    special1: Optional[Special1Filter] = None
    special2: Optional[Special2Filter] = None
    special3: Optional[Special3Filter] = None
    health: Optional[FeltValueFilter] = None
    level: Optional[FeltValueFilter] = None
    slainOnTime: Optional[DateTimeFilter] = None
    createdTime: Optional[DateTimeFilter] = None
    lastUpdatedTime: Optional[DateTimeFilter] = None
    timestamp: Optional[DateTimeFilter] = None


@strawberry.input
class BattlesFilter:
    adventurerId: Optional[FeltValueFilter] = None
    adventurerHealth: Optional[FeltValueFilter] = None
    beast: Optional[BeastFilter] = None
    beastHealth: Optional[FeltValueFilter] = None
    beastLevel: Optional[FeltValueFilter] = None
    special1: Optional[Special1Filter] = None
    special2: Optional[Special2Filter] = None
    special3: Optional[Special3Filter] = None
    seed: Optional[HexValueFilter] = None
    attacker: Optional[AttackerFilter] = None
    fled: Optional[BooleanFilter] = None
    damageDealt: Optional[FeltValueFilter] = None
    criticalHit: Optional[BooleanFilter] = None
    damageTaken: Optional[FeltValueFilter] = None
    damageLocation: Optional[SlotFilter] = None
    xpEarnedAdventurer: Optional[FeltValueFilter] = None
    xpEarnedItems: Optional[FeltValueFilter] = None
    goldEarned: Optional[FeltValueFilter] = None
    txHash: Optional[HexValueFilter] = None
    discoveryTime: Optional[DateTimeFilter] = None
    blockTime: Optional[DateTimeFilter] = None


@strawberry.input
class ItemsFilter:
    item: Optional[ItemFilter] = None
    adventurerId: Optional[FeltValueFilter] = None
    cost: Optional[FeltValueFilter] = None
    ownerAddress: Optional[HexValueFilter] = None
    owner: Optional[BooleanFilter] = None
    equipped: Optional[BooleanFilter] = None
    createdTime: Optional[DateTimeFilter] = None
    purchasedTime: Optional[DateTimeFilter] = None
    special1: Optional[Special1Filter] = None
    special2: Optional[Special2Filter] = None
    special3: Optional[Special3Filter] = None
    xp: Optional[FeltValueFilter] = None
    lastUpdatedTime: Optional[DateTimeFilter] = None
    timestamp: Optional[DateTimeFilter] = None


@strawberry.input
class AdventurersOrderByInput:
    id: Optional[OrderByInput] = None
    lastAction: Optional[OrderByInput] = None
    owner: Optional[OrderByInput] = None
    classType: Optional[OrderByInput] = None
    homeRealm: Optional[OrderByInput] = None
    name: Optional[OrderByInput] = None
    health: Optional[OrderByInput] = None
    level: Optional[OrderByInput] = None
    strength: Optional[OrderByInput] = None
    dexterity: Optional[OrderByInput] = None
    vitality: Optional[OrderByInput] = None
    intelligence: Optional[OrderByInput] = None
    wisdom: Optional[OrderByInput] = None
    charisma: Optional[OrderByInput] = None
    xp: Optional[OrderByInput] = None
    weapon: Optional[OrderByInput] = None
    chest: Optional[OrderByInput] = None
    head: Optional[OrderByInput] = None
    waist: Optional[OrderByInput] = None
    foot: Optional[OrderByInput] = None
    hand: Optional[OrderByInput] = None
    neck: Optional[OrderByInput] = None
    ring: Optional[OrderByInput] = None
    beastHealth: Optional[OrderByInput] = None
    statUpgrades: Optional[OrderByInput] = None
    gold: Optional[OrderByInput] = None
    createdTime: Optional[OrderByInput] = None
    lastUpdatedTime: Optional[OrderByInput] = None
    timestamp: Optional[OrderByInput] = None


@strawberry.input
class ScoresOrderByInput:
    adventurerId: Optional[OrderByInput] = None
    address: Optional[OrderByInput] = None
    rank: Optional[OrderByInput] = None
    xp: Optional[OrderByInput] = None
    txHash: Optional[OrderByInput] = None
    scoreTime: Optional[OrderByInput] = None
    timestamp: Optional[OrderByInput] = None


@strawberry.input
class DiscoveriesOrderByInput:
    adventurerId: Optional[OrderByInput] = None
    adventurerHealth: Optional[OrderByInput] = None
    disoveryType: Optional[OrderByInput] = None
    subDiscoveryType: Optional[OrderByInput] = None
    outputAmount: Optional[OrderByInput] = None
    obstacle: Optional[OrderByInput] = None
    obstacleLevel: Optional[OrderByInput] = None
    dodgedObstacle: Optional[OrderByInput] = None
    damageTaken: Optional[OrderByInput] = None
    damageLocation: Optional[OrderByInput] = None
    xpEarnedAdventurer: Optional[OrderByInput] = None
    xpEarnedItems: Optional[OrderByInput] = None
    entity: Optional[OrderByInput] = None
    entityLevel: Optional[OrderByInput] = None
    entityHealth: Optional[OrderByInput] = None
    special1: Optional[OrderByInput] = None
    special2: Optional[OrderByInput] = None
    special3: Optional[OrderByInput] = None
    ambushed: Optional[OrderByInput] = None
    discoveryTime: Optional[OrderByInput] = None
    timestamp: Optional[OrderByInput] = None
    seed: Optional[OrderByInput] = None
    txHash: Optional[OrderByInput] = None


@strawberry.input
class BeastsOrderByInput:
    beast: Optional[OrderByInput] = None
    adventurerId: Optional[OrderByInput] = None
    seed: Optional[OrderByInput] = None
    special1: Optional[OrderByInput] = None
    special2: Optional[OrderByInput] = None
    special3: Optional[OrderByInput] = None
    health: Optional[OrderByInput] = None
    level: Optional[OrderByInput] = None
    slainOnTime: Optional[OrderByInput] = None
    createdTime: Optional[OrderByInput] = None
    lastUpdatedTime: Optional[OrderByInput] = None
    timestamp: Optional[OrderByInput] = None


@strawberry.input
class BattlesOrderByInput:
    adventurerId: Optional[OrderByInput] = None
    adventurerHealth: Optional[OrderByInput] = None
    beast: Optional[OrderByInput] = None
    beastHealth: Optional[OrderByInput] = None
    beastLevel: Optional[OrderByInput] = None
    special1: Optional[OrderByInput] = None
    special2: Optional[OrderByInput] = None
    special3: Optional[OrderByInput] = None
    seed: Optional[OrderByInput] = None
    attacker: Optional[OrderByInput] = None
    fled: Optional[OrderByInput] = None
    damageDealt: Optional[OrderByInput] = None
    criticalHit: Optional[OrderByInput] = None
    damageTaken: Optional[OrderByInput] = None
    damageLocation: Optional[OrderByInput] = None
    xpEarnedAdventurer: Optional[OrderByInput] = None
    xpEarnedItems: Optional[OrderByInput] = None
    goldEarned: Optional[OrderByInput] = None
    txHash: Optional[OrderByInput] = None
    discoveryTime: Optional[OrderByInput] = None
    blockTime: Optional[OrderByInput] = None
    timestamp: Optional[OrderByInput] = None


@strawberry.input
class ItemsOrderByInput:
    item: Optional[OrderByInput] = None
    adventurerId: Optional[OrderByInput] = None
    cost: Optional[OrderByInput] = None
    ownerAddress: Optional[OrderByInput] = None
    owner: Optional[OrderByInput] = None
    equipped: Optional[OrderByInput] = None
    createdTime: Optional[OrderByInput] = None
    purchasedTime: Optional[OrderByInput] = None
    special1: Optional[OrderByInput] = None
    special2: Optional[OrderByInput] = None
    special3: Optional[OrderByInput] = None
    xp: Optional[OrderByInput] = None
    lastUpdatedTime: Optional[OrderByInput] = None
    timestamp: Optional[OrderByInput] = None


@strawberry.type
class Adventurer:
    id: Optional[FeltValue]
    lastAction: Optional[FeltValue]
    owner: Optional[HexValue]
    classType: Optional[ClassValue]
    homeRealm: Optional[FeltValue]
    name: Optional[StringValue]
    health: Optional[FeltValue]
    strength: Optional[FeltValue]
    dexterity: Optional[FeltValue]
    vitality: Optional[FeltValue]
    intelligence: Optional[FeltValue]
    wisdom: Optional[FeltValue]
    charisma: Optional[FeltValue]
    xp: Optional[FeltValue]
    weapon: Optional[ItemValue]
    chest: Optional[ItemValue]
    head: Optional[ItemValue]
    waist: Optional[ItemValue]
    foot: Optional[ItemValue]
    hand: Optional[ItemValue]
    neck: Optional[ItemValue]
    ring: Optional[ItemValue]
    beastHealth: Optional[FeltValue]
    statUpgrades: Optional[FeltValue]
    gold: Optional[FeltValue]
    createdTime: Optional[datetime]
    lastUpdatedTime: Optional[datetime]
    timestamp: Optional[datetime]

    @classmethod
    def from_mongo(cls, data):
        return cls(
            id=data["id"],
            lastAction=data["lastAction"],
            owner=data["owner"],
            classType=data["classType"],
            homeRealm=data["homeRealm"],
            name=data["name"],
            health=data["health"],
            strength=data["strength"],
            dexterity=data["dexterity"],
            vitality=data["vitality"],
            intelligence=data["intelligence"],
            wisdom=data["wisdom"],
            charisma=data["charisma"],
            xp=data["xp"],
            weapon=data["weapon"],
            chest=data["chest"],
            head=data["head"],
            waist=data["waist"],
            foot=data["foot"],
            hand=data["hand"],
            neck=data["neck"],
            ring=data["ring"],
            beastHealth=data["beastHealth"],
            statUpgrades=data["statUpgrades"],
            gold=data["gold"],
            createdTime=data["createdTime"],
            lastUpdatedTime=data["lastUpdatedTime"],
            timestamp=data["timestamp"],
        )


@strawberry.type
class Score:
    adventurerId: Optional[FeltValue]
    address: Optional[HexValue]
    rank: Optional[FeltValue]
    xp: Optional[FeltValue]
    txHash: Optional[HexValue]
    scoreTime: Optional[datetime]
    timestamp: Optional[datetime]

    @classmethod
    def from_mongo(cls, data):
        return cls(
            adventurerId=data["adventurerId"],
            address=data["address"],
            rank=data["rank"],
            xp=data["xp"],
            txHash=data["txHash"],
            scoreTime=data["scoreTime"],
            timestamp=data["timestamp"],
        )


@strawberry.type
class Discovery:
    adventurerId: Optional[FeltValue]
    adventurerHealth: Optional[FeltValue]
    discoveryType: Optional[DiscoveryValue]
    subDiscoveryType: Optional[SubDiscoveryValue]
    outputAmount: Optional[FeltValue]
    obstacle: Optional[ObstacleValue]
    obstacleLevel: Optional[FeltValue]
    dodgedObstacle: Optional[BooleanValue]
    damageTaken: Optional[FeltValue]
    damageLocation: Optional[SlotValue]
    xpEarnedAdventurer: Optional[FeltValue]
    xpEarnedItems: Optional[FeltValue]
    entity: Optional[BeastValue]
    entityLevel: Optional[FeltValue]
    entityHealth: Optional[FeltValue]
    special1: Optional[Special1Value]
    special2: Optional[Special2Value]
    special3: Optional[Special3Value]
    ambushed: Optional[BooleanValue]
    discoveryTime: Optional[datetime]
    timestamp: Optional[datetime]
    seed: Optional[HexValue]
    txHash: Optional[HexValue]

    @classmethod
    def from_mongo(cls, data):
        return cls(
            adventurerId=data["adventurerId"],
            adventurerHealth=data["adventurerHealth"],
            discoveryType=data["discoveryType"],
            subDiscoveryType=data["subDiscoveryType"],
            outputAmount=data["outputAmount"],
            obstacle=data["obstacle"],
            obstacleLevel=data["obstacleLevel"],
            dodgedObstacle=data["dodgedObstacle"],
            damageTaken=data["damageTaken"],
            damageLocation=data["damageLocation"],
            xpEarnedAdventurer=data["xpEarnedAdventurer"],
            xpEarnedItems=data["xpEarnedItems"],
            entity=data["entity"],
            entityLevel=data["entityLevel"],
            entityHealth=data["entityHealth"],
            special1=data["special1"],
            special2=data["special2"],
            special3=data["special3"],
            ambushed=data["ambushed"],
            discoveryTime=data["discoveryTime"],
            timestamp=data["timestamp"],
            seed=data["seed"],
            txHash=data["txHash"],
        )


@strawberry.type
class Beast:
    beast: Optional[BeastValue] = None
    adventurerId: Optional[FeltValue] = None
    seed: Optional[HexValue] = None
    special1: Optional[Special1Value] = None
    special2: Optional[Special2Value] = None
    special3: Optional[Special3Value] = None
    health: Optional[FeltValue] = None
    level: Optional[FeltValue] = None
    slainOnTime: Optional[datetime] = None
    createdTime: Optional[datetime] = None
    lastUpdatedTime: Optional[datetime] = None
    timestamp: Optional[datetime] = None

    @classmethod
    def from_mongo(cls, data):
        return cls(
            beast=data["beast"],
            adventurerId=data["adventurerId"],
            seed=data["seed"],
            special1=data["special1"],
            special2=data["special2"],
            special3=data["special3"],
            health=data["health"],
            level=data["level"],
            slainOnTime=data["slainOnTime"],
            createdTime=data["createdTime"],
            lastUpdatedTime=data["lastUpdatedTime"],
            timestamp=data["timestamp"],
        )


@strawberry.type
class Battle:
    adventurerId: Optional[FeltValue]
    adventurerHealth: Optional[FeltValue]
    beast: Optional[BeastValue]
    beastHealth: Optional[FeltValue]
    beastLevel: Optional[FeltValue]
    special1: Optional[Special1Value]
    special2: Optional[Special2Value]
    special3: Optional[Special3Value]
    seed: Optional[HexValue]
    attacker: Optional[AttackerValue]
    fled: Optional[BooleanValue]
    damageDealt: Optional[FeltValue]
    criticalHit: Optional[bool]
    damageTaken: Optional[FeltValue]
    damageLocation: Optional[SlotValue]
    xpEarnedAdventurer: Optional[FeltValue]
    xpEarnedItems: Optional[FeltValue]
    goldEarned: Optional[FeltValue]
    txHash: Optional[HexValue]
    discoveryTime: Optional[datetime]
    blockTime: Optional[datetime]
    timestamp: Optional[datetime]

    @classmethod
    def from_mongo(cls, data):
        return cls(
            adventurerId=data["adventurerId"],
            adventurerHealth=data["adventurerHealth"],
            beast=data["beast"],
            beastHealth=data["beastHealth"],
            beastLevel=data["beastLevel"],
            special1=data["special1"],
            special2=data["special2"],
            special3=data["special3"],
            seed=data["seed"],
            attacker=data["attacker"],
            fled=data["fled"],
            damageDealt=data["damageDealt"],
            criticalHit=data["criticalHit"],
            damageTaken=data["damageTaken"],
            damageLocation=data["damageLocation"],
            xpEarnedAdventurer=data["xpEarnedAdventurer"],
            xpEarnedItems=data["xpEarnedItems"],
            goldEarned=data["goldEarned"],
            txHash=data["txHash"],
            discoveryTime=data["discoveryTime"],
            blockTime=data["blockTime"],
            timestamp=data["timestamp"],
        )


@strawberry.type
class Item:
    item: Optional[ItemValue]
    adventurerId: Optional[FeltValue]
    cost: Optional[FeltValue]
    ownerAddress: Optional[HexValue]
    owner: Optional[bool]
    equipped: Optional[bool]
    createdTime: Optional[datetime]
    purchasedTime: Optional[datetime]
    special1: Optional[Special1Value]
    special2: Optional[Special2Value]
    special3: Optional[Special3Value]
    xp: Optional[FeltValue]
    lastUpdatedTime: Optional[datetime]
    timestamp: Optional[datetime]

    @classmethod
    def from_mongo(cls, data):
        return cls(
            item=data["item"],
            adventurerId=data["adventurerId"],
            cost=data["cost"],
            ownerAddress=data["ownerAddress"],
            owner=data["owner"],
            equipped=data["equipped"],
            createdTime=data["createdTime"],
            purchasedTime=data["purchasedTime"],
            special1=data["special1"],
            special2=data["special2"],
            special3=data["special3"],
            xp=data["xp"],
            lastUpdatedTime=data["lastUpdatedTime"],
            timestamp=data["timestamp"],
        )


def get_str_filters(where: StringFilter) -> List[Dict]:
    filter = {}
    if where.eq:
        filter = where.eq
    if where._in:
        filter["$in"] = where._in
    if where.notIn:
        filter["$nin"] = where.notIn
    if where.lt:
        filter["$lt"] = where.lt
    if where.lte:
        filter["$lte"] = where.lte
    if where.gt:
        filter["$gt"] = where.gt
    if where.gte:
        filter["$gte"] = where.gte
    if where.contains:
        filter["$regex"] = where.contains
    if where.startsWith:
        filter["$regex"] = "^" + where.startsWith
    if where.endsWith:
        filter["$regex"] = where.endsWith + "$"

    return filter


def get_felt_filters(where: FeltValueFilter) -> List[Dict]:
    filter = {}
    if where.eq:
        filter = where.eq
    if where._in:
        filter["$in"] = where._in
    if where.notIn:
        filter["$nin"] = where.notIn
    if where.lt:
        filter["$lt"] = where.lt
    if where.lte:
        filter["$lte"] = where.lte
    if where.gt:
        filter["$gt"] = where.gt
    if where.gte:
        filter["$gte"] = where.gte

    return filter


def get_hex_filters(where: HexValueFilter) -> List[Dict]:
    filter = {}
    if where.eq:
        filter = where.eq
    if where._in:
        filter["$in"] = where._in
    if where.notIn:
        filter["$nin"] = where.notIn
    if where.lt:
        filter["$lt"] = where.lt
    if where.lte:
        filter["$lte"] = where.lte
    if where.gt:
        filter["$gt"] = where.gt
    if where.gte:
        filter["$gte"] = where.gte

    return filter


def get_date_filters(where: DateTimeFilter) -> List[Dict]:
    filter = {}
    if where.eq:
        filter = where.eq
    if where._in:
        filter["$in"] = where._in
    if where.notIn:
        filter["$nin"] = where.notIn
    if where.lt:
        filter["$lt"] = where.lt
    if where.lte:
        filter["$lte"] = where.lte
    if where.gt:
        filter["$gt"] = where.gt
    if where.gte:
        filter["$gte"] = where.gte

    return filter


def get_bool_filters(where: BooleanFilter) -> List[Dict]:
    filter = {}
    if where.eq:
        filter = where.eq
    return filter


def process_filters(obj, prefix=None):
    filters = {}
    for key, value in obj.__dict__.items():
        if value is not None:
            filter_key = f"{prefix}.{key}" if prefix else key
            filters[filter_key] = value
    return filters


def get_adventurers(
    info,
    where: Optional[AdventurersFilter] = {},
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
    orderBy: Optional[AdventurersOrderByInput] = {},
) -> List[Adventurer]:
    db = info.context["db"]

    filter = {"_chain.valid_to": None}

    if where:
        processed_filters = process_filters(where)
        for key, value in processed_filters.items():
            if (
                isinstance(value, StringFilter)
                | isinstance(value, ClassFilter)
                | isinstance(value, AdventurerStatusFilter)
            ):
                filter[key] = get_str_filters(value)
            elif isinstance(value, HexValueFilter):
                filter[key] = get_hex_filters(value)
            elif isinstance(value, DateTimeFilter):
                filter[key] = get_date_filters(value)
            elif isinstance(value, FeltValueFilter):
                filter[key] = get_felt_filters(value)
            elif isinstance(value, BooleanFilter):
                filter[key] = get_bool_filters(value)

    sort_options = {k: v for k, v in orderBy.__dict__.items() if v is not None}

    sort_var = "updated_at"
    sort_dir = -1

    for key, value in sort_options.items():
        if value.asc:
            sort_var = key
            sort_dir = 1
            break
        if value.desc:
            sort_var = key
            sort_dir = -1
            break

    query = (
        db["adventurers"].find(filter).skip(skip).limit(limit).sort(sort_var, sort_dir)
    )

    return [Adventurer.from_mongo(t) for t in query]


def get_scores(
    info,
    where: Optional[ScoresFilter] = {},
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
    orderBy: Optional[ScoresOrderByInput] = {},
) -> List[Score]:
    db = info.context["db"]

    filter = {"_chain.valid_to": None}

    if where:
        processed_filters = process_filters(where)
        for key, value in processed_filters.items():
            if isinstance(value, StringFilter):
                filter[key] = get_str_filters(value)
            elif isinstance(value, HexValueFilter):
                filter[key] = get_hex_filters(value)
            elif isinstance(value, DateTimeFilter):
                filter[key] = get_date_filters(value)
            elif isinstance(value, FeltValueFilter):
                filter[key] = get_felt_filters(value)

    sort_options = {k: v for k, v in orderBy.__dict__.items() if v is not None}

    sort_var = "updated_at"
    sort_dir = -1

    for key, value in sort_options.items():
        if value.asc:
            sort_var = key
            sort_dir = 1
            break
        if value.desc:
            sort_var = key
            sort_dir = -1
            break

    query = db["scores"].find(filter).skip(skip).limit(limit).sort(sort_var, sort_dir)

    return [Score.from_mongo(t) for t in query]


def get_discoveries(
    info,
    where: Optional[DiscoveriesFilter] = {},
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
    orderBy: Optional[DiscoveriesOrderByInput] = {},
) -> List[Discovery]:
    db = info.context["db"]

    filter = {"_chain.valid_to": None}

    if where:
        processed_filters = process_filters(where)
        for key, value in processed_filters.items():
            if (
                isinstance(value, StringFilter)
                | isinstance(value, DiscoveryFilter)
                | isinstance(value, SubDiscoveryFilter)
                | isinstance(value, SlotFilter)
            ):
                filter[key] = get_str_filters(value)
            elif isinstance(value, HexValueFilter):
                filter[key] = get_hex_filters(value)
            elif isinstance(value, DateTimeFilter):
                filter[key] = get_date_filters(value)
            elif isinstance(value, FeltValueFilter):
                filter[key] = get_felt_filters(value)

    sort_options = {k: v for k, v in orderBy.__dict__.items() if v is not None}

    sort_var = "updated_at"
    sort_dir = -1

    for key, value in sort_options.items():
        if value.asc:
            sort_var = key
            sort_dir = 1
            break
        if value.desc:
            sort_var = key
            sort_dir = -1
            break

    query = (
        db["discoveries"].find(filter).skip(skip).limit(limit).sort(sort_var, sort_dir)
    )

    return [Discovery.from_mongo(t) for t in query]


def get_beasts(
    info,
    where: Optional[BeastsFilter] = {},
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
    orderBy: Optional[BeastsOrderByInput] = {},
) -> List[Discovery]:
    db = info.context["db"]

    filter = {"_chain.valid_to": None}

    if where:
        processed_filters = process_filters(where)
        for key, value in processed_filters.items():
            if (
                isinstance(value, StringFilter)
                | isinstance(value, BeastFilter)
                | isinstance(value, Special1Filter)
                | isinstance(value, Special2Filter)
                | isinstance(value, Special3Filter)
            ):
                filter[key] = get_str_filters(value)
            elif isinstance(value, HexValueFilter):
                filter[key] = get_hex_filters(value)
            elif isinstance(value, DateTimeFilter):
                filter[key] = get_date_filters(value)
            elif isinstance(value, FeltValueFilter):
                filter[key] = get_felt_filters(value)

    sort_options = {k: v for k, v in orderBy.__dict__.items() if v is not None}

    sort_var = "updated_at"
    sort_dir = -1

    for key, value in sort_options.items():
        if value.asc:
            sort_var = key
            sort_dir = 1
            break
        if value.desc:
            sort_var = key
            sort_dir = -1
            break

    query = db["beasts"].find(filter).skip(skip).limit(limit).sort(sort_var, sort_dir)

    return [Beast.from_mongo(t) for t in query]


def get_battles(
    info,
    where: Optional[BattlesFilter] = {},
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
    orderBy: Optional[BattlesOrderByInput] = {},
) -> List[Battle]:
    db = info.context["db"]

    filter = {"_chain.valid_to": None}

    if where:
        processed_filters = process_filters(where)
        for key, value in processed_filters.items():
            if isinstance(value, StringFilter) | isinstance(value, AttackerFilter):
                filter[key] = get_str_filters(value)
            elif isinstance(value, HexValueFilter):
                filter[key] = get_hex_filters(value)
            elif isinstance(value, DateTimeFilter):
                filter[key] = get_date_filters(value)
            elif isinstance(value, FeltValueFilter):
                filter[key] = get_felt_filters(value)
            elif isinstance(value, BooleanFilter):
                filter[key] = get_bool_filters(value)

    sort_options = {k: v for k, v in orderBy.__dict__.items() if v is not None}

    sort_var = "updated_at"
    sort_dir = -1

    for key, value in sort_options.items():
        if value.asc:
            sort_var = key
            sort_dir = 1
            break
        if value.desc:
            sort_var = key
            sort_dir = -1
            break

    query = db["battles"].find(filter).skip(skip).limit(limit).sort(sort_var, sort_dir)

    return [Battle.from_mongo(t) for t in query]


def get_items(
    info,
    where: Optional[ItemsFilter] = {},
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
    orderBy: Optional[ItemsOrderByInput] = {},
) -> List[Item]:
    db = info.context["db"]

    filter = {"_chain.valid_to": None}

    if where:
        processed_filters = process_filters(where)
        for key, value in processed_filters.items():
            if (
                isinstance(value, StringFilter)
                | isinstance(value, ItemFilter)
                | isinstance(value, SlotFilter)
                | isinstance(value, TypeFilter)
                | isinstance(value, MaterialFilter)
                | isinstance(value, Special1Filter)
                | isinstance(value, Special2Filter)
                | isinstance(value, Special3Filter)
                | isinstance(value, StatusFilter)
            ):
                filter[key] = get_str_filters(value)
            elif isinstance(value, HexValueFilter):
                filter[key] = get_hex_filters(value)
            elif isinstance(value, DateTimeFilter):
                filter[key] = get_date_filters(value)
            elif isinstance(value, FeltValueFilter):
                filter[key] = get_felt_filters(value)
            elif isinstance(value, BooleanFilter):
                filter[key] = get_bool_filters(value)

    sort_options = {k: v for k, v in orderBy.__dict__.items() if v is not None}

    sort_var = "updated_at"
    sort_dir = -1

    for key, value in sort_options.items():
        if value.asc:
            sort_var = key
            sort_dir = 1
            break
        if value.desc:
            sort_var = key
            sort_dir = -1
            break
    query = db["items"].find(filter).skip(skip).limit(limit).sort(sort_var, sort_dir)

    return [Item.from_mongo(t) for t in query]


@strawberry.type
class Query:
    adventurers: List[Adventurer] = strawberry.field(resolver=get_adventurers)
    scores: List[Score] = strawberry.field(resolver=get_scores)
    discoveries: List[Discovery] = strawberry.field(resolver=get_discoveries)
    beasts: List[Beast] = strawberry.field(resolver=get_beasts)
    battles: List[Battle] = strawberry.field(resolver=get_battles)
    items: List[Item] = strawberry.field(resolver=get_items)


class IndexerGraphQLView(GraphQLView):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self._db = db

    async def get_context(self, _request, _response):
        return {"db": self._db}


async def run_graphql_api(mongo_goerli=None, mongo_mainnet=None, port="8080"):
    mongo_goerli = MongoClient(mongo_goerli)
    mongo_mainnet = MongoClient(mongo_mainnet)
    db_name_goerli = "mongo-goerli".replace("-", "_")
    db_name_mainnet = "mongo-mainnet".replace("-", "_")
    db_goerli = mongo_goerli[db_name_goerli]
    db_mainnet = mongo_mainnet[db_name_mainnet]

    schema = strawberry.Schema(query=Query)
    view_goerli = IndexerGraphQLView(db_goerli, schema=schema)
    view_mainnet = IndexerGraphQLView(db_mainnet, schema=schema)

    app = web.Application()
    # app.router.add_route("*", "/graphql", view_goerli)

    cors = aiohttp_cors.setup(app)
    resource_goerli = cors.add(app.router.add_resource("/goerli-graphql"))
    resource_mainnet = cors.add(app.router.add_resource("/graphql"))

    cors.add(
        resource_goerli.add_route("POST", view_goerli),
        {
            "*": aiohttp_cors.ResourceOptions(
                expose_headers="*", allow_headers="*", allow_methods="*"
            ),
        },
    )
    cors.add(
        resource_goerli.add_route("GET", view_goerli),
        {
            "*": aiohttp_cors.ResourceOptions(
                expose_headers="*", allow_headers="*", allow_methods="*"
            ),
        },
    )

    cors.add(
        resource_mainnet.add_route("POST", view_mainnet),
        {
            "*": aiohttp_cors.ResourceOptions(
                expose_headers="*", allow_headers="*", allow_methods="*"
            ),
        },
    )
    cors.add(
        resource_mainnet.add_route("GET", view_mainnet),
        {
            "*": aiohttp_cors.ResourceOptions(
                expose_headers="*", allow_headers="*", allow_methods="*"
            ),
        },
    )

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(port))
    await site.start()

    print(f"GraphQL server started on port {port}")

    while True:
        await asyncio.sleep(5_000)
