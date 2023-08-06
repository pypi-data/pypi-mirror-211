import unittest

from starter_service.avro_parser import avsc_to_pydantic


class Test(unittest.TestCase):
    avro_schema = {
        "type": "record",
        "namespace": "Tutorialspoint",
        "name": "Employee",
        "fields": [
            {"name": "name", "type": "string"},
            {"name": "age", "type": "int"},
            {"name": "from", "type": "int"},
            {
                "name": "to",
                "type": ["null", "string"],
                "default": None,
                "doc": "The title of the article."
            },
        ]
    }

    def test_avsc_to_pydantic_reserved(self):
        class_python, class_name = avsc_to_pydantic(self.avro_schema)
        print(class_python)


if __name__ == '__main__':
    unittest.main()
