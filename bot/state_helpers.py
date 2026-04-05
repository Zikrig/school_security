from vkbottle.dispatch import ABCStateDispenser


async def clear_peer_state(dispenser: ABCStateDispenser, peer_id: int) -> None:
    if await dispenser.get(peer_id) is not None:
        await dispenser.delete(peer_id)
