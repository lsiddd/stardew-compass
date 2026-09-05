"""Small edge-case fixtures; no personal save is checked into the repository."""

import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
import zlib
from unittest.mock import patch
from lxml import etree
from stardew_report.cli import main
from stardew_report.extras import extras_text
from stardew_report.formatting import text_of
from stardew_report.query import Document
from stardew_report.rng import CSRandom, hash_string, random_seed, install
from stardew_report.runtime import (
    Array,
    BigInt,
    Env,
    Obj,
    binary,
    get,
    keys,
    put,
    truth,
    base_environment,
)
from stardew_report.save import SaveError, atomic_write, check_output_path, read_save

MINIMAL = b"<SaveGame><player><name>Ana</name></player><uniqueIDForThisGame>42</uniqueIDForThisGame></SaveGame>"


class SaveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.path = self.folder / "farmer_42"

    def write(self, data):
        self.path.write_bytes(data)
        return self.path

    def test_plain_bom_whitespace_and_compression(self):
        for data in (
            MINIMAL,
            b"\xef\xbb\xbf\n  " + MINIMAL,
            zlib.compress(MINIMAL),
            ('<?xml version="1.0" encoding="utf-16"?>' + MINIMAL.decode()).encode(
                "utf-16"
            ),
        ):
            with self.subTest(prefix=data[:10]):
                self.assertEqual(
                    read_save(self.write(data)).root.findtext("player/name"), "Ana"
                )

    def test_save_folder(self):
        folder = self.folder / "Ana_42"
        folder.mkdir()
        (folder / folder.name).write_bytes(MINIMAL)
        self.assertEqual(read_save(folder).path.name, "Ana_42")

    def test_bad_inputs(self):
        for data in (
            b"",
            b"not XML",
            b"<SaveGame>",
            b"<Farmer><name>Ana</name></Farmer>",
            b"<SaveGame/>",
            zlib.compress(MINIMAL)[:-2],
            zlib.compress(MINIMAL) + b"junk",
            b'<!DOCTYPE SaveGame [<!ENTITY x SYSTEM "file:///etc/passwd">]>' + MINIMAL,
        ):
            with self.subTest(data=data[:20]), self.assertRaises(SaveError):
                read_save(self.write(data))

    def test_decompression_limit(self):
        self.write(zlib.compress(b" " * 10000))
        with (
            patch("stardew_report.save.MAX_SAVE_BYTES", 100),
            self.assertRaises(SaveError),
        ):
            read_save(self.path)

    def test_never_overwrite_save_or_hardlink(self):
        self.write(MINIMAL)
        hardlink = self.folder / "alias"
        os.link(self.path, hardlink)
        for path in (self.path, hardlink):
            with self.assertRaises(SaveError):
                check_output_path(path, self.path)
        self.assertEqual(self.path.read_bytes(), MINIMAL)

    def test_atomic_failure_preserves_previous_report(self):
        self.path.write_text("previous report")
        with patch(
            "stardew_report.save.os.replace", side_effect=OSError("disk failure")
        ):
            with self.assertRaises(OSError):
                atomic_write(self.path, "new report")
        self.assertEqual(self.path.read_text(), "previous report")
        self.assertEqual(list(self.folder.iterdir()), [self.path])

    def test_cli_stdout_json_and_errors(self):
        self.write(MINIMAL)
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main([str(self.path), "-", "--only", "extras", "--format", "json"])
        self.assertEqual(code, 0)
        self.assertEqual(err.getvalue(), "")
        self.assertEqual(json.loads(out.getvalue())["sections"][0]["kind"], "extras")
        with contextlib.redirect_stderr(err):
            self.assertEqual(main([str(self.path), str(self.path)]), 1)
        self.assertEqual(self.path.read_bytes(), MINIMAL)


class RandomTests(unittest.TestCase):
    def test_upstream_vectors(self):
        fixtures = json.loads(
            Path(__file__).with_name("fixtures").joinpath("rng.json").read_text()
        )
        for case in fixtures["random"]:
            with self.subTest(seed=case["seed"]):
                rng = CSRandom(case["seed"])
                self.assertEqual([rng.Next() for _ in range(100)], case["values"])
        for case in fixtures["hashes"]:
            with self.subTest(value=case["value"]):
                self.assertEqual(hash_string(case["value"]), case["hash"])

    def test_big_ids_do_not_round_through_float(self):
        env = base_environment()
        engine = Env(env)
        engine.local["save"] = Obj(useLegacyRandom=False)
        install(env, engine)
        identifier = 9007199254740993
        actual = env["getRandomSeedFromBigInts"](
            BigInt(1), BigInt(123456789), BigInt(identifier)
        )
        expected = random_seed(False, 1, 123456789, identifier % 2147483647)
        self.assertEqual(actual, expected)
        self.assertNotEqual(actual, random_seed(False, 1, 123456789, float(identifier)))

    def test_signed_remainder(self):
        self.assertEqual(binary("%", -5, 3), -2)
        self.assertEqual(random_seed(True, -5, 3), -2)


class PortSemanticsTests(unittest.TestCase):
    def test_named_and_sparse_array_properties(self):
        a = Array()
        put(a, "Bat", 24)
        put(a, 3, "fish")
        self.assertEqual(get(a, "Bat"), 24)
        self.assertEqual(get(a, "length"), 4)
        self.assertEqual(keys(a), ["3", "Bat"])
        self.assertFalse(get(a, "hasOwnProperty")(0))
        self.assertTrue(get(a, "hasOwnProperty")("Bat"))

    def test_numeric_object_order(self):
        self.assertEqual(
            keys(Obj({"12": "a", "2": "b", "Z": "c", "A": "d"})), ["2", "12", "Z", "A"]
        )
        self.assertTrue(truth(Array()))
        self.assertTrue(truth(Obj()))
        self.assertEqual(binary("+", 12, " fish"), "12 fish")

    def test_xml_namespace_and_controls(self):
        document = Document('<html><select id="players"></select></html>')
        xml = etree.ElementTree(
            etree.fromstring(
                b'<SaveGame xmlns:p3="http://www.w3.org/2001/XMLSchema-instance"><locations><GameLocation p3:type="Farm"><characters><NPC><name>Pet</name></NPC></characters></GameLocation></locations></SaveGame>'
            )
        )
        self.assertEqual(
            document.query(xml).find("SaveGame[xmlns\\:p3]").js_get("length"), 1
        )
        self.assertEqual(
            document.query(xml)
            .find("GameLocation[p3\\:type='Farm'] > Characters > NPC > name")
            .text(),
            "Pet",
        )
        environment = base_environment()
        document.install(environment)
        option = environment["Option"]("Host", 0)
        document.query("#players").append(option)
        self.assertEqual(document.query("#players").val(), "0")

    def test_html_markers_and_tables(self):
        result = text_of(
            '<div><span class="ach_yes">Done</span><button>Hide</button><table><tr><th>Item</th><td>A &amp; B</td></tr></table><img alt="seed"></div>'
        )
        self.assertIn("[x] Done", result)
        self.assertIn("Item | A & B", result)
        self.assertIn("[seed]", result)
        self.assertNotIn("Hide", result)

    def test_extras_single_animal_and_unknown_shipping(self):
        root = etree.fromstring(b"""<SaveGame xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
          <player><name>Ana</name><basicShipped><item><key><string>(O)ModFish</string></key><value><int>7</int></value></item></basicShipped></player>
          <locations><GameLocation xsi:type="Farm"><buildings><Building><indoors xsi:type="AnimalHouse"><animals><item><value><FarmAnimal><name>Bella</name><type>Cow</type><age>12</age></FarmAnimal></value></item></animals></indoors></Building></buildings></GameLocation></locations>
        </SaveGame>""")
        result = extras_text(root)
        self.assertIn("#ModFish", result)
        self.assertIn("Bella", result)
        self.assertIn("12 days", result)


if __name__ == "__main__":
    unittest.main()
