# 🔑 Authentication & Permissions Setup

This project uses Django REST Framework (DRF) with Token Authentication to secure API endpoints.

## Authentication

### Token-based Authentication
- Uses `rest_framework.authtoken`
- Tokens are generated per user
- Required for protected endpoints

### Obtaining a Token

Make a POST request to get your authentication token:

```http
POST /api/get-token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "token": "abcdef123456..."
}
```

### Using the Token

Include the token in your request headers for authenticated endpoints:

```http
Authorization: Token abcdef123456...
```

## Permissions

The API has different permission levels for different endpoints:

| Endpoint          | Method                 | Permission Level         | Description                             |
| ----------------- | ---------------------- | ------------------------ | --------------------------------------- |
| `/api/books/`     | GET                    | Public                   | View books (no authentication required) |
| `/api/books_all/` | GET, POST, PUT, DELETE | Authenticated Users Only | Full CRUD operations on books           |

### Permission Summary

- **Public Access**: Anyone can view books via `BookList`
- **Authenticated Access**: Only authenticated users can create, update, or delete books via `BookViewSet`

Permissions are configured in `api/views.py` using DRF's `permission_classes` with the `IsAuthenticated` permission class.

## Quick Start

1. Create a user account (if not already done)
2. Obtain your token via `/api/get-token/`
3. Include the token in your Authorization header for protected endpoints
4. Start making authenticated requests to manage books

## Security Notes

- Keep your tokens secure and private
- Tokens don't expire automatically (consider implementing token rotation)
- Always use HTTPS in production to protect token transmission