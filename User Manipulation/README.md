# User Manipulation

A fully functional web application for managing users and posts, featuring a beautiful UI and responsive design.

## Features

- **User Management**
  - Add new users
  - Remove users
  - Log in / Log out
- **Post Management**
  - Create new posts
  - Edit posts
  - Remove posts
- **Security**
  - Password hashing
- **Responsive Design**
  - Works perfectly on desktop, tablet, and mobile

## Tech Stack

- **Backend:** Flask, Python
- **Frontend:** HTML, CSS
- **Database:** sqlalchemy
- **Authentication:** Flask-Login

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/victorxavier01/Python.git

2. Make a secret key:
Create a .env file and write your secret key.  
Example:
   ```bash
   SECRET_KEY = "YOUR-SECRET-KEY"
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Run the application:
   ```bash
   flask run

5. Open your browser and enter:
    ```bash
    http://localhost:5000

## Usage

- Sign up or log in to access the dashboard.

- Create, edit, or delete posts.

- Manage users (admin access required).

## Contributing

Feel free to submit issues or pull requests. Contributions are welcome!

## License

[MIT](https://choosealicense.com/licenses/mit/)