import 'package:cardic_function_assement_2/register_screen.dart';
import 'package:cardic_function_assement_2/video_upload_screen.dart';
import 'package:flutter/material.dart';

import 'data_login.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  // Attributes For Controller
  var emailController = TextEditingController();

  var userNameController = TextEditingController();

  var passwordController = TextEditingController();

  bool isPassword = true;

  Icon iconSuff = const Icon(Icons.visibility);

  var formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Login",
          style: TextStyle(
            fontSize: 40,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
          // textAlign: TextAlign.center,
        ),
        backgroundColor: Colors.blueAccent,
        toolbarHeight: 120,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: SingleChildScrollView(
          child: Form(
            key: formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                SizedBox(height: 50),
                // Text "Email Address"
                const Text(
                  "Email Address",
                  style: TextStyle(fontWeight: FontWeight.w500, fontSize: 25),
                ),
                const SizedBox(height: 20),
                TextFormField(
                  controller: emailController,
                  key: const Key("Email Field"),
                  decoration: const InputDecoration(
                    labelText: "Email Address",
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.email),
                  ),
                  keyboardType: TextInputType.emailAddress,
                  validator: (value) {
                    if (value!.isEmpty) {
                      return "Please Fill The Email Field";
                    }
                    if (value != DataLogin.emailAddress) {
                      return "The Email Address Is Wrong";
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 60),

                //Text "Password"
                const Text(
                  "Password",
                  style: TextStyle(fontWeight: FontWeight.w500, fontSize: 25),
                ),
                const SizedBox(height: 20),
                TextFormField(
                  controller: passwordController,
                  key: const Key("Password Field"),
                  decoration: InputDecoration(
                    labelText: "Password",
                    border: const OutlineInputBorder(),
                    prefixIcon: const Icon(Icons.lock),
                    suffixIcon: IconButton(
                      onPressed: () {
                        setState(() {
                          isPassword = !isPassword;
                        });
                      },
                      icon: isPassword
                          ? const Icon(Icons.visibility)
                          : const Icon(Icons.visibility_off),
                    ),
                  ),
                  keyboardType: TextInputType.visiblePassword,
                  obscureText: isPassword,
                  validator: (value) {
                    if (value!.isEmpty) {
                      return "Please Fill The Password Field";
                    }
                    if (value != DataLogin.password) {
                      return "The Password Is Wrong";
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 90),

                //   Button "Login"
                Container(
                  alignment: Alignment.bottomCenter,
                  child: MaterialButton(
                    onPressed: () {
                      setState(() {
                        if (formKey.currentState!.validate()) {
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => VideoUploadScreen()));
                        }
                      });
                    },
                    color: Colors.blueAccent,
                    minWidth: double.infinity,
                    height: 50,
                    child: const Text(
                      "Login",
                      style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 25,
                          color: Colors.white),
                    ),
                  ),
                ),

                const SizedBox(height: 10),

                // Text "Have No Account" & TextButton "Register"
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text("Don't have an account?"),
                    TextButton(
                        onPressed: () {
                          setState(() {
                            Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) => RegisterScreen(),
                                ));
                          });
                        },
                        child: const Text("Register"))
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
