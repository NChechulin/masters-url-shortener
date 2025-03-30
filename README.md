# URL Shortener

Кратко:

- есть cоздание / удаление / изменение / получение информации по короткой ссылке
- есть статистика
- есть кастомные ссылки
- есть поиск ссылки по оригинальному URL
- есть время жизни
- есть авторизация
- БД Postgres + Redis для кеширования (при удалении удаляем и из кеша)

## Deploy

- Demo: https://masters-url-shortener.onrender.com/docs (честно потратил N времени чтобы понять что там как с сетями и не до конца уверен что оно норм работает)
- Local: `docker-compose up -d --build`

## Api

Примеры запросов можно прямо в сваггере потыкать: https://masters-url-shortener.onrender.com/docs

```
curl -X 'POST' \
  'https://masters-url-shortener.onrender.com/links/shorten' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "original_url": "https://example.com/",
  "custom_alias": "string",
  "expiration": "2025-03-30T18:01:19.664Z"
}'
```

```
{
  "original_url": "https://example.com/",
  "alias": "string",
  "click_count": 0,
  "creation": "2025-03-30T18:01:26.733Z",
  "last_access": "2025-03-30T18:01:26.733Z"
}
```

### Schema

```json
"/links/shorten": {
  "post": {
    "tags": [
      "Links"
    ],
    "summary": "Create Short Link",
    "operationId": "create_short_link_links_shorten_post",
    "requestBody": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/LinkCreateModel"
          }
        }
      },
      "required": true
    },
    "responses": {
      "200": {
        "description": "Successful Response",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/LinkDetailsModel"
            }
          }
        }
      },
      "422": {
        "description": "Validation Error",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/HTTPValidationError"
            }
          }
        }
      }
    },
    "security": [
      {
        "OAuth2PasswordBearer": []
      }
    ]
  }
},
"/links/{short_code}": {
  "get": {
    "tags": [
      "Links"
    ],
    "summary": "Redirect",
    "operationId": "redirect_links__short_code__get",
    "parameters": [
      {
        "name": "short_code",
        "in": "path",
        "required": true,
        "schema": {
          "type": "string",
          "title": "Short Code"
        }
      }
    ],
    "responses": {
      "200": {
        "description": "Successful Response",
        "content": {
          "application/json": {
            "schema": {}
          }
        }
      },
      "422": {
        "description": "Validation Error",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/HTTPValidationError"
            }
          }
        }
      }
    }
  },
  "delete": {
    "tags": [
      "Links"
    ],
    "summary": "Delete",
    "operationId": "delete_links__short_code__delete",
    "security": [
      {
        "OAuth2PasswordBearer": []
      }
    ],
    "parameters": [
      {
        "name": "short_code",
        "in": "path",
        "required": true,
        "schema": {
          "type": "string",
          "title": "Short Code"
        }
      }
    ],
    "responses": {
      "200": {
        "description": "Successful Response",
        "content": {
          "application/json": {
            "schema": {}
          }
        }
      },
      "422": {
        "description": "Validation Error",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/HTTPValidationError"
            }
          }
        }
      }
    }
  },
  "put": {
    "tags": [
      "Links"
    ],
    "summary": "Update",
    "operationId": "update_links__short_code__put",
    "security": [
      {
        "OAuth2PasswordBearer": []
      }
    ],
    "parameters": [
      {
        "name": "short_code",
        "in": "path",
        "required": true,
        "schema": {
          "type": "string",
          "title": "Short Code"
        }
      }
    ],
    "requestBody": {
      "required": true,
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/LinkUpdateModel"
          }
        }
      }
    },
    "responses": {
      "200": {
        "description": "Successful Response",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/LinkDetailsModel"
            }
          }
        }
      },
      "422": {
        "description": "Validation Error",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/HTTPValidationError"
            }
          }
        }
      }
    }
  }
},
"/links/{short_code}/stats": {
  "get": {
    "tags": [
      "Links"
    ],
    "summary": "Statistics",
    "operationId": "statistics_links__short_code__stats_get",
    "security": [
      {
        "OAuth2PasswordBearer": []
      }
    ],
    "parameters": [
      {
        "name": "short_code",
        "in": "path",
        "required": true,
        "schema": {
          "type": "string",
          "title": "Short Code"
        }
      }
    ],
    "responses": {
      "200": {
        "description": "Successful Response",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/LinkDetailsModel"
            }
          }
        }
      },
      "422": {
        "description": "Validation Error",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/HTTPValidationError"
            }
          }
        }
      }
    }
  }
},
"/links/search": {
  "get": {
    "tags": [
      "Links"
    ],
    "summary": "Search Links",
    "description": "Search for all short URLs created by the current user that match the given original URL.\nReturns a list of links (or an empty list if none are found).",
    "operationId": "search_links_links_search_get",
    "security": [
      {
        "OAuth2PasswordBearer": []
      }
    ],
    "parameters": [
      {
        "name": "original_url",
        "in": "query",
        "required": true,
        "schema": {
          "type": "string",
          "title": "Original Url"
        }
      }
    ],
    "responses": {
      "200": {
        "description": "Successful Response",
        "content": {
          "application/json": {
            "schema": {
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/LinkDetailsModel"
              },
              "title": "Response Search Links Links Search Get"
            }
          }
        }
      },
      "422": {
        "description": "Validation Error",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/HTTPValidationError"
            }
          }
        }
      }
    }
  }
},
"/auth/register": {
  "post": {
    "tags": [
      "Auth"
    ],
    "summary": "Register",
    "operationId": "register_auth_register_post",
    "requestBody": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/UserCreationModel"
          }
        }
      },
      "required": true
    },
    "responses": {
      "200": {
        "description": "Successful Response",
        "content": {
          "application/json": {
            "schema": {}
          }
        }
      },
      "422": {
        "description": "Validation Error",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/HTTPValidationError"
            }
          }
        }
      }
    }
  }
},
"/auth/login": {
  "post": {
    "tags": [
      "Auth"
    ],
    "summary": "Login",
    "operationId": "login_auth_login_post",
    "requestBody": {
      "content": {
        "application/x-www-form-urlencoded": {
          "schema": {
            "$ref": "#/components/schemas/Body_login_auth_login_post"
          }
        }
      },
      "required": true
    },
    "responses": {
      "200": {
        "description": "Successful Response",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/TokenModel"
            }
          }
        }
      },
      "422": {
        "description": "Validation Error",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/HTTPValidationError"
            }
          }
        }
      }
    }
  }
}
```
