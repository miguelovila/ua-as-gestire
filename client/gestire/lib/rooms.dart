import 'package:flutter/material.dart';

class Rooms extends StatefulWidget {
  const Rooms({Key? key}) : super(key: key);

  @override
  _RoomsState createState() => _RoomsState();
}

class _RoomsState extends State<Rooms> {
  final List<Room> rooms = [
    Room(
      name: 'Classroom 1',
      image: 'assets/classroom1.jpg',
      computers: 20,
      powerOutlets: 10,
      seats: 30,
    ),
    Room(
      name: 'Videoconference Room 2',
      image: 'assets/classroom2.jpg',
      computers: 15,
      powerOutlets: 8,
      seats: 25,
    ),
    Room(
      name: 'Classroom 3',
      image: 'assets/classroom3.jpg',
      computers: 18,
      powerOutlets: 12,
      seats: 35,
    ),
    Room(
      name: 'Auditorium 4',
      image: 'assets/anf.jpg',
      computers: 0,
      powerOutlets: 20,
      seats: 200,
    ),

    // Add more rooms as needed
  ];

  List<Room> filteredRooms = []; // Filtered list of rooms
  TextEditingController searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    filteredRooms = rooms; // Initialize the filtered list with all rooms
    searchController
        .addListener(filterRooms); // Listen for changes in the search field
  }

  @override
  void dispose() {
    searchController.dispose();
    super.dispose();
  }

  void filterRooms() {
    String query = searchController.text.toLowerCase();
    setState(() {
      filteredRooms = rooms.where((room) {
        final roomName = room.name.toLowerCase();
        return roomName.contains(query);
      }).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              TextField(
                controller: searchController,
                decoration: InputDecoration(
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
              const SizedBox(height: 20.0),
              Expanded(
                child: ListView.builder(
                  itemCount: filteredRooms.length,
                  itemBuilder: (context, index) {
                    return Card(
                      child: Column(
                        children: [
                          AspectRatio(
                            aspectRatio: 16 / 9,
                            child: Image.asset(
                              filteredRooms[index].image,
                              fit: BoxFit.cover,
                            ),
                          ),
                          Padding(
                            padding: const EdgeInsets.all(10.0),
                            child: ListTile(
                              title: Text(filteredRooms[index].name),
                              subtitle: Row(
                                children: [
                                  const Icon(Icons.computer),
                                  const SizedBox(width: 5),
                                  Text(
                                      'Computers: ${filteredRooms[index].computers}'),
                                  const SizedBox(width: 10),
                                  const Icon(Icons.power),
                                  const SizedBox(width: 5),
                                  Text(
                                      'Power Outlets: ${filteredRooms[index].powerOutlets}'),
                                  const SizedBox(width: 10),
                                  const Icon(Icons.event_seat),
                                  const SizedBox(width: 5),
                                  Text('Seats: ${filteredRooms[index].seats}'),
                                ],
                              ),
                            ),
                          ),
                        ],
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class Room {
  final String name;
  final String image;
  final int computers;
  final int powerOutlets;
  final int seats;

  Room({
    required this.name,
    required this.image,
    required this.computers,
    required this.powerOutlets,
    required this.seats,
  });
}
