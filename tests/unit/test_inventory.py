"""Synthetic save fragments for inventory and storage regression coverage."""

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from lxml import etree

from stardew.cli import main
from stardew.infrastructure.saves.loader import snapshot, from_snapshot
from stardew.infrastructure.game_data import load_game_data
from stardew.application.extras import analyze_extras
from stardew.presentation.text.extras import render_extras


def extras_text(root):
    state = from_snapshot(snapshot(root), Path("synthetic_42"))
    data = load_game_data()
    return render_extras(analyze_extras(state, data), data)


def save_xml(body):
    return etree.fromstring(
        (
            '<SaveGame xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            + body
            + "<uniqueIDForThisGame>42</uniqueIDForThisGame></SaveGame>"
        ).encode()
    )


class InventoryTests(unittest.TestCase):
    def test_slots_quality_names_and_attachments(self):
        root = save_xml("""<player><name>Ana</name><items>
          <Item xsi:nil="true"/>
          <Item xsi:type="Object"><itemId>(O)24</itemId><stack>12</stack><quality>2</quality></Item>
          <Item xsi:type="Object"><itemId>24</itemId><stack>3</stack><quality>4</quality></Item>
          <Item xsi:type="FishingRod"><name>Iridium Rod</name><attachments>
            <Object xsi:nil="true"/>
            <Object><name>Bait</name><stack>27</stack></Object>
          </attachments></Item>
          <Item xsi:type="Object"><itemId>ModBerry</itemId><stack>7</stack></Item>
          <Item xsi:type="MeleeWeapon"><itemId>24</itemId></Item>
        </items><leftRing><name>Glow Ring</name><stack>1</stack></leftRing></player>""")
        result = extras_text(root)
        self.assertIn("Slot 2: Parsnip x12 (quality: gold; ID: (O)24)", result)
        self.assertIn("Slot 3: Parsnip x3 (quality: iridium; ID: 24)", result)
        self.assertIn("Slot 2: Bait x27", result)
        self.assertIn("#ModBerry x7", result)
        self.assertIn("Slot 6: #24 x1", result)  # Weapon IDs must not use object names.
        self.assertIn("leftRing: Glow Ring x1", result)
        self.assertNotIn("Slot 1:", result)

    def test_named_placed_chest_building_fridge_and_empty_chest(self):
        root = save_xml("""<player><name>Ana</name></player><locations>
          <GameLocation><name>Farm</name><objects><item>
            <key><Vector2><X>12</X><Y>8</Y></Vector2></key><value>
              <Object xsi:type="Chest"><name>Big Chest</name>
                <tileLocation><X>0</X><Y>0</Y></tileLocation>
                <modData><item><key><string>Pathoschild.ChestsAnywhere/Name</string></key>
                  <value><string>Resources</string></value></item></modData>
                <items><Item><name>Wood</name><stack>999</stack></Item></items>
              </Object>
            </value></item></objects><buildings><Building><buildingType>Shed</buildingType>
              <tileX>4</tileX><tileY>5</tileY><indoors><name>Shed</name><objects><item><value>
                <Object xsi:type="Chest"><items/></Object>
              </value></item></objects></indoors>
            </Building></buildings></GameLocation>
          <GameLocation><name>FarmHouse</name><fridge><items>
            <Item><name>Milk</name><stack>2</stack></Item>
          </items></fridge></GameLocation>
        </locations>""")
        result = extras_text(root)
        self.assertIn("Chests and fridges: 3", result)
        self.assertIn("Resources (Big Chest) — Farm / tile (12, 8)", result)
        self.assertIn("Wood x999", result)
        self.assertIn("Chest 2: Chest — Farm / Shed (4, 5) / Shed\n\n* Empty", result)
        self.assertIn("Chest 3: Fridge — FarmHouse", result)
        self.assertIn("Milk x2", result)

    def test_multiplayer_deduplication_and_missing_ids(self):
        root = save_xml("""<player><name>Ana</name><UniqueMultiplayerID>1</UniqueMultiplayerID></player>
          <farmhands><Farmer><name>Bob</name><UniqueMultiplayerID>2</UniqueMultiplayerID>
            <items><Item><name>Stone</name><stack>10</stack></Item></items></Farmer>
            <Farmer><name>Carol</name></Farmer></farmhands>
          <locations><GameLocation><farmhand><name>Bob</name><UniqueMultiplayerID>2</UniqueMultiplayerID>
          </farmhand></GameLocation></locations>""")
        result = extras_text(root)
        for name in ("Ana", "Bob", "Carol"):
            self.assertEqual(result.count(f"Inventory: {name}\n"), 1)
        self.assertIn("Stone x10", result)

    def test_nested_chests_and_legacy_ids(self):
        root = save_xml("""<player><name>Ana</name><items><Item xsi:type="Chest"><name>Chest</name>
          <items><Item xsi:type="Object"><parentSheetIndex>388</parentSheetIndex><stack>8</stack></Item>
          <Item xsi:type="Chest"><name>Inner Chest</name><items>
            <Item xsi:type="Object"><parentSheetIndex>130</parentSheetIndex><bigCraftable>true</bigCraftable></Item>
          </items></Item></items></Item></items></player>""")
        result = extras_text(root)
        self.assertIn("Chests and fridges: 2", result)
        self.assertIn("Chest 2: Inner Chest — Inventory: Ana / inside Chest", result)
        self.assertEqual(result.count("Wood x8"), 1)
        self.assertIn("Chest x1 (quality: normal; ID: 130)", result)

    def test_shared_and_separate_wallet_storage(self):
        root = save_xml("""<player><name>Ana</name></player><locations><GameLocation><name>Farm</name>
          <objects><item><value><Object xsi:type="Chest"><items/>
            <globalInventoryId><string>JunimoChests</string></globalInventoryId>
            <separateWalletItems><SerializableDictionaryOfInt64Inventory><item><key><long>2</long></key>
              <value><Inventory><Item><name>Diamond</name><stack>2</stack></Item></Inventory></value>
            </item></SerializableDictionaryOfInt64Inventory></separateWalletItems>
          </Object></value></item></objects></GameLocation></locations>
          <globalInventories><item><key><string>JunimoChests</string></key><value><Inventory>
            <Item><name>Prismatic Shard</name><stack>3</stack></Item>
          </Inventory></value></item></globalInventories>""")
        result = extras_text(root)
        self.assertIn("Shared inventory: JunimoChests (listed below)", result)
        self.assertIn("Separate wallet inventory: 2", result)
        self.assertIn("Diamond x2", result)
        self.assertEqual(result.count("Prismatic Shard x3"), 1)

    def test_cli_includes_inventory_in_text_and_json_without_changing_save(self):
        data = etree.tostring(
            save_xml("""<player><name>Ana</name><items>
          <Item><name>Wood</name><stack>5</stack></Item></items></player>""")
        )
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "Ana_42"
            path.write_bytes(data)
            for format in ("text", "json"):
                with self.subTest(format=format):
                    out = io.StringIO()
                    with contextlib.redirect_stdout(out):
                        self.assertEqual(
                            main(
                                [
                                    "report",
                                    str(path),
                                    "-o",
                                    "-",
                                    "--only",
                                    "extras",
                                    "--format",
                                    format,
                                ]
                            ),
                            0,
                        )
                    result = out.getvalue()
                    if format == "json":
                        result = json.dumps(
                            json.loads(result)["extras"], ensure_ascii=False
                        )
                    if format == "text":
                        self.assertIn("Inventory: Ana", result)
                        self.assertIn("Wood x5", result)
                    else:
                        self.assertIn('"name": "Wood"', result)
                        self.assertIn('"quantity": 5', result)
            self.assertEqual(path.read_bytes(), data)
