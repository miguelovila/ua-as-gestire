import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'constants.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class Rooms extends StatefulWidget {
  const Rooms({Key? key}) : super(key: key);

  @override
  _RoomsState createState() => _RoomsState();
}

class _RoomsState extends State<Rooms> {
  List<Room> rooms = [];
  List<Room> filteredRooms = [];
  TextEditingController searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    fetchRooms(); // Fetch rooms when the widget initializes
    searchController.addListener(filterRooms);
  }

  @override
  void dispose() {
    searchController.dispose();
    super.dispose();
  }

  Future<String> getToken() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String token = prefs.getString('token') ?? '';
    return token;
  }

  void fetchRooms() async {
    String token = await getToken();
    try {
      var url = Uri.parse(API_ROOMS_URL);
      var response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"token": token}),
      );

      if (response.statusCode == 200) {
        var data = jsonDecode(response.body);
        if (data.containsKey("rooms")) {
          // Check if "rooms" key exists
          List<dynamic> roomData = data["rooms"];

          setState(() {
            rooms =
                roomData.map((roomJson) => Room.fromJson(roomJson)).toList();
            filteredRooms = rooms;
          });
        } else {
          // Handle invalid response format
          print('Invalid response format. Missing "rooms" key.');
        }
      } else {
        // Handle API error or invalid response
        print('Failed to fetch rooms. Status code: ${response.statusCode}');
      }
    } catch (e) {
      // Handle network or other errors
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
                Container(
                  width: gridWidthLimit, // Limit the width of the search bar
                  child: TextField(
                    controller: searchController,
                    decoration: const InputDecoration(
                      hintText: 'Search',
                      contentPadding: EdgeInsets.only(left: 30.0, right: 35.0),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(100.0)),
                      ),
                      suffixIcon: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(Icons.filter_alt),
                          SizedBox(width: 15),
                          Icon(Icons.qr_code),
                          SizedBox(width: 25),
                        ],
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 20.0),
                Expanded(
                  child: LayoutBuilder(
                    builder: (context, constraints) {
                      return Container(
                        width: gridWidthLimit, // Limit the width of the grid
                        child: GridView.builder(
                          gridDelegate:
                              SliverGridDelegateWithFixedCrossAxisCount(
                            crossAxisCount: cardsPerRow,
                            crossAxisSpacing: 10.0,
                            mainAxisSpacing: 10.0,
                          ),
                          itemCount: filteredRooms.length,
                          itemBuilder: (context, index) {
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
                                          filteredRooms[index].image,
                                          fit: BoxFit.cover,
                                        ),
                                      ),
                                    ),
                                  ),
                                  Padding(
                                    padding: const EdgeInsets.all(10.0),
                                    child: ListTile(
                                      title: Text(
                                        '${filteredRooms[index].name}\n${filteredRooms[index].description}',
                                        maxLines: 2,
                                        overflow: TextOverflow.ellipsis,
                                      ),
                                      subtitle: Padding(
                                        padding: const EdgeInsets.only(
                                          top: 5.0,
                                          bottom: 1.0,
                                        ),
                                        child: Row(
                                          mainAxisSize: MainAxisSize.min,
                                          children: [
                                            Row(
                                              children: [
                                                const Icon(Icons.computer),
                                                const SizedBox(width: 5),
                                                Text(
                                                  '${filteredRooms[index].computers}',
                                                ),
                                              ],
                                            ),
                                            const SizedBox(width: 10),
                                            Row(
                                              children: [
                                                const Icon(Icons.power),
                                                const SizedBox(width: 0),
                                                Text(
                                                  '${filteredRooms[index].powerOutlets}',
                                                ),
                                              ],
                                            ),
                                            const SizedBox(width: 10),
                                            Row(
                                              children: [
                                                const Icon(Icons.event_seat),
                                                const SizedBox(width: 3),
                                                Text(
                                                  '${filteredRooms[index].seats}',
                                                ),
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
                          },
                        ),
                      );
                    },
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
