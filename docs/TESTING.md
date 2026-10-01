# Test Plan

| ID | Scenario | Input | Expected result | Actual | Status |
|---|---|---|---|---|---|
| T01 | Simulator starts | `--scenario normal` | readings generated | Fill during run | |
| T02 | Reading generated | simulator cycle | valid JSON payload | Fill | |
| T03 | Valid API data | valid sensor values + key | 200 accepted | Fill | |
| T04 | Invalid data | moisture 150 | HTTP 422 | Automated | |
| T05 | Persistence | accepted reading | row in sensor_readings | Fill | |
| T06 | Latest | GET latest | newest reading | Fill | |
| T07 | History | GET history | ordered readings | Fill | |
| T08 | Above threshold | moisture 55, threshold 30 | no auto watering | Fill | |
| T09 | Below threshold | moisture 20 | alert + watering candidate | Automated | |
| T10 | Automatic watering | dry reading | pump_on + event | Automated | |
| T11 | Moisture increases | pump_on simulator | simulated moisture rises | Fill | |
| T12 | Pump stop | elapsed max duration | pump off + event complete | Fill | |
| T13 | Cooldown | repeated dry reading | no rapid second event | Fill | |
| T14 | Manual water | POST water | pump_on + manual event | Fill | |
| T15 | Alert | high temperature/dry soil | alert stored | Fill | |
| T16 | Acknowledge | PUT acknowledge | status acknowledged | Fill | |
| T17 | Offline | stop simulator | offline alert | Fill | |
| T18 | Dashboard | valid history | cards populated | Fill | |
| T19 | Charts | multiple readings | charts render | Fill | |
| T20 | DB failure | stop DB | graceful API errors/logs | Fill | |
| T21 | API failure | stop backend | simulator retry/log failure | Fill | |
| T22 | Simulator retry | temporary API outage | later cycles recover | Fill | |
| T23 | Unauthorized | no/invalid JWT | HTTP 401 | Fill | |
| T24 | Threshold update | PUT threshold | device configuration changes | Fill | |
| T25 | Multiple devices | 2+ devices | each user's devices isolated | Fill | |

## Automated tests
Run from repository root:
```powershell
$env:PYTHONPATH="."
pytest -q
```
The included tests cover registration/device creation, Pydantic validation and sensor ingestion triggering automatic watering.
