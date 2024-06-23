// video_upload_screen.dart
import 'dart:io';

import 'package:cardic_function_assement_2/api_result.dart';
import 'package:cardic_function_assement_2/api_result.dart';
import 'package:cardic_function_assement_2/load_flash_screen.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:http/http.dart' as http;
import 'package:video_player/video_player.dart';

// import 'package:image_picker/image_picker.dart';
// import 'package:video_player/video_player.dart';

class VideoUploadScreen extends StatefulWidget {
  const VideoUploadScreen({super.key});

  @override
  _VideoUploadScreenState createState() => _VideoUploadScreenState();
}

class _VideoUploadScreenState extends State<VideoUploadScreen> {
  VideoPlayerController _videoPlayerController =
      VideoPlayerController.file(File(""));

  late Future<void> _initializeVideoPlayerFuture;

  // @override
  // void initState() {
  //   super.initState();
  //   _videoPlayerController = VideoPlayerController.asset(
  //     "assets/videos/sample_video.mp4",
  //   );
  //   _initializeVideoPlayerFuture = _videoPlayerController.initialize();
  // }

  @override
  void dispose() {
    _videoPlayerController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          toolbarHeight: 70,
          leading: const Icon(
            Icons.menu,
            color: Colors.white,
          ),
          title: const Center(
            child: Text(
              'Upload Video',
              style: TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.bold,
                fontSize: 30,
              ),
              textAlign: TextAlign.center,
            ),
          ),
          backgroundColor: Colors.blueAccent,
        ),
        body: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Container(
            width: double.infinity,
            decoration: const BoxDecoration(
              image: DecorationImage(
                image: AssetImage("assets/images/uploadImage.jpg"),
                fit: BoxFit.cover,
              ),
            ),
            child: Column(
              // mainAxisAlignment: MainAxisAlignment.end,
              // crossAxisAlignment: ,
              children: [
                SizedBox(height: 10),
                const Text(
                  "Please Pick a Video",
                  style: TextStyle(
                      color: Colors.blueAccent,
                      fontSize: 25,
                      fontStyle: FontStyle.italic),
                ),
                SizedBox(height: 20),
                Container(
                  width: double.infinity,
                  alignment: Alignment.bottomCenter,
                  child: MaterialButton(
                    onPressed: () async {
                      FilePickerResult? result =
                          await FilePicker.platform.pickFiles(
                        type: FileType.video,
                        allowCompression: true,
                      );
                      if (result != null) {
                        PlatformFile file = result.files.first;
                        _videoPlayerController = VideoPlayerController.file(
                            File(file.path.toString()))
                          ..initialize().then((_) {
                            setState(() {});
                            _initializeVideoPlayerFuture = _videoPlayerController
                                .initialize(); // Rebuild the widget to show the video
                          });
                        APIResult.videoPath = file.path.toString();
                      } else {
                        // User canceled the picker
                      }
                    },
                    color: Colors.blueAccent,
                    child: const Text("Upload Video",
                        style: TextStyle(
                            color: Colors.white,
                            fontSize: 30,
                            fontWeight: FontWeight.bold,
                            fontStyle: FontStyle.italic)),
                  ),
                ),
                const SizedBox(height: 20),

                _videoPlayerController.value.isInitialized
                    ? FutureBuilder(
                        future: _initializeVideoPlayerFuture,
                        builder: (context, snapshot) {
                          if (snapshot.connectionState ==
                              ConnectionState.done) {
                            return AspectRatio(
                              aspectRatio:
                                  _videoPlayerController.value.aspectRatio,
                              child: Stack(
                                alignment: Alignment.bottomCenter,
                                children: [
                                  VideoPlayer(_videoPlayerController),
                                  IconButton(
                                    onPressed: () {
                                      setState(() {
                                        if (_videoPlayerController
                                            .value.isPlaying) {
                                          _videoPlayerController.pause();
                                        } else {
                                          _videoPlayerController.play();
                                        }
                                      });
                                    },
                                    icon: Icon(
                                      _videoPlayerController.value.isPlaying
                                          ? Icons.pause
                                          : Icons.play_arrow,
                                      size: 50,
                                      color: Colors.white,
                                    ),
                                  ),
                                ],
                              ),
                            );
                          } else {
                            return Text("");
                          }
                        },
                      )
                    : const Text('No video selected'),
                // _videoPlayerController.value.isInitialized
                //     ? AspectRatio(
                //         aspectRatio: _videoPlayerController.value.aspectRatio,
                //         child: VideoPlayer(_videoPlayerController),
                //       )
                //     : const Text('No video selected'),
                Expanded(
                  child: Container(
                    width: double.infinity,
                    height: double.infinity,
                    alignment: Alignment.bottomCenter,
                    child: MaterialButton(
                      onPressed: () {
                        if (_videoPlayerController.value.isInitialized) {
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => const LoadingScreen()));
                        } else {
                          // Show alert dialog
                          showDialog(
                              context: context,
                              builder: (BuildContext context) {
                                return AlertDialog(
                                  title: const Text(
                                    "ALERT:",
                                    style: TextStyle(color: Colors.red),
                                  ),
                                  content: const Text(
                                    "Please Pick a Video First",
                                    style: TextStyle(
                                        fontSize: 20, color: Colors.red),
                                  ),
                                  actions: [
                                    TextButton(
                                      onPressed: () {
                                        Navigator.of(context).pop();
                                      },
                                      child: const Text("OK"),
                                    ),
                                  ],
                                );
                              });
                        }
                      },
                      color: Colors.blueAccent,
                      child: const Text("Analyze The Video",
                          style: TextStyle(
                              color: Colors.white,
                              fontSize: 25,
                              fontWeight: FontWeight.bold,
                              fontStyle: FontStyle.italic)),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ));
  }
}
