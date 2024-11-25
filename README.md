# RadinSport Admin Panel

## Overview

The RadinSport Admin Panel is a Flask-based API application designed for managing and supporting products in an e-commerce system. It provides various endpoints for updating order statuses, managing product categories, searching products, handling images, and more.

---

## Features

- **Order Management:**
  - Update order statuses.
  
- **Product Management:**
  - Search for products by category or DKP code.
  - Retrieve product details with dynamic title modifications.
  
- **Image Handling:**
  - Upload product images to the server.
  - Remove product images from the server.
  - List available images for a specific product.

---

## API Endpoints

### 1. `/support_update_status` (POST)
Updates the status of an order.

- **Request Body:**
  - `variable1`: Order number.
  - `variable2`: New status.
  
- **Response:**
  - JSON message confirming the update.

---

### 2. `/support_open_category` (GET)
Retrieves product information for a given category.

- **Query Parameters:**
  - `variable`: Category identifier.
  
- **Response:**
  - A list of products in the specified category.

---

### 3. `/search_dkp` (GET)
Searches for products by DKP code.

- **Query Parameters:**
  - `variable1`: The product DKP code.
  
- **Response:**
  - A list of matching products.

---

### 4. `/get_items` (GET)
Retrieves all products matching a specific code prefix.

- **Query Parameters:**
  - `code`: The code prefix to search.
  
- **Response:**
  - A list of matching products.

---

### 5. `/save_image_to_host` (POST)
Uploads a product image to the server.

- **Request Body:**
  - `DKP`: The product identifier.
  - `image`: The image file.
  
- **Response:**
  - Success message upon saving the image.

---

### 6. `/remove_image_from_host` (POST)
Deletes a product image from the server.

- **Request Body:**
  - `image_url`: URL of the image to delete.
  
- **Response:**
  - Success message upon deletion.

---

### 7. `/get_image_name` (GET)
Lists all images for a specific product.

- **Query Parameters:**
  - `DKP`: The product identifier.
  
- **Response:**
  - A list of image filenames.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mhdemd/RadinSport-AdminPanel.git
   cd RadinSport-AdminPanel
Set up a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
flask run
License
This project is licensed under the MIT License. You are free to use, modify, and distribute this software under the terms of the license. However, the repository owner (Mahdi Emadi) cannot upload new files to the repository.

See the LICENSE file for details.

Contribution
Contributions are welcome! Feel free to submit a pull request.

For any issues or questions, contact the repository owner:

Email: mahdi.emadi@yahoo.com
