import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';
import 'constants.dart';

class Reservation {
  final int id;
  final int startTime;
  final int endTime;
  final dynamic item;

  Reservation({
    required this.id,
    required this.startTime,
    required this.endTime,
    required this.item,
  });

  factory Reservation.fromJson(Map<String, dynamic> json) {
    if (json.containsKey('room')) {
      return Reservation(
        id: json['id'],
        startTime: json['start_time'],
        endTime: json['end_time'],
        item: Room.fromJson(json['room']),
      );
    } else if (json.containsKey('equipment')) {
      return Reservation(
        id: json['id'],
        startTime: json['start_time'],
        endTime: json['end_time'],
        item: Equipment.fromJson(json['equipment']),
      );
    }
    throw Exception('Invalid reservation data');
  }
}

class Room {
  final int id;
  final String name;
  final String capacity;
  final String available;

  Room({
    required this.id,
    required this.name,
    required this.capacity,
    required this.available,
  });

  factory Room.fromJson(Map<String, dynamic> json) {
    return Room(
      id: json['id'],
      name: json['name'],
      capacity: json['capacity'],
      available: json['available'],
    );
  }
}

class Equipment {
  final int id;
  final String name;
  final bool available;

  Equipment({
    required this.id,
    required this.name,
    required this.available,
  });

  factory Equipment.fromJson(Map<String, dynamic> json) {
    return Equipment(
      id: json['id'],
      name: json['name'],
      available: json['available'] == 1,
    );
  }
}

class Reservations extends StatefulWidget {
  const Reservations({Key? key}) : super(key: key);

  @override
  _ReservationsState createState() => _ReservationsState();
}

class _ReservationsState extends State<Reservations> {
  List<Reservation> reservations = [];

  @override
  void initState() {
    super.initState();
    fetchReservations();
  }

  Future<void> fetchReservations() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String token = prefs.getString('token') ?? '';

    try {
      Uri url;

      if (USE_HTTPS) {
        url = Uri.https(BASE_URL, 'api/users/reservations');
      } else {
        url = Uri.http(BASE_URL, 'api/users/reservations');
      }
      var headers = {"Content-Type": "application/json"};
      var body = {"token": token};

      var response = await http.post(
        url,
        headers: headers,
        body: jsonEncode(body),
      );

      print('Response status code: ${response.statusCode}');
      print('Response body: ${response.body}');

      if (response.statusCode == 200) {
        var data = jsonDecode(response.body);
        print('Parsed data: $data');

        if (data.containsKey('reservations')) {
          var reservationsData = data['reservations'];

          List<Reservation> tempReservations = [];

          if (reservationsData.containsKey('rooms')) {
            var roomReservations = reservationsData['rooms'];
            tempReservations.addAll(
              roomReservations
                  .map<Reservation>((reservationJson) =>
                      Reservation.fromJson(reservationJson))
                  .toList(),
            );
          }

          if (reservationsData.containsKey('equipments')) {
            var equipmentReservations = reservationsData['equipments'];
            tempReservations.addAll(
              equipmentReservations
                  .map<Reservation>((reservationJson) =>
                      Reservation.fromJson(reservationJson))
                  .toList(),
            );
          }

          setState(() {
            reservations = tempReservations;
          });
        } else {
          setState(() {
            reservations = [];
          });
        }
      } else {
        setState(() {
          reservations = [];
        });
      }
    } catch (e) {
      try {
        setState(() {
          reservations = [];
        });
      } catch (e) {
        print('Error fetching reservations: $e');
      }
      print("Error fetching reservations: $e");
    }
  }

  String formatDateTime(int timestamp) {
    var dateTime = DateTime.fromMillisecondsSinceEpoch(timestamp * 1000);
    return '${dateTime.day}/${dateTime.month}/${dateTime.year}, ${dateTime.hour}:${dateTime.minute}';
  }

  Future<void> returnEquipment(int equipmentId) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String token = prefs.getString('token') ?? '';

    try {
      Uri url;

      if (USE_HTTPS) {
        url = Uri.https(BASE_URL, 'api/equipments/$equipmentId/return');
      } else {
        url = Uri.http(BASE_URL, 'api/equipments/$equipmentId/return');
      }
      var headers = {"Content-Type": "application/json"};
      var body = {"token": token};

      var response = await http.post(
        url,
        headers: headers,
        body: jsonEncode(body),
      );

      print('Return Equipment response status code: ${response.statusCode}');
      print('Return Equipment response body: ${response.body}');

      if (response.statusCode == 200) {
        var responseData = jsonDecode(response.body);
        var code = responseData['code'];

        showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: Text('Return Equipment'),
              content: Text('Code: $code'),
              actions: <Widget>[
                TextButton(
                  child: Text('OK'),
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                ),
              ],
            );
          },
        );
      } else {
        showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: Text('Return Equipment'),
              content: Text('Failed to return equipment'),
              actions: <Widget>[
                TextButton(
                  child: Text('OK'),
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                ),
              ],
            );
          },
        );
      }
    } catch (e) {
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: Text('Return Equipment'),
            content: Text('Error: $e'),
            actions: <Widget>[
              TextButton(
                child: Text('OK'),
                onPressed: () {
                  Navigator.of(context).pop();
                },
              ),
            ],
          );
        },
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Reservations'),
      ),
      body: ListView.builder(
        itemCount: reservations.length,
        itemBuilder: (context, index) {
          var reservation = reservations[index];
          return GestureDetector(
            onTap: () {
              if (reservation.item is Equipment) {
                returnEquipment(reservation.item.id);
              }
            },
            child: ListTile(
              title: Text(
                reservation.item is Room
                    ? reservation.item.name
                    : reservation.item.name,
              ),
              subtitle: Text(
                reservation.item is Room
                    ? reservation.item.capacity
                    : 'Equipment',
              ),
              leading: reservation.item is Room
                  ? Image.network(USE_HTTPS
                      ? reservation.item.available.replaceFirst('http', 'https')
                      : reservation.item.available)
                  : Icon(Icons.electrical_services),
              trailing: Text(
                'Start: ${formatDateTime(reservation.startTime)}\nEnd: ${formatDateTime(reservation.endTime)}',
              ),
            ),
          );
        },
      ),
    );
  }
}

void main() {
  runApp(MaterialApp(
    title: 'Reservations App',
    home: Reservations(),
  ));
}
