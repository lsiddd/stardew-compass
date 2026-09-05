"""Report assembly: one XML parse, isolated rule state, deterministic sections."""

from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import time
from . import __version__
from .extras import extras_text
from .formatting import heading, text_of
from .query import Document
from .rng import install
from .runtime import Obj, base_environment, call, get
from .save import Save

CHECKUP_SECTIONS = (
    "Summary",
    "Money",
    "Skills",
    "SkillMastery",
    "Quests",
    "SpecialOrders",
    "Monsters",
    "Stardrops",
    "Family",
    "Social",
    "Cooking",
    "Crafting",
    "Fishing",
    "BasicShipping",
    "CropShipping",
    "Powers",
    "Museum",
    "SecretNotes",
    "JournalScraps",
    "Bundles",
    "Raccoons",
    "Grandpa",
    "Walnuts",
    "IslandUpgrades",
    "PerfectionTracker",
    "ArcadeGames",
    "Animals",
)
CHECKUP_TITLE = "CHECKUP  -  progress, achievements and what is missing"
PREDICTOR_TITLE = "PREDICTOR  -  what the RNG has in store"
EXTRAS_TITLE = "EXTRA DETAIL  -  skills, shipping, rarecrows and animals"


@dataclass(frozen=True)
class Section:
    title: str
    text: str
    kind: str
    subsection: bool = False


@dataclass
class Report:
    save_file: str
    generated: str
    summary: list[str]
    sections: list[Section]
    timings: dict[str, float]

    def text(self) -> str:
        header = "\n".join(
            [
                "STARDEW VALLEY SAVE REPORT",
                *("  " + line for line in self.summary),
                f"  Save file: {self.save_file}",
                f"  Generated: {self.generated}",
            ]
        )
        chunks = []
        for section in self.sections:
            chunks.extend(
                [
                    heading(section.title, "-" if section.subsection else "="),
                    section.text,
                ]
            )
        return header + "\n" + "\n".join(chunks) + "\n"

    def json(self) -> str:
        data = asdict(self)
        data["schema_version"] = 1
        data["generator_version"] = __version__
        return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def engine_context(name, module):
    environment = base_environment()
    template = Path(__file__).with_name("data") / (name + ".html")
    document = Document(template.read_text(encoding="utf-8"))
    document.install(environment)
    engine = module.create(environment)
    install(environment, engine)
    return document, engine


def build_report(save: Save, only: str = "all") -> Report:
    sections = []
    timings = {}
    summary = [
        f"{save.root.findtext('player/farmName', '')} Farm",
        f"Farmer {save.root.findtext('player/name')}",
    ]
    if only in ("all", "checkup"):
        from .engines import checkup

        started = time.perf_counter()
        _, engine = engine_context("checkup", checkup)
        info = Obj(outputPrefOld="hide_details", outputPrefNew="hide_all")
        chunks = []
        for name in CHECKUP_SECTIONS:
            try:
                chunks.append(call(engine["parse" + name], save.tree, info))
            except Exception as error:
                raise RuntimeError(f"Checkup section {name}: {error}") from error
        summary = [
            line[2:]
            for line in text_of(chunks[0]).splitlines()
            if line.startswith("* ")
        ]
        sections.append(Section(CHECKUP_TITLE, text_of("".join(chunks)), "checkup"))
        timings["checkup"] = time.perf_counter() - started
    if only in ("all", "predictor"):
        from .engines import predictor

        started = time.perf_counter()
        document, engine = engine_context("predictor", predictor)
        try:
            result = call(engine["parseSummary"], save.tree)
        except Exception as error:
            raise RuntimeError(f"Predictor summary: {error}") from error
        sections.append(Section(PREDICTOR_TITLE, text_of(result), "predictor"))
        for node in document.getElementsByName("tabset"):
            tab_id = get(node, "id")
            tab = tab_id.split("-")[1]
            try:
                call(engine["updateTab"], tab, False)
            except Exception as error:
                raise RuntimeError(f"Predictor section {tab}: {error}") from error
            body = text_of(get(document.getElementById("out-" + tab), "innerHTML"))
            if body:
                label = document.query(f'label[for="{tab_id}"]').html()
                label = " ".join(text_of(label).split())
                sections.append(Section(label, body, "predictor", True))
        timings["predictor"] = time.perf_counter() - started
    if only in ("all", "extras"):
        started = time.perf_counter()
        sections.append(Section(EXTRAS_TITLE, extras_text(save.root), "extras"))
        timings["extras"] = time.perf_counter() - started
    return Report(
        save.path.name,
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        summary,
        sections,
        timings,
    )
