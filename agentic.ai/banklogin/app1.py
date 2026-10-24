
from flask import Flask, request, session, render_template_string, redirect, url_for

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

correct_password = "admin123"
MAX_ATTEMPTS = 3

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Login</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        body {
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #141e30, #243b55);
            padding: 20px;
        }

        .login-card {
            background: white;
            width: 100%;
            max-width: 400px;
            padding: 35px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }

        .icon {
            width: 75px;
            height: 75px;
            line-height: 75px;
            border-radius: 50%;
            margin: 0 auto 20px;
            font-size: 35px;
            background: #e0f2fe;
        }

        h1 {
            color: #1e293b;
            font-size: 27px;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #64748b;
            font-size: 14px;
            margin-bottom: 28px;
            line-height: 1.5;
        }

        .input-group {
            text-align: left;
            margin-bottom: 20px;
        }

        label {
            display: block;
            color: #334155;
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 9px;
        }

        .password-box {
            display: flex;
            align-items: center;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            overflow: hidden;
        }

        .password-box:focus-within {
            border-color: #2563eb;
            box-shadow: 0 0 0 3px #dbeafe;
        }

        input {
            width: 100%;
            padding: 14px;
            border: none;
            outline: none;
            font-size: 15px;
            min-width: 0;
        }

        .show-btn {
            background: white;
            border: none;
            padding: 12px;
            cursor: pointer;
            color: #2563eb;
            font-weight: bold;
        }

        .login-btn, .reset-btn {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 10px;
            background: #2563eb;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        .login-btn:hover {
            background: #1d4ed8;
            transform: translateY(-2px);
        }

        .message {
            margin-bottom: 20px;
            padding: 12px;
            border-radius: 9px;
            font-size: 14px;
            line-height: 1.5;
        }

        .error {
            color: #b91c1c;
            background: #fee2e2;
        }

        .success {
            color: #166534;
            background: #dcfce7;
        }

        .locked {
            color: #9f1239;
            background: #ffe4e6;
        }

        .attempts {
            color: #64748b;
            font-size: 13px;
            margin-top: 18px;
        }

        .reset-btn {
            margin-top: 15px;
            background: #0f766e;
        }

        .reset-btn:hover {
            background: #115e59;
        }

        .footer {
            margin-top: 25px;
            font-size: 12px;
            color: #94a3b8;
        }
    </style>
</head>

<body>
    <div class="login-card">

        <div class="icon">
            {% if status == "success" %}✅
            {% elif status == "locked" %}🔒
            {% else %}🛡️{% endif %}
        </div>

        <h1>
            {% if status == "success" %}
                Login Successful
            {% elif status == "locked" %}
                Account Locked
            {% else %}
                Welcome Back!
            {% endif %}
        </h1>

        <p class="subtitle">
            {% if status == "success" %}
                You entered the correct password.
            {% elif status == "locked" %}
                Too many incorrect attempts. Access is blocked.
            {% else %}
                Enter your password to access your account.
            {% endif %}
        </p>

        {% if message %}
            <div class="message {{ status }}">
                {{ message }}
            </div>
        {% endif %}

        {% if status == "success" %}
            <form action="/reset" method="post">
                <button class="reset-btn" type="submit">
                    Logout
                </button>
            </form>

        {% elif status == "locked" %}
            <p class="attempts">Maximum attempts reached: 3/3</p>

        {% else %}
            <form method="POST" action="/">
                <div class="input-group">
                    <label for="password">Password</label>

                    <div class="password-box">
                        <input
                            type="password"
                            id="password"
                            name="password"
                            placeholder="Enter your password"
                            required
                            autofocus
                        >
                        <button
                            type="button"
                            class="show-btn"
                            onclick="togglePassword()"
                        >Show</button>
                    </div>
                </div>

                <button class="login-btn" type="submit">
                    Login →
                </button>
            </form>

            <p class="attempts">
                Attempts remaining: {{ remaining }} / 3
            </p>
        {% endif %}

        <div class="footer">
            Secure Login System | Powered by Flask
        </div>
    </div>

    <script>
        function togglePassword() {
            const password = document.getElementById("password");
            const button = document.querySelector(".show-btn");

            if (password.type === "password") {
                password.type = "text";
                button.textContent = "Hide";
            } else {
                password.type = "password";
                button.textContent = "Show";
            }
        }
    </script>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return render_template_string(
            HTML, status="success",
            message="Welcome! Access granted.",
            remaining=0
        )

    attempts = session.get("attempts", 0)
    message = ""
    status = "normal"

    if attempts >= MAX_ATTEMPTS:
        return render_template_string(
            HTML, status="locked",
            message="Your account is locked.",
            remaining=0
        )

    if request.method == "POST":
        password = request.form.get("password", "")

        if password == correct_password:
            session["logged_in"] = True
            return redirect(url_for("login"))

        attempts += 1
        session["attempts"] = attempts

        if attempts >= MAX_ATTEMPTS:
            status = "locked"
            message = "Account locked after 3 wrong attempts."
        else:
            status = "error"
            message = "Wrong password! Please try again."

    remaining = MAX_ATTEMPTS - attempts

    return render_template_string(
        HTML,
        status=status,
        message=message,
        remaining=remaining
    )


@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
