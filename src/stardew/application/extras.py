"""Additional saved facts as structured results, shared by text and JSON."""

from stardew.domain.models.game_data import GameData
from stardew.domain.models.results import ExtrasPlayer, ExtrasResult, ShippedItem
from stardew.domain.models.state import GameState


def analyze_extras(state: GameState, data: GameData) -> ExtrasResult:
    players = []
    for player in state.players:
        shipped = []
        for identifier, quantity in player.collection_counts.get(
            "basicShipped", {}
        ).items():
            identifier = identifier.removeprefix("(O)")
            shipped.append(
                ShippedItem(
                    identifier,
                    data.items.name(identifier),
                    quantity,
                )
            )
        shipped.sort(
            key=lambda item: (
                (0, int(item.item_id)) if item.item_id.isdigit() else (1, item.item_id)
            )
        )
        shipped.sort(key=lambda item: -item.quantity)
        players.append(
            ExtrasPlayer(
                player.name,
                player.player_id,
                player.inventory,
                player.equipment,
                player.experience,
                player.skills,
                tuple(shipped),
            )
        )
    rarecrows = set()
    nodes = (
        state.index.objects_by_name.get("Rarecrow", ())
        if state.index is not None
        else state.snapshot.iter()
    )
    for node in nodes:
        if node.value("name") == "Rarecrow":
            rarecrow_id = node.value("parentSheetIndex") or node.value("itemId")
            if rarecrow_id:
                rarecrows.add(data.items.name(rarecrow_id, big_craftable=True))
    return ExtrasResult(
        tuple(players),
        state.world.containers,
        state.world.shared_inventories,
        tuple(sorted(rarecrows)),
        state.world.animals,
        state.world.perfection_waivers,
    )
