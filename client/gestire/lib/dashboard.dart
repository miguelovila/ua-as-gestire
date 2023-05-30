import 'package:flutter/material.dart';
import 'package:gestire/rooms.dart';
import 'package:gestire/equipments.dart';
import 'package:gestire/records.dart';

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
        if (constraints.maxWidth < 800) {
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
                Account(),
              ],
            ),
            bottomNavigationBar: NavigationBar(
              selectedIndex: currentPage,
              onDestinationSelected: (int index) {
                setState(() {
                  currentPage = index;
                  pageController.animateToPage(
                    currentPage,
                    duration: const Duration(milliseconds: 300),
                    curve: Curves.ease,
                  );
                });
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
        } else if (constraints.maxWidth >= 800 && constraints.maxWidth < 1000) {
          // Navigation Rail with hidden labels
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
                          return AlertDialog(
                            title: const Text('Account Dialog'),
                            content:
                                const Text('This is the account dialog box.'),
                            actions: [
                              TextButton(
                                onPressed: () {
                                  Navigator.of(context).pop();
                                },
                                child: const Text('Close'),
                              ),
                            ],
                          );
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
                      Account(),
                    ],
                  ),
                ),
              ],
            ),
          );
        } else {
          // Navigation Rail with visible labels
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
                          return AlertDialog(
                            title: const Text('Account Dialog'),
                            content:
                                const Text('This is the account dialog box.'),
                            actions: [
                              TextButton(
                                onPressed: () {
                                  Navigator.of(context).pop();
                                },
                                child: const Text('Close'),
                              ),
                            ],
                          );
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
                  labelType: NavigationRailLabelType.all,
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
                      Account(),
                    ],
                  ),
                ),
              ],
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

class Account extends StatelessWidget {
  const Account({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Account'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            showDialog(
              context: context,
              builder: (BuildContext context) {
                return AlertDialog(
                  title: const Text('Account Dialog'),
                  content: const Text('This is the account dialog box.'),
                  actions: [
                    TextButton(
                      onPressed: () {
                        Navigator.of(context).pop();
                      },
                      child: const Text('Close'),
                    ),
                  ],
                );
              },
            );
          },
          child: const Text('Open Account Dialog'),
        ),
      ),
    );
  }
}
