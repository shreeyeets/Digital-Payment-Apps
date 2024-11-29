# UPI Transaction Automation Scripts

## Overview

This project implements automation of UPI (Unified Payments Interface) transactions using Appium, an open-source automation framework for mobile applications. The scripts can interact with multiple UPI apps, simulating user actions and performing transactions.

## Technologies Used

- **Appium**: Open-source mobile automation framework
- **Scrcpy**: Real-time device mirroring and control
- **Supported UPI Apps**: Google Pay, Mobikwik, PayTM, PhonePe

## Features

- Automate UPI transactions across multiple apps
- Transfer of 1 rupee per transaction (customizable)
- Capture transaction duration
- Device screen mirroring for debugging

## Prerequisites

### Software Requirements
- Appium
- Scrcpy
- Node.js
- Android SDK
- ADB (Android Debug Bridge)
- Python 3.10+

### Setup Instructions

1. Install Appium globally
   ```bash
   npm install -g appium

2. Create a Python virtual environment
   ```bash
   python3.10 -m venv appium_env
   source appium_env/bin/activate

3. Install Python dependencies
   ```bash
   pip install appium-python-client

4. Install UIAutomator2 Appium driver
   ```bash
   appium driver install uiautomator2

5. Check driver dependencies
   ```bash
   appium driver doctor uiautomator2

## Device Configuration

- Enable USB Debugging on your Android device
- Set JAVA_HOME and ANDROID_HOME environment variables

## Key Automation Steps

- Contact Selection: Dynamically select contacts using Appium Inspector
- Payment Details Entry: Automate input of contact, amount, and UPI PIN
- Transaction Confirmation: Simulate pay button and handle confirmation prompts
- Performance Tracking: Capture transaction timestamps and duration

## Configuration Notes

- Scripts require modification based on specific device and app
- Some interactions use screen coordinates due to app security measures
- Appium Inspector helps identify UI elements and generate selectors

## Important Considerations

- Carefully review and test scripts before use
- Transactions are performed at your own risk
- Ensure compliance with UPI app terms of service
