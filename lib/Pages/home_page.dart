import 'package:flutter/material.dart';
import 'package:frontend_part_2/Pages/community_page.dart';
import 'package:frontend_part_2/Pages/conversation_branch_page.dart';
import 'package:frontend_part_2/Pages/help_page.dart';
import 'package:frontend_part_2/Pages/progress_tracking_page.dart';
import 'package:frontend_part_2/Pages/settings_page.dart';
import 'package:frontend_part_2/style/colour.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  // Track selected tab index
  int currentPageIndex = 0;

  final List<Map<String,dynamic>> gridItem = [
    {
      "color" : AppColors.green_5,
      "image" : "Assets/ai_chatbot_icon.png",
      "title" : "Conversation Branch",
      "page"  : const ConversationBranchPage(),
    },
    {
      "color" : AppColors.green_4,
      "image" : "Assets/voice_practice_icon.png",
      "title" : "Voice Practice Branch",
      "page"  : const CommunityPage() //Add Voice Practice Page here
    }
  ];
  @override
  Widget build(BuildContext context){
    return Scaffold(
      body: IndexedStack(
        //The Bottom Navigation's Options are places here
        index: currentPageIndex,
        children: [
          buildHomeScreen(context), //home_page
          const ProgressTrackingPage(), // progress_tracking page
          const CommunityPage(), // add Community Page here to the nav bar
          const SettingsPage(), //Settings page
        ],
      ),
      bottomNavigationBar: NavigationBarTheme(
        data: NavigationBarThemeData(
          indicatorColor: AppColors.textMain,
          labelTextStyle: WidgetStateProperty.all(
            TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.bold,
              color: AppColors.textMain
            ),
          ),
        ),
        child: NavigationBar(
          backgroundColor: AppColors.green_5,
          selectedIndex: currentPageIndex,
          onDestinationSelected: (int index){
            setState(() {
              currentPageIndex = index;
            });
          },
          destinations: const<NavigationDestination> [
            NavigationDestination(
              icon: Icon(
                Icons.home,
              ),
              label: "Home",
            ),
            NavigationDestination(
              icon: Icon(
                Icons.bar_chart_rounded,
              ),
              label: "Progress",
            ),
            NavigationDestination(
              icon: Icon(
                Icons.people_alt_rounded,
              ),
              label: "Community",
            ),
            NavigationDestination(
              icon: Icon(
                Icons.settings,
              ),
              label: "Settings",
            ),
          ],
        ),
      ),
    );
  }
  Widget buildHomeScreen(BuildContext context) {
    var size = MediaQuery.of(context).size; //gives total height of device
    return Scaffold(
      body: Stack(
        children: <Widget>[Container(
          height: size.height * .45,
          decoration: BoxDecoration(
            color: AppColors.green_2,
            )
          ),
          SafeArea(
              child:Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20 , vertical: 5),
                child: Column(
                  crossAxisAlignment:CrossAxisAlignment.start,
                  children:[
                    Align(
                      alignment: Alignment.topRight,
                      child: Container(
                        alignment: Alignment.center,
                        height: 60,
                        width: 60,
                        decoration: BoxDecoration(
                          color: AppColors.green_3,
                          shape: BoxShape.circle,
                        ),
                        child: Icon(
                          Icons.account_circle_outlined,
                          size: 50,
                          color: AppColors.textMain,
                        ),
                      ),
                    ),
                    Text(
                        "Welcome",
                      style: TextStyle(
                        fontSize: 40,
                        fontWeight: FontWeight.w800,
                        color: AppColors.textMain,
                      )
                    ),
                    SizedBox(height: 10,),

                    //Section for ice breaker session must be connected here
                    Container(
                      width: MediaQuery.of(context).size.width,
                      height: 200,
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [AppColors.green_1, AppColors.green_3]
                        ),
                        borderRadius: BorderRadius.only(
                          topLeft: Radius.circular(20),
                          topRight: Radius.circular(80),
                          bottomRight: Radius.circular(20),
                          bottomLeft: Radius.circular(20),
                        ),
                        boxShadow: [
                          BoxShadow(
                            offset: Offset(10, 10),
                            blurRadius: 10,
                            color: AppColors.green_1,
                          )
                        ]
                      ),
                      child: Container(
                        padding: const EdgeInsets.only(left: 20,top: 20,right: 20),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              "Dive Into \nYour Daily Ice Breaker \nSession",
                              style: TextStyle(
                                fontSize: 25,
                                fontWeight: FontWeight.w600,
                                color: AppColors.background,
                              ),
                            ),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.end,
                              children: [
                                GestureDetector(
                                  onTap: (){
                                    Navigator.push(
                                        context,
                                      MaterialPageRoute(builder: (context) => ProgressTrackingPage()) //Add Ice breaker session page here
                                    );
                                  },
                                  child: Icon(
                                    Icons.play_circle_outline_rounded,
                                    size: 50,
                                    color: AppColors.textMain,
                                  ),
                                )
                              ],
                            )
                          ],
                        ),
                      ),
                    ),
                    SizedBox(height: 50,),
                    Expanded(
                      child: GridView.builder(
                        itemCount: gridItem.length,
                          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                            crossAxisCount: 2,
                            crossAxisSpacing: 10,
                            mainAxisSpacing: 10,
                            childAspectRatio: .75
                          ),
                        itemBuilder: (context,index){
                          final item = gridItem[index];
                          return GestureDetector(
                            onTap: (){
                              Navigator.push(
                                context,
                                MaterialPageRoute(builder: (context) => item["page"]
                                ),
                              );
                            },
                            child: Container(
                              decoration: BoxDecoration(
                                color: item["color"],
                                borderRadius: BorderRadius.circular(20),
                              ),
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  Image.asset(
                                    item["image"],
                                    width: 150,
                                    height: 145,
                                    fit: BoxFit.cover,
                                  ),
                                  Text(
                                    item["title"],
                                    textAlign: TextAlign.center,
                                    style: TextStyle(
                                      fontWeight: FontWeight.w800,
                                      fontSize: 25,
                                      color: AppColors.background
                                    ),
                                  )
                                ],
                              ),
                            ),
                          );

                        },
                      ),
                    )
                  ],
                ),
              )
          )
        ]
      ),
    );
  }
}
