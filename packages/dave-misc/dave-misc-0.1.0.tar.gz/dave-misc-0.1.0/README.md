# Medium multiply
A small demo library for a Medium publication about publishing libraries.

### Installation
```
pip install dave-misc
```

### Get started
How to match some pattern with string:

```Python
from regx_entities import RegxEntities

# Instantiate a Multiplication object
regx = RegxEntities()

#Can added regular custom expressions
regx.add_entity("otp", r"[0-9]{4}", priority=True)

# Call the multiply method
result = regx.get_matchs("the otp is 0204")

```