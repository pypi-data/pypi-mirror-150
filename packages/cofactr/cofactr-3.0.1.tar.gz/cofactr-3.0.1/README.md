# Cofactr

Python client library for accessing Cofactr.

## Example

```python
from typing import List
from cofactr.core import get_part, get_parts, search_parts
# Flagship is the default schema.
from cofactr.schema.flagship.part import Part

part_res = get_part(id=cpid, external=False)
part: Part = res["data"]

parts_res = search_parts(query="esp32", external=False)
parts: List[Part] = res["data"]
```
