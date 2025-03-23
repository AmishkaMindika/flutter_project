import 'package:flutter/material.dart';

class DebatingChatPage extends StatefulWidget {
  @override
  _DebatingChatPageState createState() => _DebatingChatPageState();
}

class _DebatingChatPageState extends State<DebatingChatPage> {
  TextEditingController _controller = TextEditingController();
  List<String> messages = [];
  final List<String> autoResponses = [
    "Interesting point, let's dig deeper!",
    "I disagree, let's explore another perspective.",
    "Great argument, but here's another viewpoint.",
    "That's an interesting perspective, but have you considered this?",
  ];

  void sendMessage() {
    if (_controller.text.isNotEmpty) {
      setState(() {
        messages.add('You: ${_controller.text}');
        messages.add('Opponent: ${autoResponses[(messages.length ~/ 2) % autoResponses.length]}');
      });
      _controller.clear();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Debating Chat'),
        backgroundColor: Colors.green,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Expanded(
              child: ListView.builder(
                itemCount: messages.length,
                itemBuilder: (context, index) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 5),
                    child: Text(
                      messages[index],
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: index % 2 == 0 ? Colors.green : Colors.black,
                      ),
                    ),
                  );
                },
              ),
            ),
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: InputDecoration(
                      hintText: 'Type your argument...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15),
                        borderSide: BorderSide.none,
                      ),
                      filled: true,
                      fillColor: Colors.grey.shade200,
                      contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    ),
                  ),
                ),
                SizedBox(width: 10),
                IconButton(
                  icon: Icon(Icons.send, color: Colors.green),
                  onPressed: sendMessage,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
