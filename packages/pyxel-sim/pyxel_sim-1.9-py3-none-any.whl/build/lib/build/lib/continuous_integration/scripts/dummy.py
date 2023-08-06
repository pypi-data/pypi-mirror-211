from create_json_schema import (
    Klass,
    generate_class,
    get_doc_from_klass,
    get_documentation,
)

from pyxel.outputs import ExposureOutputs, Outputs

klass = Klass(Outputs)

foo = get_documentation(klass.cls)

print("Goodbye World")
