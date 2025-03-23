import 'package:flutter/material.dart';
import '../style/colour.dart';

class ConversationBranchPage extends StatefulWidget {
  const ConversationBranchPage({super.key});

  @override
  State<ConversationBranchPage> createState() => _ConversationBranchPageState();
}

class _ConversationBranchPageState extends State<ConversationBranchPage> {
  final List<Map<String, String>> chatBranches = [
    {
      "imagePath": "assets/interview_chat_icon.png",
      "title": "Interview Branch",
      "description": "Learn how to communicate in an Interview"
    },
    {
      "imagePath": "assets/debating_icon.png",
      "title": "Debating Branch",
      "description": "Go head to head in a debate and test yourself"
    },
    {
      "imagePath": "assets/public_speaking_icon.png",
      "title": "Public Speaking Branch",
      "description": "Immerse yourself in front of a large crowd"
    },
    {
      "imagePath": "assets/casual_talk_icon.png",
      "title": "Casual Chat Branch",
      "description": "Just have a Casual Chat"
    },
    {
      "imagePath": "assets/funny_talk_icon.png",
      "title": "Funny Chat Branch",
      "description": "Make a funny joke and talk"
    },
  ];

  void navigateToChat(String branchTitle) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ChatScreen(branchTitle: branchTitle),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [AppColors.green_1, AppColors.green_3],
            begin: const FractionalOffset(0.0, 0.4),
            end: Alignment.topRight,
          ),
        ),
        child: Column(
          children: [
            Container(
              padding: const EdgeInsets.only(top: 70, left: 20, right: 20),
              width: MediaQuery.of(context).size.width,
              height: 250,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      GestureDetector(
                        onTap: () {
                          Navigator.pop(context);
                        },
                        child: Icon(
                          Icons.arrow_back_ios,
                          size: 25,
                          color: AppColors.textMain,
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 30),
                  Text(
                    "Conversation \nBranch",
                    style: TextStyle(
                      fontSize: 30,
                      fontWeight: FontWeight.w500,
                      color: AppColors.textMain,
                    ),
                  ),
                ],
              ),
            ),
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: AppColors.background,
                  borderRadius: BorderRadius.only(
                    topRight: Radius.circular(70),
                  ),
                ),
                child: Column(
                  children: [
                    SizedBox(height: 30),
                    Row(
                      children: [
                        SizedBox(width: 20),
                        Text(
                          "Chat Branches",
                          style: TextStyle(
                            fontSize: 25,
                            fontWeight: FontWeight.bold,
                            color: AppColors.green_1,
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 20),
                    Expanded(
                      child: ListView.builder(
                        itemCount: chatBranches.length,
                        itemBuilder: (context, index) {
                          return Padding(
                            padding: const EdgeInsets.only(bottom: 10.0),
                            child: GestureDetector(
                              onTap: () => navigateToChat(chatBranches[index]["title"]!),
                              child: buildStackItem(
                                imagePath: chatBranches[index]["imagePath"]!,
                                title: chatBranches[index]["title"]!,
                                description: chatBranches[index]["description"]!,
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
      ),
    );
  }
}

Widget buildStackItem({
  required String imagePath,
  required String title,
  required String description,
}) {
  return Card(
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(20),
    ),
    elevation: 10,
    child: Container(
      height: 150,
      width: double.infinity,
      padding: const EdgeInsets.all(20.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            child: Column(
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: AppColors.green_1,
                  ),
                ),
                SizedBox(height: 5),
                Text(
                  description,
                  style: TextStyle(
                    fontSize: 15,
                    color: AppColors.textSub,
                  ),
                ),
              ],
            ),
          ),
          SizedBox(width: 20),
          ClipRRect(
            borderRadius: BorderRadius.only(
              topRight: Radius.circular(20),
            ),
            child: Image.asset(
              imagePath,
              width: 100,
              height: 100,
              fit: BoxFit.cover,
            ),
          ),
        ],
      ),
    ),
  );
}

class ChatScreen extends StatelessWidget {
  final String branchTitle;
  const ChatScreen({super.key, required this.branchTitle});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(branchTitle),
        backgroundColor: AppColors.green_3,
      ),
      body: Center(
        child: Text("Chat for $branchTitle"),
      ),
    );
  }
}

