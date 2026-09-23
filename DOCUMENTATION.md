# Gestire Documentation

This guide collects the setup, testing, hardware, and API information previously kept in the README, checked against the source in this repository. For the project story and architecture overview, see [README.md](README.md).

The hosted demo has been retired. The source and build archives preserve the 2023 prototype, including hardcoded deployment settings that need changing for local use.

- [Local setup](#local-setup)
- [API reference](#api-reference)
- [Database](#database)
- [Locker hardware](#locker-hardware)
- [Automated testing](#automated-testing)
- [Implementation notes](#implementation-notes)
- [Original project material](#original-project-material)

## Local Setup

### Backend

Use Python 3.11, the original project's target. The application uses Flask, Flask-CORS, bcrypt, and Python's built-in SQLite module. The HTTP tests also need `requests`. The pinned Flask version fails during startup on Python 3.14 because it calls the removed `pkgutil.get_loader` function.

From the repository root, create an environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install 'Flask==2.3.2' 'Flask-Cors==3.0.10' 'Werkzeug<3' bcrypt requests
cd backend
python app.py
```

These installation commands retain the recorded Flask versions and use the `bcrypt` package imported by the source. The archived [requirements.txt](backend/requirements.txt) instead lists `python_bcrypt==0.3.2`; it also omits `requests`. The Werkzeug constraint keeps Flask 2.3.2's test client compatible with its dependency.

Start the backend with `python app.py`: the route modules import objects from `__main__`, and database initialization runs in that entry point. A plain `flask run` invocation does not follow the same initialization path.

The server binds to `0.0.0.0:5000`, and is accessible on the same machine at `http://localhost:5000`. Startup creates `backend/database/database.db` and populates empty catalogue tables with seven demo users, 22 rooms, and eight equipment items. Existing non-empty catalogue tables are left as they are.

Demo accounts are `du0@ua.pt` through `du6@ua.pt`, with matching passwords `du0` through `du6`. The original test script uses `du1@ua.pt` / `du1`. These are local sample accounts.

### Local Addresses and Images

Update these settings before connecting the client or hardware:

| Location | Setting |
| --- | --- |
| [client/gestire/lib/constants.dart](client/gestire/lib/constants.dart) | Set `USE_HTTPS = false` and `BASE_URL = 'localhost:5000'` for a browser on the server machine. `BASE_URL` is a host and optional port, with no scheme or `/api` suffix. |
| [backend/database/con.py](backend/database/con.py) | Replace the old origin in seeded image URLs with `http://localhost:5000`, or the server's LAN origin if using another device. Keep the `/api/images/...` paths. |
| [lockers/src/main.cpp](lockers/src/main.cpp) | Set Wi-Fi credentials and `API_URL` to a reachable server address including `/api`, for example `http://192.168.1.100:5000/api`. |
| [backend/cfg.py](backend/cfg.py) and [lockers/src/main.cpp](lockers/src/main.cpp) | Keep `LOCKER_SECRET` and `API_SECRET` equal. The locker uses this shared value; app session tokens are separate. |

For a phone or ESP32, use the backend computer's LAN address in place of `localhost`. Image URLs must also be reachable from the device displaying them.

Image URLs are stored in SQLite. Editing the seed source affects newly seeded tables, so an existing database needs its image fields updated too. To rebuild disposable demo data, stop the server, move the database file aside, and restart the backend. Keep a backup if it contains reservations you want to preserve.

### Flutter Client

The app source is in [client/gestire/](client/gestire/). It uses `http` for requests and `shared_preferences` for profile and session storage.

The checked-in SDK metadata needs attention before rebuilding: [pubspec.yaml](client/gestire/pubspec.yaml) declares Dart `>=2.19.6 <3.0.0`, while [pubspec.lock](client/gestire/pubspec.lock) records Dart `>=3.0.0-0 <4.0.0`. Reconcile the SDK constraint and dependencies with your chosen Flutter toolchain first. A Flutter build has not been verified as part of this documentation update.

After resolving the toolchain and changing the API address:

```bash
cd client/gestire
flutter pub get
flutter run -d chrome
```

Use an available device target for a native build, with the corresponding platform tools installed. Original build artifacts are kept at:

- [Android APK](client/android-frontend.apk)
- [Linux archive](client/linux-frontend.tar.xz)
- [Web archive](client/web-frontend.zip)

These builds retain the former deployment configuration. They are historical artifacts, rather than ready-to-run clients for a new local backend.

### ESP32 Firmware

The main firmware project is [lockers/](lockers/). The copy under `deliverables/lockers/` is an earlier snapshot with different network settings.

The PlatformIO environment targets `nodemcu-32s` with the Arduino framework. Its library dependencies are declared in [platformio.ini](lockers/platformio.ini): Keypad, LiquidCrystal_I2C, and ArduinoJson.

After setting the network values and connecting the board:

```bash
cd lockers
pio run
pio run --target upload
pio device monitor --baud 115200
```

The physical controller is needed to verify keypad, display, and relay behaviour. The [recorded hardware demo](https://youtube.com/shorts/Ew3Ff9O0Odw) is linked from the original project.

## API Reference

Routes live under `/api`. Send JSON bodies with `Content-Type: application/json`. Authenticated application routes take a `token` field in the body. The locker endpoint instead takes the shared locker secret in that field.

Times are Unix timestamps in **seconds**. Reservation durations are also in **seconds**. Room reservations require at least 900 seconds. Equipment reservations start when the API receives the request.

### Route Summary

| Method | Path | Body fields | Result |
| --- | --- | --- | --- |
| POST | `/api/auth` | `email`, `password` | Profile and session token |
| POST | `/api/auth/check` | `token` | Token validity; renews a valid session |
| POST | `/api/rooms` | `token`, `filters` | Matching room rows |
| GET | `/api/rooms/{room_id}` | `token` | One room row; this route expects a JSON body even though it uses GET |
| POST | `/api/rooms/{room_id}/reserve` | `token`, `start_time`, `duration`, optional `reason` | Room reservation confirmation |
| POST | `/api/equipments` | `token` | All equipment rows |
| POST | `/api/equipments/{equipment_id}` | `token` | One equipment row |
| POST | `/api/equipments/{equipment_id}/reserve` | `token`, `duration`, optional `reason` | Pickup PIN |
| POST | `/api/equipments/{equipment_id}/return` | `token` | Return PIN for the most recent borrower's unavailable item |
| POST | `/api/users/reservations` | `token` | Up to 100 room and 100 equipment reservations for the user |
| POST | `/api/locker/{code}` | `token` containing the locker secret | Consumes the code and returns its compartment and operation |
| GET | `/api/images/{path}` | None | Image from `backend/static/` |

### Authentication

```bash
curl -X POST http://localhost:5000/api/auth \
  -H 'Content-Type: application/json' \
  -d '{"email":"du1@ua.pt","password":"du1"}'
```

A successful response contains:

```json
{
  "mec": 107001,
  "name": "Dummy User One",
  "email": "du1@ua.pt",
  "profile_picture": "http://localhost:5000/api/images/student_2.png",
  "token": "<session-token>"
}
```

The example image address assumes the local URL changes described above. Tokens are stored in SQLite and expire after 600 seconds without a successful validity check. Authenticated API calls check the token and extend that expiry. `POST /api/auth/check` returns `{"valid": true}` with status 200, or `{"valid": false}` with status 401 for an invalid or expired token. Invalid login credentials return 401.

### Rooms

The room list requires a `filters` object; use `{}` to request all rooms. Supported API filters are `minSeats`, `minPowerSockets`, `type`, and `availableNow`. Name and description substring searches happen in the Flutter client.

```json
{
  "token": "<session-token>",
  "filters": {
    "minSeats": 20,
    "minPowerSockets": 10,
    "type": "Classroom",
    "availableNow": true
  }
}
```

Room types in the sample data are `Auditorium`, `Classroom`, `Office`, `Teaching Laboratory`, and `Videoconference Room`. Type matching is exact; numeric filters mean “at least”.

The API returns database rows as positional JSON arrays. The list response is `{"rooms": [[...], ...]}`; the detail response is `{"room": [...]}`. Column order is:

```text
[id, name, description, image, capacity, power_sockets, computers,
 oscilloscopes, signal_generators, multimeters, sound_system,
 projector, whiteboard, reservations]
```

The last field is a legacy text field seeded with `"[]"`; bookings themselves are stored in the separate `reservations` table.

To reserve a room, submit a start timestamp and duration to `/api/rooms/{room_id}/reserve`:

```json
{
  "token": "<session-token>",
  "start_time": 2000000000,
  "duration": 3600,
  "reason": "Study session"
}
```

Success returns `{"success": "Room reserved"}`. Invalid time ranges and detected conflicts return status 400. See the [implementation notes](#implementation-notes) for the limits of the overlap and “Available Now” checks.

### Equipment

`POST /api/equipments` returns `{"equipments": [[...], ...]}`, and the detail route returns `{"equipment": [...]}`. Row order is:

```text
[id, name, description, reservations, locker, image, available]
```

`available` is an integer, `0` or `1`. The `reservations` field is another legacy text field. The endpoint lists the whole catalogue; text search runs in Flutter.

Reserve an available item through `/api/equipments/{equipment_id}/reserve`:

```json
{
  "token": "<session-token>",
  "duration": 3600,
  "reason": "Lab experiment"
}
```

Success returns:

```json
{"message": "Equipment reserved", "code": 123456}
```

The API marks the item unavailable immediately and schedules a callback for 120 seconds later. If the pickup code is still pending, that callback makes the item available and adds `User didn't pick up the equipment` to the reservation's observation field.

For a return, send `{"token": "<session-token>"}` to `/api/equipments/{equipment_id}/return`. The route checks the most recent reservation's user and the item's availability. Success returns:

```json
{"message": "Equipment return code", "code": 654321}
```

Requesting a return code alone does not make the item available. That happens when the locker endpoint consumes the return code. Return-code expiry has a known scheduler bug, described below.

### User Reservations

`POST /api/users/reservations` takes the session token and returns:

```json
{
  "reservations": {
    "rooms": [],
    "equipments": []
  }
}
```

Each populated entry contains `id`, `start_time`, `end_time`, and a nested `room` or `equipment` object. Each list is ordered by descending start time and limited to 100 entries. Empty lists still produce a successful response.

Equipment details contain `id`, `name`, and integer `available`. The nested room fields have misleading names in this version: `capacity` holds the room description and `available` holds the image URL. The Records screen uses those values as its subtitle and thumbnail.

### Locker Protocol

The ESP32 submits a six-digit code in the route path:

```http
POST /api/locker/123456
Content-Type: application/json

{"token": "<locker-secret>"}
```

A successful pickup response is:

```json
{"type": "get", "locker": "1A"}
```

A return response uses `"type": "put"`. Compartments are `1A`, `1B`, `1C`, `1D`, `2A`, `2B`, `2C`, and `2D`.

The endpoint deletes the accepted code, so it cannot be reused. It keeps equipment unavailable for `get`, and marks it available for `put`. A wrong shared secret returns 401; a code absent from memory returns 400. This is an HTTP response to the ESP32's request, not a separate server-initiated command.

### Errors

Most routes return `{"error": "..."}` with status 400 for malformed requests, missing resources, or unavailable items, and 401 for authentication failures. Authentication routes also use 401 for malformed requests. The implementation catches many exceptions and reports `Invalid request`; the old README's generic 500 tables did not reflect that behaviour.

## Database

The schema and seed functions are in [backend/database/con.py](backend/database/con.py), and the database path is configured in [backend/cfg.py](backend/cfg.py).

| Table | Contents |
| --- | --- |
| `users` | University number, name, email, bcrypt password hash, profile image URL |
| `tokens` | Session token, expiry timestamp, user ID |
| `rooms` | Room name, type, image, capacity, facilities, legacy reservation text field |
| `equipments` | Item name, description, locker ID, image, availability, legacy reservation text field |
| `reservations` | User ID, room ID, start/end timestamps, optional reason |
| `equipment_reservations` | User ID, equipment ID, start/end timestamps, usage place, observation |

Pickup and return codes are held in an in-memory dictionary in [backend/routes/equipments.py](backend/routes/equipments.py). They are not stored in SQLite. Reservations and availability survive a restart; pending codes and their scheduled callbacks do not.

## Locker Hardware

### Wiring Defined by the Firmware

| Output | ESP32 GPIO |
| --- | ---: |
| Locker `1A` | 13 |
| Locker `1B` | 14 |
| Locker `1C` | 27 |
| Locker `1D` | 26 |
| Locker `2A` | 25 |
| Locker `2B` | 33 |
| Locker `2C` | 32 |
| Locker `2D` | 23 |

Keypad rows use GPIOs `15, 4, 16, 17`; columns use `5, 18, 19`. The key layout is:

```text
1 2 3
4 5 6
7 8 9
* 0 #
```

The LCD is configured as 20 columns by four rows at I2C address `0x27`. The sketch uses the board's default I2C pins. Relays start HIGH and are driven LOW to activate a compartment.

### Controller Behaviour

The state machine in [lockers/src/main.cpp](lockers/src/main.cpp) has eight states: `S_IDLE`, `S_INPUT`, `S_ABORTED`, `S_PROCESSING`, `S_INVALID`, `S_GET`, `S_PUT`, and `S_ERROR`.

Entering six digits submits the code automatically. `*` deletes the preceding digit and `#` aborts input. On a successful response, the display directs the user to collect or return equipment at the named compartment. The relay stays active for ten seconds, then the controller returns to idle. An invalid code or request failure displays an error.

There is no door-closure or item-presence feedback in this firmware. The backend does not receive confirmation that the physical operation completed.

## Automated Testing

The original [tests/tester.py](tests/tester.py) uses Python `unittest` and `requests` against a running server at `http://localhost:5000/api`.

With the backend running, open a second terminal at the repository root:

```bash
source .venv/bin/activate
python tests/tester.py
```

Run it against disposable sample data. It authenticates as `du1@ua.pt`, writes reservations, and does not clean up afterward. A fresh **seeded** database is needed; an uninitialized database without users cannot satisfy the tests.

There are 11 test methods covering login, token checks, room and equipment reads, reservations, returns, and a nominal locker check. Their interpretation needs care:

- The room reservation test uses a fixed timestamp. Running it again can conflict with its previous booking.
- The equipment reservation test can fail if the item remains unavailable from a previous run. An unclaimed pickup is normally released after 120 seconds while the server stays running.
- `setUp()` resets `reservation_code` before every test, so the locker test's conditional body never executes. It also contains an application token where the locker secret would be required.
- The return test relies on the reservation test having run first. The suite is dependent on shared state and test order.

The old README included a transcript with two failures on a reused database. That is one possible result, rather than a guaranteed outcome or a complete verification of the locker flow.

## Implementation Notes

These are behaviours visible in the checked-in source, useful when reproducing the prototype or deciding where to resume development:

- **Room intervals:** the conflict query tests whether either endpoint of the new reservation falls inside an existing reservation. It misses a new interval that completely surrounds an existing booking and treats touching endpoints as conflicts. Its default “now” timestamps are evaluated when the module loads.
- **Equipment form:** the UI labels duration in minutes but submits the raw number, which the backend interprets as seconds. The optional reason field is displayed but not included in the equipment form's request. The room form does convert minutes to seconds.
- **Code expiry:** pickup cleanup is scheduled after 120 seconds. Return cleanup passes `argument=(code)` instead of a one-element tuple, which causes the scheduled callback to fail. The locker endpoint does not independently check the stored `expires` timestamp.
- **Recovery:** pending codes and timers live only in server memory. A restart can leave a reserved item unavailable without a usable pickup code. Code consumption also precedes relay activation, so a failed response or hardware operation cannot be retried with that same code.
- **Physical state:** accepting a return code immediately marks the item available. No sensor confirms that it was returned, and returning it does not replace the reservation's planned end time with an actual return time.
- **Authentication and scope:** this version uses local sample users, bcrypt hashes, and a shared locker secret over HTTP. University SSO, QR scanning, and physical room access control are not implemented; the QR icon in the room search bar is decorative.
- **Reservation records:** room details use the mismatched `capacity` and `available` fields described in the API reference. Equipment availability is the item's current catalogue state, not a per-reservation completion flag.

## Original Project Material

Gestire was developed for Análise de Sistemas at DETI, University of Aveiro, in 2023 by group 603:

| Team member | Student number |
| --- | --- |
| Diogo Silva | 108212 |
| Ivo Delgado | 107757 |
| Martim Carvalho | 108749 |
| Miguel Vila | 107276 |

The coursework is preserved under [deliverables/](deliverables/):

| Material | Location |
| --- | --- |
| Backlog material | [e1-backlog](deliverables/e1-backlog/) |
| Product vision and scope | [Vision report](deliverables/e2-vision/AS-E2-Visionodf.docx.pdf) |
| Process analysis and use cases | [Analysis report](deliverables/e3-analysis/AS-E3-Analise.docx.pdf) |
| Architecture and construction | [Construction report](deliverables/e5-construction/AS-E5-Construcao.docx.pdf) |
| Presentation slides | [presentations](deliverables/presentations/) |
| Earlier locker firmware | [deliverables/lockers](deliverables/lockers/) |

These reports describe different stages of the project and include planned features. The source is the reference for implemented behaviour: for example, the firmware uses C++/Arduino, and the login uses local credentials.
