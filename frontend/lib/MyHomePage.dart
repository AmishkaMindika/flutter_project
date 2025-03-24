import 'package:flutter/material.dart';
import 'package:flutter_project/style/colour.dart';
import 'Pages/community_page.dart';
import 'Pages/conversation_branch_page.dart';
import 'Pages/progress_tracking_page.dart';
import 'Pages/settings_page.dart';
import 'profile_screen.dart';
import 'voice_practice_screen.dart';
import 'community_chat_screen.dart';
import 'ice_breaker_screen.dart';
import 'models/user.dart';

class HomePage extends StatefulWidget {
  final User user;

  const HomePage({super.key, required this.user});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int currentPageIndex = 0;

  final List<Map<String, dynamic>> gridItems = [
    {
      "color": AppColors.green_5,
      "image": "assets/ai_chatbot_icon.png",
      "title": "Conversation Branch",
      "page": const ConversationBranchPage(),
    },
    {
      "color": AppColors.green_4,
      "image": "assets/voice_practice_icon.png",
      "title": "Voice Practice",
      "page": VoicePracticeScreen(userName: "User"),
    }
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: currentPageIndex,
        children: [
          buildHomeScreen(context),
          const ProgressTrackingPage(),
          const CommunityPage(),
          const SettingsPage(),
        ],
      ),
      bottomNavigationBar: NavigationBar(
        backgroundColor: AppColors.green_5,
        selectedIndex: currentPageIndex,
        onDestinationSelected: (int index) {
          setState(() {
            currentPageIndex = index;
          });
        },
        destinations: const <NavigationDestination>[
          NavigationDestination(icon: Icon(Icons.home), label: "Home"),
          NavigationDestination(icon: Icon(Icons.bar_chart_rounded), label: "Progress"),
          NavigationDestination(icon: Icon(Icons.people_alt_rounded), label: "Community"),
          NavigationDestination(icon: Icon(Icons.settings), label: "Settings"),
        ],
      ),
    );
  }

  Widget buildHomeScreen(BuildContext context) {
    var size = MediaQuery.of(context).size;
    return Scaffold(
      body: Stack(
        children: <Widget>[
          Container(
            height: size.height * .45,
            decoration: BoxDecoration(color: AppColors.green_2),
          ),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 5),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Align(
                    alignment: Alignment.topRight,
                    child: GestureDetector(
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => ProfileScreen(user: widget.user),
                          ),
                        ).then((_) {
                          setState(() {});
                        });
                      },
                      child: CircleAvatar(
                        backgroundColor: AppColors.green_3,
                        radius: 30,
                        child: Icon(Icons.account_circle_outlined, size: 50, color: AppColors.textMain),
                      ),
                    ),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    "Welcome, ${widget.user.name}!",
                    style: TextStyle(fontSize: 40, fontWeight: FontWeight.w800, color: AppColors.textMain),
                  ),
                  const SizedBox(height: 10),
                  buildIceBreakerCard(context),
                  const SizedBox(height: 50),
                  Expanded(
                    child: GridView.builder(
                      itemCount: gridItems.length,
                      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount: 2,
                        crossAxisSpacing: 10,
                        mainAxisSpacing: 10,
                        childAspectRatio: .75,
                      ),
                      itemBuilder: (context, index) {
                        final item = gridItems[index];
                        return GestureDetector(
                          onTap: () {
                            Navigator.push(context, MaterialPageRoute(builder: (context) => item["page"]));
                          },
                          child: Container(
                            decoration: BoxDecoration(
                              color: item["color"],
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Image.asset(item["image"], width: 150, height: 145, fit: BoxFit.cover),
                                Text(
                                  item["title"],
                                  textAlign: TextAlign.center,
                                  style: TextStyle(fontWeight: FontWeight.w800, fontSize: 25, color: AppColors.background),
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget buildIceBreakerCard(BuildContext context) {
    return Container(
      width: MediaQuery.of(context).size.width,
      height: 220,
      decoration: BoxDecoration(
        gradient: LinearGradient(colors: [AppColors.green_1, AppColors.green_3]),
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(20),
          topRight: Radius.circular(80),
          bottomRight: Radius.circular(20),
          bottomLeft: Radius.circular(20),
        ),
        boxShadow: [BoxShadow(offset: const Offset(10, 10), blurRadius: 10, color: AppColors.green_1)],
      ),
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text("Dive Into \nYour Daily Ice Breaker \nSession",
              style: TextStyle(fontSize: 25, fontWeight: FontWeight.w600, color: AppColors.background)),
          Align(
            alignment: Alignment.bottomRight,
            child: IconButton(
              icon: Icon(Icons.play_circle_outline_rounded, size: 50, color: AppColors.textMain),
              onPressed: () {
                Navigator.push(context, MaterialPageRoute(builder: (context) => IceBreakerScreen(userName: widget.user.name)));
              },
            ),
          ),
        ],
      ),
    );
  }
}
