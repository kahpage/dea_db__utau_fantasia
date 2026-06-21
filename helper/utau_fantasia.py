# Notes:
import sys
import json
from pathlib import Path
from typing import Any

# Add project root to sys.path (find the directory containing db_structs.py)
_root = Path(__file__).resolve().parent
while _root.parent != _root:
    if (_root / "db_structs.py").exists():
        if str(_root) not in sys.path:
            sys.path.append(str(_root))
        break
    _root = _root.parent

from db_structs import (
    Medium,
    Circle,
    Event,
    EventGroup,
    Source,
    ReliabilityTypes,
    OriginTypes,
    Location,
)

RT, OT = ReliabilityTypes, OriginTypes

PATH_HELPER = Path(__file__).parent
PATH_EVENT_GROUP = PATH_HELPER.parent
PATH_MEDIA = PATH_EVENT_GROUP / "media"


def retrieve_circles(event_name: str) -> list[Circle]:
    """Retrieve circles of given event. In the circle file has not been created, execute the creation script first."""
    circles_json_path = PATH_HELPER / event_name / "circles.json"
    if not circles_json_path.exists():
        print(
            f"Circle file for {event_name} not found, running the creation script ..."
        )
        creation_script_path = PATH_HELPER / event_name / "main.py"
        if not creation_script_path.exists():
            raise FileNotFoundError(
                f"Creation script for {event_name} not found at {creation_script_path}"
            )
        # Import main() from the creation script and execute
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            f"{event_name}.main", creation_script_path
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "main"):
                module.main()

        if not circles_json_path.exists():
            raise FileNotFoundError(
                f"Creation script {creation_script_path} failed to create {circles_json_path}"
            )

    with circles_json_path.open("r", encoding="utf-8") as f:
        circles_raw = json.load(f)
    return [Circle.load_from_json(c) for c in circles_raw]


if __name__ == "__main__":
    events: list[Event] = []
    active_events: list[int | str] = list(range(1, 14 + 1))

    i = 1  # ==== utau_fantasia1 ====
    if i in active_events:
        event_name = f"utau_fantasia{i}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "01_utaufan.gif",
                [
                    Source(
                        "https://web.archive.org/web/20140421182456/http://vocaloid-fantasia.com/utafan.htm",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "01_haichi03.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20130530090329/http://vocaloid-fantasia.com/cir-iciran03.htm",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d41280.738025225925!2d139.63619093655805!3d35.438584145120856!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x60185cfc879b30db%3A0x8d76dbf7eaf7b911!2sYokohama%20Sanbo%20Hall%20Marineria!5e0!3m2!1sen!2sfr!4v1782062083547!5m2!1sen!2sfr",
                description="横浜産貿ホール　マリネリア全面",
                sources=[
                    Source(
                        "https://web.archive.org/web/20240228191408/https://vocaloid-fantasia.com/about03.htm",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=["UTAU Fantasia", f"UTAU Fantasia {i}"],
            dates="2012.09.23",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20240228191408/https://vocaloid-fantasia.com/about03.htm",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://web.archive.org/web/20251228222107/https://vocaloid-fantasia.com/cir-iciran03.htm",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            description="Simultaneous with VOCALOID Fantasia 3.",
            # comments=None,
            last_edited="2026.06.21",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    # i =   # ==== utau_fantasia ====
    # if i in active_events:
    #     # event_name = f"utau_fantasia{i}"
    #     print(f"Processing {event_name} ...")

    #     media_ = [
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #     ]
    #     locations = [
    #         # Location(
    #         #     iframe_url="",
    #         #     description="",
    #         #     sources=[
    #         #         Source(
    #         #             "",
    #         #             (ReliabilityTypes.Reliable, OriginTypes.Official),
    #         #         )
    #         #     ],
    #         # ),
    #     ]
    #     event = Event(
    #         aliases=[f"UTAU Fantasia {i}"],
    #         dates="",
    #         circles=[],
    #         media=media_,
    #         sources=[
    #             # Source(f"Date: {}", (RT.Reliable, OT.Official)),
    #             # Source("Participating circles: ", (RT.Reliable, OT.Official)),
    #         ],
    #         locations=locations,
    #         description=None,
    #         # comments=None,
    #         # last_edited="",
    #     )

    #     # Retrieve circles
    #     # event.circles = retrieve_circles(event_name)
    #     events.append(event)
    # ==== event group ====
    media = [
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
    ]
    links = [
        # "",
    ]

    event_group = EventGroup(
        aliases=[
            # "",
        ],
        events=events,
        media=media,
        links=links,
        sources=[
            # Source(
            #     "",
            #     (ReliabilityTypes.Reliable, OriginTypes.Official),
            # ),
        ],
        comments=None,
        description=None,
        # last_edited="",
    )

    print(f"Saving {Path(__file__).stem} database...")
    event_group.save(PATH_EVENT_GROUP, indent=None)
    print("Done")
