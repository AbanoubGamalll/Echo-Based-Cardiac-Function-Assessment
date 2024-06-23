// register_screen.dart
import 'package:flutter/material.dart';
import 'package:flutter/material.dart';

import 'data_login.dart';
import 'login_screen.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  // Attributes For Controller
  var emailController = TextEditingController();

  var userNameController = TextEditingController();

  var passwordController = TextEditingController();

  var confirmPasswordController = TextEditingController();

  bool isPassword = true;

  Icon iconSuff = Icon(Icons.visibility);

  var formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Center(
          child: Text(
            "Register",
            style: TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.bold,
              fontSize: 50,
            ),
            textAlign: TextAlign.center,
          ),
        ),
        backgroundColor: Colors.blueAccent,
        toolbarHeight: 150,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Center(
          child: SingleChildScrollView(
            child: Form(
              key: formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Text "Email Address"
                  Column(
                    children: [
                      TextFormField(
                        controller: emailController,
                        decoration: const InputDecoration(
                          labelText: "Email Address",
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.email),
                        ),
                        keyboardType: TextInputType.emailAddress,
                        validator: (value) {
                          if (value!.isEmpty) {
                            return "Please Fill The Email Address Field";
                          }

                          return null;
                        },
                      ),
                      const SizedBox(height: 40),
                      TextFormField(
                        controller: userNameController,
                        decoration: const InputDecoration(
                          labelText: "User Name",
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.person),
                        ),
                        keyboardType: TextInputType.text,
                        validator: (value) {
                          if (value!.isEmpty) {
                            return "Please Fill The User Name Field";
                          }

                          return null;
                        },
                      ),
                      const SizedBox(height: 40),
                      TextFormField(
                        controller: passwordController,
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
                        validator: (value) {
                          if (value!.isEmpty) {
                            return "Please Fill The Password Field";
                          }

                          return null;
                        },
                        keyboardType: TextInputType.visiblePassword,
                        obscureText: isPassword,
                      ),
                      const SizedBox(height: 40),
                      TextFormField(
                        controller: confirmPasswordController,
                        decoration: InputDecoration(
                          labelText: "Confirm Password",
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
                          if (value != passwordController.text) {
                            return "The Confirm Password Doesn't match The Password";
                          }
                          if (value!.isEmpty) {
                            return "Please Fill The Confirm Password Field";
                          }

                          return null;
                        },
                      ),
                    ],
                  ),

                  const SizedBox(height: 80),

                  //   Button "Register"
                  Container(
                    alignment: Alignment.bottomCenter,
                    child: MaterialButton(
                      onPressed: () {
                        setState(() {
                          if (formKey.currentState!.validate()) {
                            Navigator.pushAndRemoveUntil(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => const LoginScreen()),
                              (route) => false,
                            );
                            DataLogin.userName = userNameController.text;
                            DataLogin.emailAddress = emailController.text;
                            DataLogin.password = passwordController.text;
                          }
                        });
                      },
                      color: Colors.blueAccent,
                      minWidth: double.infinity,
                      height: 60,
                      child: const Text(
                        "SUBMIT",
                        style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 30,
                            color: Colors.white),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
