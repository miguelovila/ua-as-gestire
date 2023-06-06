import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'constants.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

class EquipmentReservationForm extends StatefulWidget {
  final int equipmentId;
  final bool available;
  final VoidCallback? onSuccess;

  const EquipmentReservationForm({
    Key? key,
    required this.equipmentId,
    required this.available,
    required this.onSuccess,
  }) : super(key: key);

  @override
  State<EquipmentReservationForm> createState() =>
      _EquipmentReservationFormState();
}

class _EquipmentReservationFormState extends State<EquipmentReservationForm> {
  final durationController = TextEditingController();
  final reasonController = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  bool _reservationSuccess = false;
  String _reservationCode = '';

  Future<String> getToken() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String token = prefs.getString('token') ?? '';
    return token;
  }

  String? _validateDuration(String? value) {
    if (value == null || value.isEmpty) {
      return 'Please enter a duration';
    }
    final duration = int.tryParse(value);
    if (duration == null || duration <= 0) {
      return 'Please enter a valid duration';
    }
    return null;
  }

  void _reserveEquipment(BuildContext context) async {
    if (_formKey.currentState!.validate()) {
      String token = await getToken();
      final body = {"token": token, "duration": durationController.text};

      Uri url;

      if (USE_HTTPS) {
        url =
            Uri.https(BASE_URL, 'api/equipments/${widget.equipmentId}/reserve');
      } else {
        url =
            Uri.http(BASE_URL, 'api/equipments/${widget.equipmentId}/reserve');
      }
      var response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200) {
        int code = jsonDecode(response.body)['code'];
        setState(() {
          _reservationSuccess = true;
          _reservationCode = code.toString();
        });
      } else {
        ScaffoldMessenger.of(context)
            .showSnackBar(
              SnackBar(
                content: Text('Reservation failed'),
                action: SnackBarAction(
                  label: 'OK',
                  onPressed: () {},
                ),
              ),
            )
            .closed
            .then((reason) {
          if (reason != SnackBarClosedReason.action) {}
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return _reservationSuccess
        ? Column(
            children: [
              Text(
                'Reservation successful',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 18,
                ),
              ),
              SizedBox(height: 16),
              Text(
                'Reservation Code: $_reservationCode',
                style: TextStyle(
                  fontSize: 16,
                ),
              ),
            ],
          )
        : Form(
            key: _formKey,
            child: Column(
              children: [
                Row(
                  children: [
                    Expanded(
                      child: TextFormField(
                        controller: durationController,
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                          labelText: 'Duration',
                          helperText: 'in minutes',
                        ),
                        validator: _validateDuration,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: TextFormField(
                        controller: reasonController,
                        decoration: const InputDecoration(
                            border: OutlineInputBorder(),
                            labelText: 'Reason (optional)',
                            helperText: "why, where?"),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                ElevatedButton(
                  onPressed: () {
                    _reserveEquipment(context);
                  },
                  child: const Padding(
                    padding: EdgeInsets.symmetric(vertical: 16, horizontal: 32),
                    child: Text(
                      'Reserve',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          );
  }
}
