# Documentație API

## 1. Înregistrare

**Endpoint**: `/register/`

**Metodă**: `POST`

**Acces**: Public

**Parametri**:

```jsx
http
POST /register/ HTTP/1.1
Host: yourdomain.com
Content-Type: application/json

{
    "username": "new_user",
    "email": "new_user@example.com",
    "password": "password123",
    "user_type": "student"
}
```

**Exemplu de răspuns**:

```jsx
{
    "id": 1,
    "username": "new_user",
    "email": "new_user@example.com",
    "user_type": "student"
}
```

## **2. Autentificare**

**Endpoint**: `/login/`

**Metodă**: `POST`

**Acces**: Public

**Parametri**:

- `username`: string
- `password`: string

**Exemplu de cerere**:

```jsx
POST /login/ HTTP/1.1
Host: yourdomain.com
Content-Type: application/json

{
    "username": "new_user",
    "password": "password123"
}
```

**Exemplu de răspuns**:

```jsx
{
    "refresh": "refresh_token",
    "access": "access_token",
    "user": {
        "id": 1,
        "username": "new_user",
        "email": "new_user@example.com",
        "user_type": "student"
    }
}
```

## **3. Crearea unui examen**

**Endpoint**: `/exams/create/`

**Metodă**: `POST`

**Acces**: Studenți autentificați

**Parametri**:

- `subject`: string
- `date`: datetime
- `location`: string
- `class_assigned`: int (ID-ul clasei)

**Exemplu de cerere**:

```jsx
POST /exams/create/ HTTP/1.1
Host: yourdomain.com
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
    "subject": "Mathematics",
    "date": "2024-12-15T10:00:00Z",
    "location": "Room 101",
    "class_assigned": 1
}
```

**Exemplu de răspuns**:

```jsx
{
    "id": 1,
    "subject": "Mathematics",
    "date": "2024-12-15T10:00:00Z",
    "location": "Room 101",
    "class_assigned": 1,
    "created_by": 1,
    "accepted": false,
    "rejected": false
}
```

## **4. Acceptarea unui examen**

**Endpoint**: `/exams/<int:pk>/accept/`

**Metodă**: `PATCH`

**Acces**: Profesori autentificați

**Parametri**:

- `accepted`: boolean

**Exemplu de cerere**:

```jsx
PATCH /exams/1/accept/ HTTP/1.1
Host: yourdomain.com
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
    "accepted": true
}
```

**Exemplu de răspuns**:

```jsx
{
    "status": "Exam accepted"
}
```

## **5. Respingerea unui examen**

**Endpoint**: `/exams/<int:pk>/reject/`

**Metodă**: `PATCH`

**Acces**: Profesori autentificați

**Parametri**:

- `rejected`: boolean

**Exemplu de cerere**:

```jsx
PATCH /exams/1/reject/ HTTP/1.1
Host: yourdomain.com
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
    "rejected": true
}
```

**Exemplu de răspuns**:

```jsx
{
    "status": "Exam rejected"
}
```

## **6. Lista examenelor unui utilizator**

**Endpoint**: `/student/exams/`

**Metodă**: `GET`

**Acces**: Studenți autentificați

**Parametri**: Niciunul

**Exemplu de cerere**:

```jsx
GET /user/exams/ HTTP/1.1
Host: yourdomain.com
Authorization: Bearer <your_jwt_token>
```

**Exemplu de răspuns**:

```jsx
[
    {
        "id": 1,
        "subject": "Mathematics",
        "date": "2024-12-15T10:00:00Z",
        "location": "Room 101",
        "class_assigned": 1,
        "created_by": 1,
        "accepted": false,
        "rejected": false
    }
]
```

## **7. Lista examenelor în așteptare pentru un profesor**

**Endpoint**: `/professor/pending-exams/`

**Metodă**: `GET`

**Acces**: Profesori autentificați

**Parametri**: Niciunul

**Exemplu de cerere**:

```jsx
GET /professor/pending-exams/ HTTP/1.1
Host: yourdomain.com
Authorization: Bearer <your_jwt_token>
```

**Exemplu de răspuns**:

```jsx
[
    {
        "id": 1,
        "subject": "Mathematics",
        "date": "2024-12-15T10:00:00Z",
        "location": "Room 101",
        "class_assigned": 1,
        "created_by": 1,
        "accepted": false,
        "rejected": false
    }
]
```

## **8. Lista claselor**

**Endpoint**: `/classes/`

**Metodă**: `GET`

**Acces**: Utilizatori autentificați

**Parametri**: Niciunul

**Exemplu de cerere**:

```jsx
GET /classes/ HTTP/1.1
Host: yourdomain.com
Authorization: Bearer <your_jwt_token>
```

**Exemplu de răspuns**:

```jsx
[
    {
        "id": 1,
        "name": "Computer Science - 3rd year group 3B",
        "professors": [1, 2],
        "students": [1, 2, 3, 4, 5]
    }
]
```

## **9. Detaliile unei clase**

**Endpoint**: `/classes/<int:pk>/`

**Metodă**: `GET`

**Acces**: Utilizatori autentificați

**Parametri**: Niciunul

**Exemplu de cerere**:

```jsx
GET /classes/1/ HTTP/1.1
Host: yourdomain.com
Authorization: Bearer <your_jwt_token>
```

**Exemplu de răspuns**:

```jsx
{
    "id": 1,
    "name": "Class 101",
    "professors": [1, 2],
    "students": [1, 2, 3, 4, 5]
}
```

## **10. Crearea unei clase**

**Endpoint**: `/classes/create/`

**Metodă**: `POST`

**Acces**: Utilizatori autentificați

**Parametri**:

- `name`: string
- `professors`: listă de int (ID-urile profesorilor)
- `students`: listă de int (ID-urile studenților)

**Exemplu de cerere**:

```jsx
POST /classes/create/ HTTP/1.1
Host: yourdomain.com
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
    "name": "Class 101",
    "professors": [1, 2],
    "students": [1, 2, 3, 4, 5]
}
```

**Exemplu de răspuns**:

```jsx
{
    "id": 1,
    "name": "Class 101",
    "professors": [1, 2],
    "students": [1, 2, 3, 4, 5]
}
```