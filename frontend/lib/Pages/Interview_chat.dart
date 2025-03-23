import 'package:flutter/material.dart';

class InterviewChatPage extends StatefulWidget {
  @override
  _InterviewChatPageState createState() => _InterviewChatPageState();
}

class _InterviewChatPageState extends State<InterviewChatPage> {
  final TextEditingController _messageController = TextEditingController();
  final List<Map<String, String>> _messages = [];

  final Map<String, String> interviewResponses = {
    "Tell me about yourself": "I'm an AI assistant here to help you with interview questions!",
    "What are your strengths?": "I am highly adaptable, quick to learn, and excel in problem-solving.",
    "What are your weaknesses?": "I sometimes focus too much on details, but I'm working on balancing perfection with efficiency.",
    "Why do you want this job?": "I am passionate about this field and believe I can contribute meaningfully to the company.",
    "Where do you see yourself in 5 years?": "I see myself growing into a leadership role and contributing to impactful projects.",
  };

  void _sendMessage() {
    String message = _messageController.text.trim();
    if (message.isEmpty) return;

    setState(() {
      _messages.add({"sender": "user", "text": message});
    });

    Future.delayed(Duration(seconds: 1), () {
      setState(() {
        _messages.add({
          "sender": "bot",
          "text": interviewResponses[message] ?? "That's interesting! Can you elaborate?"
        });
      });
    });

    _messageController.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.green.shade50,
      appBar: AppBar(
        title: Text(
          'Interview Chat',
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.black),
        ),
        centerTitle: true,
        backgroundColor: Colors.green.shade200,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                bool isUser = message["sender"] == "user";
                return Align(
                  alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: EdgeInsets.symmetric(vertical: 5, horizontal: 10),
                    padding: EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: isUser ? Colors.green.shade300 : Colors.white,
                      borderRadius: BorderRadius.circular(15),
                    ),
                    child: Text(
                      message["text"]!,
                      style: TextStyle(fontSize: 16, color: isUser ? Colors.white : Colors.black),
                    ),
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(12.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    decoration: InputDecoration(
                      hintText: 'Type a message...',
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(20)),
                      filled: true,
                      fillColor: Colors.white,
                    ),
                  ),
                ),
                SizedBox(width: 10),
                CircleAvatar(
                  backgroundColor: Colors.green.shade300,
                  child: IconButton(
                    icon: Icon(Icons.send, color: Colors.white),
                    onPressed: _sendMessage,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
