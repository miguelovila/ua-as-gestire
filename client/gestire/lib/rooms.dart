import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'constants.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'login.dart';

class Rooms extends StatefulWidget {
  const Rooms({Key? key}) : super(key: key);

  @override
  _RoomsState createState() => _RoomsState();
}

class _RoomsState extends State<Rooms> {
  List<Room> rooms = [];
  List<Room> filteredRooms = [];
  TextEditingController searchController = TextEditingController();
  TextEditingController minSeatsController = TextEditingController();
  TextEditingController minPowerSocketsController = TextEditingController();
  TextEditingController typeController = TextEditingController();
  TextEditingController availableNowController = TextEditingController();

  @override
  void initState() {
    super.initState();
    fetchRooms({}); // Fetch rooms when the widget initializes
    searchController.addListener(filterRooms);
  }

  @override
  void dispose() {
    searchController.dispose();
    minSeatsController.dispose();
    minPowerSocketsController.dispose();
    typeController.dispose();
    availableNowController.dispose();
    super.dispose();
  }

  Future<String> getToken() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String token = prefs.getString('token') ?? '';
    return token;
  }

  void fetchRooms(Map<String, dynamic> filters) async {
    String token = await getToken();
    try {
      var url = Uri.parse(API_ROOMS_URL);
      var body = {
        "token": token,
        "filters": filters,
      };

      // Remove the empty filter values from the request body
      (body['filters'] as Map<String, dynamic>?)
          ?.removeWhere((key, value) => value == '');

      var response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200) {
        var data = jsonDecode(response.body);
        print(data);
        if (data.containsKey("rooms")) {
          List<dynamic> roomData = data["rooms"];

          setState(() {
            rooms =
                roomData.map((roomJson) => Room.fromJson(roomJson)).toList();
            filteredRooms = rooms;
          });
        } else {
          setState(() {
            filteredRooms = [];
          });
        }
      } else if (response.statusCode == 401) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => Login()),
        );
      } else {
        setState(() {
          filteredRooms = [];
        });
      }
    } catch (e) {
      setState(() {
        filteredRooms = [];
      });
      print('Error fetching rooms: $e');
    }
  }

  void filterRooms() {
    String query = searchController.text.toLowerCase();
    setState(() {
      filteredRooms = rooms.where((room) {
        final roomName = room.name.toLowerCase();
        final roomDescription = room.description.toLowerCase();
        return roomName.contains(query) || roomDescription.contains(query);
      }).toList();
    });
  }

  void applyFilters() {
    String type = typeController.text;
    Map<String, dynamic> filters = {
      'minSeats': int.tryParse(minSeatsController.text),
      'minPowerSockets': int.tryParse(minPowerSocketsController.text),
      'type': type.isNotEmpty ? type : null,
      'availableNow': availableNowController.text == 'true',
    };

    fetchRooms(filters);
  }

  @override
  Widget build(BuildContext context) {
    int cardsPerRow = 1;
    if (MediaQuery.of(context).size.width > 900) {
      cardsPerRow = 3;
    } else if (MediaQuery.of(context).size.width > 500) {
      cardsPerRow = 2;
    }

    double gridWidthLimit = 900.0;
    if (MediaQuery.of(context).size.width > 1000) {
      gridWidthLimit = 1200.0;
    } else if (MediaQuery.of(context).size.width > 800) {
      gridWidthLimit = 900.0;
    }

    double maxCardHeight = MediaQuery.of(context).size.height / 3;

    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: SafeArea(
            child: Column(
              children: [
                SearchBar(
                  searchController: searchController,
                  gridWidthLimit: gridWidthLimit,
                  onApplyFilters: applyFilters,
                  minSeatsController: minSeatsController,
                  minPowerSocketsController: minPowerSocketsController,
                  typeController: typeController,
                  availableNowController: availableNowController,
                ),
                const SizedBox(height: 20.0),
                Expanded(
                  child: RoomGrid(
                    gridWidthLimit: gridWidthLimit,
                    cardsPerRow: cardsPerRow,
                    filteredRooms: filteredRooms,
                    maxCardHeight: maxCardHeight,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class SearchBar extends StatelessWidget {
  final TextEditingController searchController;
  final double gridWidthLimit;
  final Function()? onApplyFilters;
  final TextEditingController minSeatsController;
  final TextEditingController minPowerSocketsController;
  final TextEditingController typeController;
  final TextEditingController availableNowController;

  const SearchBar({
    required this.searchController,
    required this.gridWidthLimit,
    this.onApplyFilters,
    required this.minSeatsController,
    required this.minPowerSocketsController,
    required this.typeController,
    required this.availableNowController,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: gridWidthLimit, // Limit the width of the search bar
      child: TextField(
        controller: searchController,
        decoration: InputDecoration(
          hintText: 'Search',
          contentPadding: const EdgeInsets.only(left: 30.0, right: 35.0),
          border: const OutlineInputBorder(
            borderRadius: BorderRadius.all(Radius.circular(100.0)),
          ),
          suffixIcon: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              FilterIcon(
                onApplyFilters: onApplyFilters,
                minSeatsController: minSeatsController,
                minPowerSocketsController: minPowerSocketsController,
                typeController: typeController,
                availableNowController: availableNowController,
              ),
              SizedBox(width: 15),
              Icon(Icons.qr_code),
              SizedBox(width: 25),
            ],
          ),
        ),
      ),
    );
  }
}

class FilterIcon extends StatefulWidget {
  final Function()? onApplyFilters;
  final TextEditingController minSeatsController;
  final TextEditingController minPowerSocketsController;
  final TextEditingController typeController;
  final TextEditingController availableNowController;

  const FilterIcon({
    this.onApplyFilters,
    required this.minSeatsController,
    required this.minPowerSocketsController,
    required this.typeController,
    required this.availableNowController,
  });

  @override
  _FilterIconState createState() => _FilterIconState();
}

class _FilterIconState extends State<FilterIcon> {
  bool isAvailableNow = false;

  @override
  void initState() {
    super.initState();
    isAvailableNow = widget.availableNowController.text == 'true';
  }

  @override
  Widget build(BuildContext context) {
    return PopupMenuButton<String>(
      icon: Icon(Icons.filter_alt),
      onSelected: (value) {
        if (value == 'applyFilters') {
          widget.onApplyFilters?.call();
        } else if (value == 'resetFilters') {
          widget.minSeatsController.text = '';
          widget.minPowerSocketsController.text = '';
          widget.typeController.text = '';
          widget.availableNowController.text = '';
          widget.onApplyFilters?.call();
        }
      },
      itemBuilder: (BuildContext context) {
        return <PopupMenuEntry<String>>[
          PopupMenuItem<String>(
            value: 'applyFilters',
            child: Text('Apply Filters'),
          ),
          PopupMenuItem<String>(
            value: 'resetFilters',
            child: Text('Reset Filters'),
          ),
          PopupMenuItem<String>(
            value: 'minSeats',
            child: TextField(
              controller: widget.minSeatsController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(
                labelText: 'Minimum Seats',
              ),
            ),
          ),
          PopupMenuItem<String>(
            value: 'minPowerSockets',
            child: TextField(
              controller: widget.minPowerSocketsController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Minimum Power Sockets',
              ),
            ),
          ),
          PopupMenuItem<String>(
            value: 'type',
            child: DropdownButtonFormField<String>(
              decoration: const InputDecoration(
                labelText: 'Type',
              ),
              value: widget.typeController.text.isNotEmpty
                  ? widget.typeController.text
                  : null,
              onChanged: (value) {
                widget.typeController.text = value ?? '';
              },
              items: [
                DropdownMenuItem<String>(
                  value: 'Auditorium',
                  child: Text('Auditorium'),
                ),
                DropdownMenuItem<String>(
                  value: 'Classroom',
                  child: Text('Classroom'),
                ),
                DropdownMenuItem<String>(
                  value: 'Office',
                  child: Text('Office'),
                ),
                DropdownMenuItem<String>(
                  value: 'Teaching Laboratory',
                  child: Text('Teaching Laboratory'),
                ),
                DropdownMenuItem<String>(
                  value: 'Videoconference Room',
                  child: Text('Videoconference Room'),
                ),
                // Add more unique dropdown items as needed
              ],
            ),
          ),
          PopupMenuItem<String>(
            value: 'availableNow',
            child: Row(
              children: [
                Text('Available Now'),
                Spacer(),
                Switch(
                  value: widget.availableNowController.text == 'true',
                  onChanged: (value) {
                    widget.availableNowController.text = value.toString();
                  },
                ),
              ],
            ),
          ),
        ];
      },
    );
  }
}

class RoomGrid extends StatelessWidget {
  final double gridWidthLimit;
  final int cardsPerRow;
  final List<Room> filteredRooms;
  final double maxCardHeight;

  const RoomGrid({
    required this.gridWidthLimit,
    required this.cardsPerRow,
    required this.filteredRooms,
    required this.maxCardHeight,
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        return Container(
          width: gridWidthLimit, // Limit the width of the grid
          child: GridView.builder(
            gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: cardsPerRow,
              crossAxisSpacing: 10.0,
              mainAxisSpacing: 10.0,
            ),
            itemCount: filteredRooms.length,
            itemBuilder: (context, index) {
              return GestureDetector(
                onTap: () {
                  showDialog(
                    context: context,
                    builder: (_) => RoomDetailsDialog(
                      room: filteredRooms[index],
                    ),
                  );
                },
                child: RoomCard(
                  room: filteredRooms[index],
                  maxCardHeight: maxCardHeight,
                ),
              );
            },
          ),
        );
      },
    );
  }
}

class RoomCard extends StatelessWidget {
  final Room room;
  final double maxCardHeight;

  const RoomCard({
    required this.room,
    required this.maxCardHeight,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Expanded(
            child: SizedBox(
              height: maxCardHeight,
              child: AspectRatio(
                aspectRatio: 16 / 9,
                child: Image.network(
                  room.image,
                  fit: BoxFit.cover,
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(10.0),
            child: ListTile(
              title: Text(
                '${room.name}\n${room.description}',
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              subtitle: Padding(
                padding: const EdgeInsets.only(top: 5.0, bottom: 1.0),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.computer),
                        const SizedBox(width: 5),
                        Text('${room.computers}'),
                      ],
                    ),
                    const SizedBox(width: 10),
                    Row(
                      children: [
                        const Icon(Icons.power),
                        const SizedBox(width: 0),
                        Text('${room.powerOutlets}'),
                      ],
                    ),
                    const SizedBox(width: 10),
                    Row(
                      children: [
                        const Icon(Icons.event_seat),
                        const SizedBox(width: 3),
                        Text('${room.seats}'),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class Room {
  final String name;
  final String description;
  final String image;
  final int seats;
  final int powerOutlets;
  final int computers;
  final int oscilloscopes;
  final int signalGenerators;
  final int multimeters;
  final int soundSystem;
  final int projector;
  final int whiteboard;

  Room({
    required this.name,
    required this.description,
    required this.image,
    required this.seats,
    required this.powerOutlets,
    required this.computers,
    required this.oscilloscopes,
    required this.signalGenerators,
    required this.multimeters,
    required this.soundSystem,
    required this.projector,
    required this.whiteboard,
  });

  factory Room.fromJson(dynamic json) {
    return Room(
      name: json[1],
      description: json[2],
      image: json[3],
      seats: json[4],
      powerOutlets: json[5],
      computers: json[6],
      oscilloscopes: json[7],
      signalGenerators: json[8],
      multimeters: json[9],
      soundSystem: json[10],
      projector: json[11],
      whiteboard: json[12],
    );
  }
}

class RoomDetailsDialog extends StatefulWidget {
  final Room room;

  const RoomDetailsDialog({Key? key, required this.room}) : super(key: key);

  @override
  _RoomDetailsDialogState createState() => _RoomDetailsDialogState();
}

class _RoomDetailsDialogState extends State<RoomDetailsDialog> {
  bool _isExpanded = false;

  @override
  Widget build(BuildContext context) {
    return Dialog(
      insetPadding: const EdgeInsets.symmetric(horizontal: 16.0),
      child: SingleChildScrollView(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 500.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              const Padding(
                padding: EdgeInsets.all(16.0),
                child: Text(
                  'Reservation',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
              ),
              const SizedBox(height: 16.0),
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 16.0),
                child: Divider(),
              ),
              const SizedBox(height: 16.0),
              GestureDetector(
                onTap: () {
                  setState(() {
                    _isExpanded = !_isExpanded;
                  });
                },
                child: Container(
                  color: Colors.transparent,
                  padding: const EdgeInsets.all(16.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Details',
                        style: TextStyle(
                            fontSize: 20, fontWeight: FontWeight.bold),
                      ),
                      Icon(
                        _isExpanded
                            ? Icons.keyboard_arrow_up
                            : Icons.keyboard_arrow_down,
                        color: Colors.grey,
                      ),
                    ],
                  ),
                ),
              ),
              AnimatedCrossFade(
                duration: const Duration(milliseconds: 300),
                firstChild: const SizedBox(),
                secondChild: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16.0),
                  child: FractionallySizedBox(
                    widthFactor: 1.0,
                    child: DataTable(
                      columnSpacing: 16.0,
                      dataRowMinHeight: 3.0,
                      columns: const [
                        DataColumn(
                          label: Expanded(
                            child: Center(
                              child: Text(
                                'Property',
                                textAlign: TextAlign.center,
                                style: TextStyle(fontWeight: FontWeight.bold),
                              ),
                            ),
                          ),
                        ),
                        DataColumn(
                          label: Expanded(
                            child: Center(
                              child: Text(
                                'Value',
                                textAlign: TextAlign.center,
                                style: TextStyle(fontWeight: FontWeight.bold),
                              ),
                            ),
                          ),
                        ),
                      ],
                      rows: [
                        DataRow(
                          cells: [
                            const DataCell(
                              Center(child: Text('Name')),
                            ),
                            DataCell(
                              Center(child: Text(widget.room.name)),
                            ),
                          ],
                        ),
                        DataRow(
                          cells: [
                            const DataCell(
                              Center(child: Text('Description')),
                            ),
                            DataCell(
                              Center(
                                  child: Text(
                                widget.room.description,
                                textAlign: TextAlign.center,
                              )),
                            ),
                          ],
                        ),
                        DataRow(
                          cells: [
                            const DataCell(
                              Center(child: Text('Seats')),
                            ),
                            DataCell(
                              Center(child: Text(widget.room.seats.toString())),
                            ),
                          ],
                        ),
                        DataRow(
                          cells: [
                            const DataCell(
                              Center(
                                  child: Text(
                                'Power Outlets',
                                textAlign: TextAlign.center,
                              )),
                            ),
                            DataCell(
                              Center(
                                  child: Text(
                                      widget.room.powerOutlets.toString())),
                            ),
                          ],
                        ),
                        DataRow(
                          cells: [
                            const DataCell(
                              Center(child: Text('Computers')),
                            ),
                            DataCell(
                              Center(
                                  child:
                                      Text(widget.room.computers.toString())),
                            ),
                          ],
                        ),
                        DataRow(
                          cells: [
                            const DataCell(
                              Center(child: Text('Oscilloscopes')),
                            ),
                            DataCell(
                              Center(
                                  child: Text(
                                      widget.room.oscilloscopes.toString())),
                            ),
                          ],
                        ),
                        DataRow(
                          cells: [
                            const DataCell(
                              Center(
                                  child: Text(
                                'Signal Generators',
                                textAlign: TextAlign.center,
                              )),
                            ),
                            DataCell(
                              Center(
                                  child: Text(
                                      widget.room.signalGenerators.toString())),
                            ),
                          ],
                        ),
                        DataRow(
                          cells: [
                            const DataCell(
                              Center(child: Text('Multimeters')),
                            ),
                            DataCell(
                              Center(
                                  child:
                                      Text(widget.room.multimeters.toString())),
                            ),
                          ],
                        ),
                        DataRow(
                          cells: [
                            const DataCell(
                              Center(
                                  child: Text(
                                'Sound System',
                                textAlign: TextAlign.center,
                              )),
                            ),
                            DataCell(
                              Center(
                                  child: Text(widget.room.soundSystem == 1
                                      ? 'Yes'
                                      : 'No')),
                            ),
                          ],
                        ),
                        DataRow(
                          cells: [
                            const DataCell(
                              Center(child: Text('Projector')),
                            ),
                            DataCell(
                              Center(
                                  child: Text(widget.room.projector == 1
                                      ? 'Yes'
                                      : 'No')),
                            ),
                          ],
                        ),
                        DataRow(
                          cells: [
                            const DataCell(
                              Center(child: Text('Whiteboard')),
                            ),
                            DataCell(
                              Center(
                                  child: Text(widget.room.whiteboard == 1
                                      ? 'Yes'
                                      : 'No')),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
                crossFadeState: _isExpanded
                    ? CrossFadeState.showSecond
                    : CrossFadeState.showFirst,
              ),
              const SizedBox(height: 16.0),
            ],
          ),
        ),
      ),
    );
  }
}
