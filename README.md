# Wishlist Application

This is a Flask-based web application for managing a wishlist. The application allows users to add, view, and remove items from their wishlist.

## Features

- Add new items to the wishlist
- View the wishlist
- Remove items from the wishlist
- View the history of removed items (visible in the .db)

## Requirements

- Docker

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com-Psychodelic42:Psychodelic42/wishlist.git
   cd wishlist
   ```

2. run docker build process
   ```bash
   sudo docker build -t wishlist .
   
3. docker run or start image in portainer/whatever you are using

4. enjoy the application on http://[IP OR HOSTNAME]:44555/
