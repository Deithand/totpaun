# **TOTP Authenticator**

The TOTP Authenticator is a robust desktop application designed for the efficient management of Time-based One-Time Passwords (TOTP). Developed utilizing Python and the PyQt6 framework, this application facilitates the secure storage of cryptographic secret keys and the subsequent generation of 6-digit authentication codes. It supports a diverse array of online services, including but not limited to GitHub, Google, and Dropbox.

## **Key Features**

* **Secure Local Storage of Secret Keys**: All TOTP secret keys are securely maintained within a localized secrets.json file, ensuring data residency and control.  
* **Intuitive User Interface**: The application provides a clean and straightforward graphical interface, enabling users to effortlessly add, remove, and manage their authentication accounts.  
* **Real-time Code Generation**: TOTP codes are dynamically updated every 30 seconds, guaranteeing the provision of current and valid authentication credentials.  
* **Expedited Code Copying**: A single click allows for the instantaneous transfer of generated codes to the system clipboard, streamlining the authentication process.  
* **Visual Time Indicator**: A prominent progress bar, coupled with a countdown timer, visually represents the remaining validity period of the current code, enhancing user awareness.  
* **Cross-Platform Compatibility**: Leveraging the PyQt6 framework, the application demonstrates compatibility across various operating systems.

## **Operational Setup**

### **System Requirements**

* Python version 3.x  
* The PyQt6 and pyotp libraries

### **Installation Procedure**

1. **Repository Cloning**: The project repository can be cloned, or the totp\_client.py file may be downloaded directly:  
   git clone https://github.com/your-username/totp-authenticator.git  
   cd totp-authenticator

   *Note: It is advisable to substitute your-username with the actual GitHub username if the project is hosted on GitHub.*  
2. **Dependency Installation**: Navigate to the project directory within a terminal or command prompt and execute the following command to install the requisite libraries:  
   pip install PyQt6 pyotp

### **Application Execution**

Subsequent to the successful installation of dependencies, the application can be initiated by executing the primary script:

python totp\_client.py

## ** Usage Guidelines**

### **Account Addition Protocol**

1. Initiate the process by clicking the **"ADD ACCOUNT"** button, located at the bottom of the application window.  
2. A dialog box will subsequently appear, prompting for an **"ACCOUNT NAME"** (e.g., "GitHub", "Google").  
3. Enter the **"SECRET KEY"** obtained from the respective service during the two-factor authentication setup.  
4. An optional **"Show secret key"** checkbox is provided for visual verification of the entered key.  
5. Conclude the addition process by clicking **"ADD"**.

Upon successful validation, the newly added account will be displayed in the list, accompanied by its current TOTP code.

### **Account Deletion Protocol**

1. To remove an account, click the **"DELETE"** button positioned adjacent to the target account.  
2. A confirmation dialog will appear, requiring user affirmation to proceed with the deletion.

### **Code Copying Protocol**

1. To copy an authentication code, click the **"COPY"** button associated with the desired account's code.  
2. The code will be transferred to the system clipboard, and the button's text will temporarily change to "COPIED" to indicate successful operation.

## **Underlying Technologies**

* [Python](https://www.python.org/)  
* [PyQt6](https://www.riverbankcomputing.com/software/pyqt/intro)  
* [pyotp](https://pyotp.readthedocs.io/en/latest/)  
* [JSON](https://www.json.org/json-en.html)

## **Security Considerations**

The secret keys are stored in a secrets.json file, co-located with the application's executable. It is imperative to note that **this file is not encrypted at rest**, thereby necessitating stringent security measures on the host system. The implementation of disk encryption or other system-level security protocols is strongly recommended to safeguard the confidentiality of these sensitive credentials.

## **Contribution Guidelines**

Contributions to this project are highly encouraged. Individuals interested in submitting suggestions, reporting defects, or proposing new functionalities are invited to follow the standard contribution workflow:

1. Fork the repository.  
2. Create a new branch (e.g., git checkout \-b feature/ImprovedFunctionality).  
3. Commit your modifications with a descriptive message (e.g., git commit \-m 'Implement improved functionality').  
4. Push the changes to your designated branch (e.g., git push origin feature/ImprovedFunctionality).  
5. Submit a Pull Request for review.

## **License Agreement**

This project is distributed under the MIT License. Comprehensive details regarding the terms and conditions of this license are available in the LICENSE file (if applicable).
