import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

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
      var url = Uri.parse('http://localhost:5000/api/users/reservations');
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
      setState(() {
        reservations = [];
      });
      print('Error fetching reservations: $e');
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
          return ListTile(
            title: Text(reservation.item is Room
                ? reservation.item.name
                : reservation.item.name),
            subtitle: Text(reservation.item is Room
                ? reservation.item.capacity
                : 'Equipment'),
            leading: reservation.item is Room
                ? Image.network(reservation.item.available)
                : Icon(Icons.electrical_services),
            trailing: Text(
              'Start: ${reservation.startTime}\nEnd: ${reservation.endTime}',
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
