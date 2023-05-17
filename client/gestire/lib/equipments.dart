import 'package:flutter/material.dart';

class Equipments extends StatefulWidget {
  const Equipments({Key? key}) : super(key: key);

  @override
  _EquipmentsState createState() => _EquipmentsState();
}

class _EquipmentsState extends State<Equipments> {
  final List<Equipment> equipments = [
    Equipment(
      name: 'Arduino',
      image: 'assets/arduino.jpg',
      availability: 5,
    ),
    Equipment(
      name: 'ESP32',
      image: 'assets/esp32.jpg',
      availability: 2,
    ),
    Equipment(
      name: 'PIC32',
      image: 'assets/pic32.jpg',
      availability: 8,
    ),
    Equipment(
      name: 'FPGA Cyclone IV',
      image: 'assets/fpga.jpg',
      availability: 3,
    ),
    // Add more equipment as needed
  ];

  final TextEditingController _searchController = TextEditingController();
  List<Equipment> _filteredEquipments = [];

  @override
  void initState() {
    super.initState();
    _filteredEquipments = equipments;
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  void _filterEquipments(String query) {
    setState(() {
      if (query.isNotEmpty) {
        _filteredEquipments = equipments
            .where((equipment) =>
                equipment.name.toLowerCase().contains(query.toLowerCase()))
            .toList();
      } else {
        _filteredEquipments = equipments;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: SafeArea(
            child: Column(
              children: [
                TextField(
                  controller: _searchController,
                  onChanged: _filterEquipments,
                  decoration: const InputDecoration(
                    hintText: 'Search',
                    contentPadding: EdgeInsets.only(left: 30.0, right: 35.0),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.all(Radius.circular(100.0)),
                    ),
                    suffixIcon: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(Icons.search),
                        SizedBox(width: 25),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 20.0),
                Expanded(
                  child: ListView.builder(
                    itemCount: _filteredEquipments.length,
                    itemBuilder: (context, index) {
                      return Card(
                        child: Column(
                          children: [
                            AspectRatio(
                              aspectRatio: 16 / 9,
                              child: ClipRRect(
                                borderRadius: const BorderRadius.vertical(
                                    top: Radius.circular(4)),
                                child: Image.asset(
                                  _filteredEquipments[index].image,
                                  fit: BoxFit.cover,
                                ),
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.all(10.0),
                              child: ListTile(
                                title: Text(_filteredEquipments[index].name),
                                subtitle: Row(
                                  children: [
                                    const Icon(Icons.control_point_duplicate),
                                    const SizedBox(width: 5),
                                    Text(
                                        '${_filteredEquipments[index].availability}'),
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
      ),
    );
  }
}

class Equipment {
  final String name;
  final String image;
  final int availability;

  Equipment({
    required this.name,
    required this.image,
    required this.availability,
  });
}
