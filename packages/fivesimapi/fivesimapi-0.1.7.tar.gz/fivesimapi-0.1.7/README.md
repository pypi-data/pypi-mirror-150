### Installation
```pip install fivesimapi```

### Example Code
```python
import FiveSimApi, asyncio
from FiveSimApi import fivesim

async def main():
    five_sim = fivesim.FiveSim(api_key)
    data = await five_sim.get_profile()
    print(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
