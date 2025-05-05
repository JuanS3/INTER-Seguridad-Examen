# app.py
# from fastapi import FastAPI, Request, Form
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
# from fastapi.security import HTTPBasic
# import sqlite3
# import os
# import uvicorn

app = FastAPI(title="Sistema de Gestión de Casos Legales - BJI")

security = HTTPBasic()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

def setup_database():
    if os.path.exists("legal_cases.db"):
        return

    conn = sqlite3.connect("legal_cases.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE clients (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        phone TEXT,
        address TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE cases (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        status TEXT,
        client_id INTEGER,
        assigned_to INTEGER,
        confidential BOOLEAN,
        FOREIGN KEY (client_id) REFERENCES clients (id),
        FOREIGN KEY (assigned_to) REFERENCES users (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE confidential_notes (
        id INTEGER PRIMARY KEY,
        case_id INTEGER,
        content TEXT,
        created_at TEXT,
        FOREIGN KEY (case_id) REFERENCES cases (id)
    )
    ''')

    users = [
        (19342, "admin", "S3cur3P@ssw0rd!", "admin"),
        (42342, "maria.lopez", "abogado123", "lawyer"),
        (43443, "juan.perez", "juanito2023", "lawyer"),
        (98324, "ana.garcia", "an4g4rc1a", "assistant")
    ]
    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", users)

    clients = [
        (1, "Corporación Global S.A.", "contacto@corpglobal.com", "+1-555-7890", "Calle Principal 123"),
        (2, "Industrias Tecnológicas", "legal@indtech.com", "+1-555-4567", "Avenida Central 456"),
        (3, "Roberto Méndez", "rmendez@email.com", "+1-555-1234", "Calle Secundaria 789"),
        (4, "Ministerio de Defensa", "legal@mindefensa.gov", "+1-555-6789", "Avenida Gobierno 100"),
        (5, "Compañia de Seguros", "seguros@seguros.com", "+1-555-2345", "Calle Principal 567"),
        (6, "Empresa de Transporte", "transporte@transporte.com", "+1-555-3456", "Avenida Central 890"),
        (7, "Instituto de Investigaciones Científicas", "investigaciones@investigaciones.com", "+1-555-4567", "Calle Secundaria 123"),
        (8, "Compañia de Seguros", "seguros@seguros.com", "+1-555-2345", "Calle Principal 567"),
        (9, "Empresa de Transporte", "transporte@transporte.com", "+1-555-3456", "Avenida Central 890"),
        (10, "Instituto de Investigaciones Científicas", "investigaciones@investigaciones.com", "+1-555-4567", "Calle Secundaria 123")
    ]
    cursor.executemany("INSERT INTO clients VALUES (?, ?, ?, ?, ?)", clients)

    cases = [
        (1, "Demanda por Patentes", "Disputa sobre patente tecnológica #45678", "En proceso", 1, 2, False),
        (2, "Caso de Fraude Fiscal", "Investigación sobre posible evasión fiscal", "En proceso", 2, 3, True),
        (3, "Divorcio R. Méndez", "Proceso de divorcio y división de bienes", "En proceso", 3, 2, False),
        (4, "Contrato Confidencial MD", "Revisión de contratos clasificados", "Pendiente", 4, 2, True),
        (5, "Caso de Fraude Bancario", "Investigación sobre posible fraude bancario", "En proceso", 5, 3, True),
        (6, "Divorcio J. Rodríguez", "Proceso de divorcio y división de bienes", "Finalizado", 6, 2, False),
        (7, "Caso de Fraude Bancario", "Investigación sobre posible fraude bancario", "En proceso", 7, 3, True),
        (8, "Demanda por Estafa", "Proceso de demanda por estafa", "Finalizado", 8, 2, False),
    ]
    cursor.executemany("INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?, ?)", cases)

    notes = [
        (1, 2, "Cliente admitió conocimiento de actividades fraudulentas. No documentar en el informe oficial.", "2023-01-15 14:30:00"),
        (2, 2, "Evidencia encontrada en servidor no declarado. Contiene registros contables paralelos.", "2023-01-20 09:15:00"),
        (3, 4, "Contrato incluye cláusula secreta sobre operaciones en territorio extranjero. Nivel de clasificación: ALTO", "2023-02-10 16:45:00"),
        (4, 4, "Reunión con General Martínez programada para el 05/03. No registrar en agenda oficial.", "2023-02-28 11:20:00"),
        (5, 5, "Caso de Fraude Bancario. Revisión de transacciones bancarias.", "2023-03-10 15:00:00"),
        (6, 3, "Proceso de Divorcio R. Méndez. Revisión de documentos para divorcio y división de bienes.", "2023-03-10 15:00:00"),
        (7, 8, "El endpoint de usuarios es confidencial. Revisión de seguridad. (/api/users?user_id=1)", "2025-03-10 15:00:00"),
    ]
    cursor.executemany("INSERT INTO confidential_notes VALUES (?, ?, ?, ?)", notes)

    conn.commit()
    conn.close()

setup_database()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": ""})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect("legal_cases.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    try:
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            return RedirectResponse(url="/dashboard", status_code=303)
        else:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "message": "Credenciales inválidas!"
            })
    except Exception as e:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "message": f"Error: {str(e)}"
        })
    finally:
        conn.close()

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    conn = sqlite3.connect("legal_cases.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, status, client_id FROM cases WHERE confidential = 0")
    cases = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "cases": cases
    })

@app.get("/api/cases")
async def get_cases(case_id: str = None):
    conn = sqlite3.connect("legal_cases.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        if case_id:
            query = f"SELECT * FROM cases WHERE id = {case_id}"
            cursor.execute(query)
        else:
            cursor.execute("SELECT * FROM cases")

        cases = [dict(row) for row in cursor.fetchall()]
        return {"status": "success", "data": cases}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

@app.get("/api/users")
async def get_users(user_id: str = None):
    conn = sqlite3.connect("legal_cases.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        if user_id:
            query = f"SELECT * FROM users WHERE id = {user_id}"
            cursor.execute(query)
            users = [dict(row) for row in cursor.fetchall()]
            return {"status": "success", "data": users}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

@app.get("/api/notes")
async def get_notes(case_id: str = None):
    conn = sqlite3.connect("legal_cases.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        if case_id:
            query = f"SELECT * FROM confidential_notes WHERE case_id = {case_id}"
            cursor.execute(query)
        else:
            cursor.execute("SELECT * FROM confidential_notes")

        notes = [dict(row) for row in cursor.fetchall()]
        return {"status": "success", "data": notes}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
