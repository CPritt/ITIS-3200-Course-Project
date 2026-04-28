# ITIS 3200 Course Project

## Overview

An interactive console application that demonstrates how common symmetric encryption schemes work, including their vulnerabilities and how they can be exploited.

## Dependencies

- Python 3.x
- cryptography — `pip install cryptography` or `pip3 install cryptography`

## Setup

1. Install the required library using the command above
2. Run the program with `python main.py` or `python3 main.py`

## Description

This program allows the user to choose different AES encryption modes and step through the encryption and decryption process for each one. It also demonstrates a real vulnerability for each mode, showing a concrete fail case so the user can see exactly how and why the scheme breaks down.
The goal is to provide a hands-on learning experience for entry-level symmetric key encryption, covering how each mode works and what makes some configurations insecure.
