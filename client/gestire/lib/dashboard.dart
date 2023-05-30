import 'package:flutter/material.dart';
import 'package:gestire/login.dart';
import 'package:gestire/rooms.dart';
import 'package:gestire/equipments.dart';
import 'package:gestire/records.dart';
import 'package:shared_preferences/shared_preferences.dart';

extension StringCasingExtension on String {
  String toCapitalized() =>
      length > 0 ? '${this[0].toUpperCase()}${substring(1).toLowerCase()}' : '';
  String toTitleCase() => replaceAll(RegExp(' +'), ' ')
      .split(' ')
      .map((str) => str.toCapitalized())
      .join(' ');
}

class Dashboard extends StatefulWidget {
  const Dashboard({Key? key}) : super(key: key);

  @override
  _DashboardState createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  int currentPage = 0;
  late PageController pageController;

  @override
  void initState() {
    super.initState();
    pageController = PageController(initialPage: currentPage);
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (BuildContext context, BoxConstraints constraints) {
        if (constraints.maxWidth >= 1000) {
          // Navigation Rail in an extended state
          return Scaffold(
            body: Row(
              children: [
                NavigationRail(
                  extended: true,
                  selectedIndex: currentPage,
                  onDestinationSelected: (int index) {
                    if (index == destinations.length - 1) {
                      showDialog(
                        context: context,
                        builder: (BuildContext context) {
                          return AccountDialog();
                        },
                      );
                    } else {
                      setState(() {
                        currentPage = index;
                        pageController.animateToPage(
                          currentPage,
                          duration: const Duration(milliseconds: 300),
                          curve: Curves.ease,
                        );
                      });
                    }
                  },
                  labelType: NavigationRailLabelType.none,
                  destinations: destinations.map(
                    (Destination destination) {
                      return NavigationRailDestination(
                        icon: destination.icon,
                        selectedIcon: destination.selectedIcon,
                        label: Text(destination.label),
                      );
                    },
                  ).toList(),
                ),
                VerticalDivider(thickness: 1, width: 1),
                Expanded(
                  child: PageView(
                    controller: pageController,
                    onPageChanged: (int index) {
                      setState(() {
                        currentPage = index;
                      });
                    },
                    children: const [
                      Rooms(),
                      Equipments(),
                      Records(),
                    ],
                  ),
                ),
              ],
            ),
          );
        } else if (constraints.maxWidth >= 800) {
          // Navigation Rail with labels hidden
          return Scaffold(
            body: Row(
              children: [
                NavigationRail(
                  selectedIndex: currentPage,
                  onDestinationSelected: (int index) {
                    if (index == destinations.length - 1) {
                      showDialog(
                        context: context,
                        builder: (BuildContext context) {
                          return AccountDialog();
                        },
                      );
                    } else {
                      setState(() {
                        currentPage = index;
                        pageController.animateToPage(
                          currentPage,
                          duration: const Duration(milliseconds: 300),
                          curve: Curves.ease,
                        );
                      });
                    }
                  },
                  destinations: destinations.map(
                    (Destination destination) {
                      return NavigationRailDestination(
                        icon: destination.icon,
                        selectedIcon: destination.selectedIcon,
                        label: SizedBox.shrink(),
                      );
                    },
                  ).toList(),
                ),
                VerticalDivider(thickness: 1, width: 1),
                Expanded(
                  child: PageView(
                    controller: pageController,
                    onPageChanged: (int index) {
                      setState(() {
                        currentPage = index;
                      });
                    },
                    children: const [
                      Rooms(),
                      Equipments(),
                      Records(),
                    ],
                  ),
                ),
              ],
            ),
          );
        } else {
          // Bottom Navigation Bar
          return Scaffold(
            body: PageView(
              controller: pageController,
              onPageChanged: (int index) {
                setState(() {
                  currentPage = index;
                });
              },
              children: const [
                Rooms(),
                Equipments(),
                Records(),
                AccountDialog(),
              ],
            ),
            bottomNavigationBar: NavigationBar(
              selectedIndex: currentPage,
              onDestinationSelected: (int index) {
                if (index == destinations.length - 1) {
                  showDialog(
                    context: context,
                    builder: (BuildContext context) {
                      return AccountDialog();
                    },
                  );
                } else {
                  setState(() {
                    currentPage = index;
                    pageController.animateToPage(
                      currentPage,
                      duration: const Duration(milliseconds: 300),
                      curve: Curves.ease,
                    );
                  });
                }
              },
              destinations: destinations.map(
                (Destination destination) {
                  return NavigationDestination(
                    label: destination.label,
                    icon: destination.icon,
                    selectedIcon: destination.selectedIcon,
                    tooltip: destination.label,
                  );
                },
              ).toList(),
            ),
          );
        }
      },
    );
  }
}

class Destination {
  const Destination(this.label, this.icon, this.selectedIcon);
  final String label;
  final Widget icon;
  final Widget selectedIcon;
}

const List<Destination> destinations = <Destination>[
  Destination(
    'Rooms',
    Icon(Icons.meeting_room_outlined),
    Icon(Icons.meeting_room),
  ),
  Destination(
    'Equipments',
    Icon(Icons.home_repair_service_outlined),
    Icon(Icons.home_repair_service),
  ),
  Destination(
    'Records',
    Icon(Icons.history_outlined),
    Icon(Icons.history),
  ),
  Destination(
    'Account',
    Icon(Icons.account_circle_outlined),
    Icon(Icons.account_circle),
  ),
];

class AccountDialog extends StatefulWidget {
  const AccountDialog({Key? key}) : super(key: key);

  @override
  _AccountDialogState createState() => _AccountDialogState();
}

class _AccountDialogState extends State<AccountDialog> {
  late SharedPreferences sharedPreferences;
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    initializeSharedPreferences();
  }

  Future<void> initializeSharedPreferences() async {
    sharedPreferences = await SharedPreferences.getInstance();
    setState(() {
      isLoading = false;
    });
  }

  Future<void> signOut(BuildContext context) async {}

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      contentPadding:
          const EdgeInsets.symmetric(vertical: 25.0, horizontal: 25.0),
      content: isLoading
          ? const CircularProgressIndicator()
          : Builder(
              builder: (BuildContext context) {
                final String? name = sharedPreferences.getString('name');
                final String? email = sharedPreferences.getString('email');
                final String? profilePicture =
                    sharedPreferences.getString('profile_picture');

                return Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    CircleAvatar(
                      radius: 50,
                      backgroundImage: profilePicture != null
                          ? NetworkImage(profilePicture)
                          : null,
                      child: profilePicture == null
                          ? const Icon(Icons.person)
                          : null,
                    ),
                    const SizedBox(height: 16.0),
                    Text(
                      name.toString().toTitleCase(),
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                          fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8.0),
                    Text(
                      email ?? 'N/A',
                      style: const TextStyle(fontSize: 14),
                    ),
                    const SizedBox(height: 20.0),
                    FilledButton(
                      child: const Padding(
                        padding: EdgeInsets.all(14.0),
                        child: Text('Sign out'),
                      ),
                      onPressed: () {
                        showDialog(
                          context: context,
                          builder: (BuildContext context) {
                            return AlertDialog(
                              title: const Text('Sign out'),
                              content: const Text(
                                  'Are you sure you want to sign out?'),
                              actions: [
                                TextButton(
                                  onPressed: () {
                                    Navigator.pop(context);
                                  },
                                  child: const Text('Cancel'),
                                ),
                                TextButton(
                                  onPressed: () async {
                                    await sharedPreferences.clear();
                                    if (context.mounted)
                                      Navigator.pushReplacement(
                                        context,
                                        MaterialPageRoute(
                                          builder: (BuildContext context) =>
                                              const Login(),
                                        ),
                                      );
                                  },
                                  child: const Text('Sign out'),
                                ),
                              ],
                            );
                          },
                        );
                      },
                    ),
                  ],
                );
              },
            ),
    );
  }
}
