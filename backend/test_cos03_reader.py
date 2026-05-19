import unittest

from cos03_reader import apply_channel_reading, parse_store_frame


SOIL_TEMP_FRAME = bytes.fromhex(
    "AA2624020141C266666A0856E702E2848300000000E59C9FE5A3A4E6B8A9E5BAA6000000000000AF00000000000000000000000000000000000000000000698F"
)
SOIL_MOISTURE_FRAME = bytes.fromhex(
    "AA26240101000000006A0857960025524800000000E59C9FE5A3A4E6B9BFE5BAA60000000000009800000000000000000000000000000000000000000000EB53"
)
PH_FRAME = bytes.fromhex(
    "AA26240401404000006A08584500300000000000005048000000000000000000000000000000008700000000000000000000000000000000000000000000EBE7"
)
LEAF_MOISTURE_FRAME = bytes.fromhex(
    "AA26240801000000006A0857EB0025000000000000E58FB6E99DA2E6B9BFE5BAA60000000000007700000000000000000000000000000000000000000000A054"
)
NITROGEN_FRAME = bytes.fromhex(
    "AA26240501000000006A08573C006D672F6B670000E6B0AE0000000000000000000000000000009000000000000000000000000000000000000000000000D74D"
)


class Cos03ReaderTests(unittest.TestCase):
    def test_parse_store_frame_extracts_name_unit_and_value(self):
        reading = parse_store_frame(SOIL_TEMP_FRAME)
        self.assertEqual(reading["channel_no"], 2)
        self.assertEqual(reading["name"], "土壤温度")
        self.assertEqual(reading["unit"], "℃")
        self.assertAlmostEqual(reading["value"], 24.3, places=1)

    def test_apply_channel_reading_maps_sensor_fields(self):
        snapshot = {}
        apply_channel_reading(snapshot, parse_store_frame(SOIL_TEMP_FRAME))
        apply_channel_reading(snapshot, parse_store_frame(SOIL_MOISTURE_FRAME))
        apply_channel_reading(snapshot, parse_store_frame(PH_FRAME))
        apply_channel_reading(snapshot, parse_store_frame(LEAF_MOISTURE_FRAME))
        apply_channel_reading(snapshot, parse_store_frame(NITROGEN_FRAME))

        self.assertAlmostEqual(snapshot["airTemp"], 24.3, places=1)
        self.assertAlmostEqual(snapshot["soilMoisture"], 15.2, places=1)
        self.assertAlmostEqual(snapshot["ph"], 3.0, places=1)
        self.assertAlmostEqual(snapshot["airHumidity"], 11.9, places=1)
        self.assertEqual(snapshot["nitrogen"], 144.0)

    def test_latest_reading_overwrites_previous_channel_value(self):
        snapshot = {}
        first = parse_store_frame(SOIL_TEMP_FRAME)
        second = parse_store_frame(
            bytes.fromhex(
                "AA2624020141C0CCCD6A08576902E2848300000000E59C9FE5A3A4E6B8A9E5BAA6000000000000A200000000000000000000000000000000000000000000F147"
            )
        )

        apply_channel_reading(snapshot, first)
        apply_channel_reading(snapshot, second)

        self.assertAlmostEqual(snapshot["airTemp"], 24.1, places=1)
        self.assertEqual(snapshot["_channel_values"]["土壤温度"]["timestamp"], second["timestamp"])


if __name__ == "__main__":
    unittest.main()
