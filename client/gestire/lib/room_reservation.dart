import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'constants.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

class RoomReservationForm extends StatefulWidget {
  final int roomId;
  final VoidCallback? onSuccess;

  const RoomReservationForm({
    Key? key,
    required this.roomId,
    required this.onSuccess,
  }) : super(key: key);

  @override
  State<RoomReservationForm> createState() => _RoomReservationFormState();
}

class _RoomReservationFormState extends State<RoomReservationForm> {
  final dateController = TextEditingController();
  final timeController = TextEditingController();
  final durationController = TextEditingController();
  final descriptionController = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  DateTime? _selectedDate;
  TimeOfDay? _selectedTime;

  Future<void> _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime(2100),
    );

    if (picked != null) {
      setState(() {
        _selectedDate = picked;
        dateController.text = picked.day.toString().padLeft(2, '0') +
            '-' +
            picked.month.toString().padLeft(2, '0') +
            '-' +
            picked.year.toString();
      });
    }
  }

  Future<void> _selectTime(BuildContext context) async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: TimeOfDay.now(),
    );

    if (picked != null) {
      setState(() {
        _selectedTime = picked;
        timeController.text = picked.format(context);
      });
    }
  }

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

  void _reserveRoom(BuildContext context) async {
    if (_formKey.currentState!.validate()) {
      final startTime = _selectedDate!.millisecondsSinceEpoch ~/ 1000 +
          _selectedTime!.hour * 3600 +
          _selectedTime!.minute * 60;

      final duration = int.parse(durationController.text) * 60;
      String token = await getToken();
      final body = {
        "token": token,
        "start_time": startTime.toString(),
        "duration": duration.toString(),
        "reason": descriptionController.text,
      };

      var url = Uri.http(BASE_URL, 'api/rooms/${widget.roomId}/reserve');
      var response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200) {
        // Reservation successful
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Reservation successful'),
            action: SnackBarAction(
              label: 'OK',
              onPressed: () {},
            ),
          ),
        );
        widget.onSuccess!();
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
    return Column(
      children: [
        Form(
          key: _formKey,
          child: Column(
            children: [
              Row(
                children: [
                  Expanded(
                    child: GestureDetector(
                      onTap: () {
                        _selectDate(context);
                      },
                      child: AbsorbPointer(
                        child: TextFormField(
                          controller: dateController,
                          decoration: const InputDecoration(
                            border: OutlineInputBorder(),
                            labelText: 'Date',
                            helperText: '31-12-2123',
                          ),
                          validator: (value) {
                            if (value!.isEmpty) {
                              return 'Please enter a date';
                            }
                            return null;
                          },
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: GestureDetector(
                      onTap: () {
                        _selectTime(context);
                      },
                      child: AbsorbPointer(
                        child: TextFormField(
                          controller: timeController,
                          decoration: const InputDecoration(
                            border: OutlineInputBorder(),
                            labelText: 'Time',
                            helperText: '23:59',
                          ),
                          validator: (value) {
                            if (value!.isEmpty) {
                              return 'Please enter a time';
                            }
                            return null;
                          },
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
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
                      controller: descriptionController,
                      decoration: const InputDecoration(
                        border: OutlineInputBorder(),
                        labelText: 'Description',
                        helperText: 'Example: Meeting with John Doe',
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () {
                  _reserveRoom(context);
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
        ),
      ],
    );
  }
}
