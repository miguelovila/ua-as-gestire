import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'constants.dart';
//import 'equipment_reservation.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'login.dart';

class Equipments extends StatefulWidget {
  const Equipments({Key? key}) : super(key: key);

  @override
  _EquipmentsState createState() => _EquipmentsState();
}

class _EquipmentsState extends State<Equipments> {
  List<Equipment> equipments = [];
  List<Equipment> filteredEquipments = [];
  TextEditingController searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    fetchEquipments(); // Fetch equipments when the widget initializes
    searchController.addListener(filterEquipments);
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

  void fetchEquipments() async {
    String token = await getToken();
    try {
      var url = Uri.parse(API_EQUIPMENTS_URL);
      var body = {
        "token": token,
      };

      var response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200) {
        var data = jsonDecode(response.body);
        print(data);
        if (data.containsKey("equipments")) {
          List<dynamic> equipmentData = data["equipments"];

          setState(() {
            equipments = equipmentData
                .map((equipmentJson) => Equipment.fromJson(equipmentJson))
                .toList();
            filteredEquipments = equipments;
          });
        } else {
          setState(() {
            filteredEquipments = [];
          });
        }
      } else if (response.statusCode == 401) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => Login()),
        );
      } else {
        setState(() {
          filteredEquipments = [];
        });
      }
    } catch (e) {
      setState(() {
        filteredEquipments = [];
      });
      print('Error fetching equipments: $e');
    }
  }

  void filterEquipments() {
    String query = searchController.text.toLowerCase();
    setState(() {
      filteredEquipments = equipments.where((equipment) {
        final equipmentName = equipment.name.toLowerCase();
        final equipmentDescription = equipment.description.toLowerCase();
        return equipmentName.contains(query) ||
            equipmentDescription.contains(query);
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
                SearchBar(
                  searchController: searchController,
                  gridWidthLimit: gridWidthLimit,
                ),
                const SizedBox(height: 20.0),
                Expanded(
                  child: EquipmentGrid(
                    gridWidthLimit: gridWidthLimit,
                    cardsPerRow: cardsPerRow,
                    filteredEquipments: filteredEquipments,
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

  const SearchBar({
    required this.searchController,
    required this.gridWidthLimit,
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
        ),
      ),
    );
  }
}

class EquipmentGrid extends StatelessWidget {
  final double gridWidthLimit;
  final int cardsPerRow;
  final List<Equipment> filteredEquipments;
  final double maxCardHeight;

  const EquipmentGrid({
    required this.gridWidthLimit,
    required this.cardsPerRow,
    required this.filteredEquipments,
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
            itemCount: filteredEquipments.length,
            itemBuilder: (context, index) {
              return GestureDetector(
                onTap: () {
                  showDialog(
                    context: context,
                    builder: (_) => EquipmentDetailsDialog(
                      equipment: filteredEquipments[index],
                    ),
                  );
                },
                child: EquipmentCard(
                  equipment: filteredEquipments[index],
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

class EquipmentCard extends StatelessWidget {
  final Equipment equipment;
  final double maxCardHeight;

  const EquipmentCard({
    required this.equipment,
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
                  equipment.image,
                  fit: BoxFit.cover,
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(10.0),
            child: ListTile(
              title: Text(
                '${equipment.name}\n${equipment.description}',
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
                        const Icon(Icons.storage),
                        const SizedBox(width: 5),
                        Text('${equipment.locker}'),
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

class Equipment {
  final int id;
  final String name;
  final String description;
  final String image;
  final String type;
  final String locker;

  Equipment({
    required this.id,
    required this.name,
    required this.description,
    required this.image,
    required this.type,
    required this.locker,
  });

  factory Equipment.fromJson(dynamic json) {
    return Equipment(
      id: json[0],
      name: json[1],
      description: json[2],
      image: json[5],
      type: json[3],
      locker: json[4],
    );
  }
}

class EquipmentDetailsDialog extends StatefulWidget {
  final Equipment equipment;

  const EquipmentDetailsDialog({Key? key, required this.equipment})
      : super(key: key);

  @override
  _EquipmentDetailsDialogState createState() => _EquipmentDetailsDialogState();
}

class _EquipmentDetailsDialogState extends State<EquipmentDetailsDialog> {
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
              Padding(
                padding: EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    Text(
                      'Reservation',
                      style:
                          TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                    SizedBox(height: 16.0),
                    //EquipmentReservationForm(
                    //  equipmentId: widget.equipment.id,
                    //  onSuccess: () {
                    //    Navigator.of(context).pop();
                    //  },
                    //),
                  ],
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
                crossFadeState: _isExpanded
                    ? CrossFadeState.showSecond
                    : CrossFadeState.showFirst,
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
                              Center(child: Text(widget.equipment.name)),
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
                                  widget.equipment.description,
                                  textAlign: TextAlign.center,
                                ),
                              ),
                            ),
                          ],
                        ),
                        DataRow(
                          cells: [
                            const DataCell(
                              Center(child: Text('Type')),
                            ),
                            DataCell(
                              Center(child: Text(widget.equipment.type)),
                            ),
                          ],
                        ),
                        DataRow(
                          cells: [
                            const DataCell(
                              Center(child: Text('Locker')),
                            ),
                            DataCell(
                              Center(child: Text(widget.equipment.locker)),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 16.0),
            ],
          ),
        ),
      ),
    );
  }
}
