# Password-Manager


A secure and user-friendly password manager application built with Python and Flask. This application allows users to store, manage, and retrieve their passwords efficiently.

## Features

### **Core Functionalities**
- **User Registration & Login**:
  - Secure registration with password strength enforcement.
  - User authentication with hashed master passwords stored in the database.

- **Add Passwords**:
  - Save credentials (website, username, and password) in an encrypted database.
  - Password encryption using PBKDF2-HMAC-SHA256 and Fernet (AES encryption).

- **View Passwords**:
  - Secure password retrieval with decryption on demand.
  - Displays the website, username, and decrypted password in a user-friendly vault.

- **Edit Passwords**:
  - Update stored website, username, and password details.
  - Automatically re-encrypts updated passwords with a new salt.

- **Delete Passwords**:
  - Permanently remove passwords from the vault.

- **Change Master Password**:
  - Re-encrypt all stored passwords when the master password is updated.
  - Generates new salts for enhanced security.

### **Advanced Features**
- **Password Generation**:
  - Generate strong passwords with customizable settings:
    - Length of password.
    - Inclusion of uppercase letters, digits, and symbols.
  - Validation to ensure generated passwords meet stringent security criteria.

- **Session Management**:
  - Session-based authentication using Flask-Session.
  - Automatic session clearing upon logout to ensure data privacy.

- **Search Functionality**:
  - Easily locate passwords within the vault by website or username.

- **Database Security**:
  - Encrypted password storage with unique salts for each entry.
  - Automatic re-encryption when passwords or the master password is updated.

- **Input Validation**:
  - Enforces a strong password policy during registration:
    - Minimum 8 characters.
    - At least one uppercase letter, one lowercase letter, one digit, and one symbol.
## Requirements

- Python 3.x
- Flask
- SQLite

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/SakshiiRK/Password-Manager.git
   cd Password-Manager
