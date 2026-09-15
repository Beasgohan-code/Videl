# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Queue Manager

import random
from collections import defaultdict, deque
from typing import Union, Tuple, Optional, List
from ._dataclass import Media, Track

MediaItem = Union[Media, Track]


class Queue:
    def __init__(self):
        self.queues: dict[int, deque[MediaItem]] = defaultdict(deque)

    def add(self, chat_id: int, item: MediaItem) -> int:
        """Add an item to queue and return position (0-based index)."""
        self.queues[chat_id].append(item)
        return len(self.queues[chat_id]) - 1

    def check_item(self, chat_id: int, item_id: str) -> Tuple[int, Optional[MediaItem]]:
        """Check if item exists in queue."""
        pos, track = next(
            (
                (i, track)
                for i, track in enumerate(list(self.queues[chat_id]))
                if track.id == item_id
            ),
            (-1, None),
        )
        return pos, track

    def force_add(
        self, chat_id: int, item: MediaItem, remove: Union[int, bool] = False
    ) -> None:
        """Replace current playing item with new track."""
        self.remove_current(chat_id)
        self.queues[chat_id].appendleft(item)
        if remove and isinstance(remove, int):
            self.queues[chat_id].rotate(-remove)
            self.queues[chat_id].popleft()
            self.queues[chat_id].rotate(remove)

    def get_current(self, chat_id: int) -> Optional[MediaItem]:
        """Return currently playing item."""
        return self.queues[chat_id][0] if self.queues[chat_id] else None

    def get_next(self, chat_id: int, check: bool = False) -> Optional[MediaItem]:
        """Pop current track and return next track."""
        if not self.queues[chat_id]:
            return None
        if check:
            return self.queues[chat_id][1] if len(self.queues[chat_id]) > 1 else None

        self.queues[chat_id].popleft()
        return self.queues[chat_id][0] if self.queues[chat_id] else None

    def get_queue(self, chat_id: int) -> List[MediaItem]:
        """Get copy of entire playlist queue."""
        return list(self.queues[chat_id])

    def remove_current(self, chat_id: int) -> None:
        """Remove currently playing item."""
        if self.queues[chat_id]:
            self.queues[chat_id].popleft()

    def clear(self, chat_id: int) -> None:
        """Clear queue for chat."""
        self.queues[chat_id].clear()

    def shuffle(self, chat_id: int) -> bool:
        """Shuffle queued songs (keeping current song first)."""
        if len(self.queues[chat_id]) <= 2:
            return False
        q_list = list(self.queues[chat_id])
        current = q_list[0]
        remaining = q_list[1:]
        random.shuffle(remaining)
        self.queues[chat_id] = deque([current] + remaining)
        return True
