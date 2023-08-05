# PySAP Macro

Python script to connect with SAP and allow usage of VB scripts

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. You can check my [GitHub](https://github.com/teusinLS/pysap_macro) for further informations.

### Installing

To install this package and all of it's requirements, run the following code on your terminal:

```
pip install pysap_macro
```

## Testing if it is working

You can create a Python file for testing purpose with the following code:

```
from pysap_macro import SAP

class Test:
    def __init__(self):
        self.run()

    def run(self):
        session = SAP.connect_sap(self, connection_name="SAP ENVIRONMENT NAME")

        # your VB code created by SAP below

Test()
```

## Authors

Thanks to [Fkfouri's sapy_script](https://github.com/fkfouri/sapy_script) for creating an amazing library and providing it on Github. This project was created based on his code.

* **Mateus Lima Silva**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
