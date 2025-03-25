TMPL = '''
<style>
    body {
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        background-color: #f8f8f8;
        text-align: center;
        padding: 20px 10px;
        margin: 0;
    }
    h1 {
        color: #d32f2f;
        font-size: 3.5em;
        font-weight: bold;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    h2 {
        color: #555;
        font-size: 2.5em;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .content {
        background-color: #fff;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin: 0 auto 20px;
        max-width: 90%;
        width: 100%;
    }
    .content p {
        font-size: 1.8em;
        color: #333;
        line-height: 1.8;
        text-align: left;
        margin: 0;
    }
    .content p br {
        display: block;
        content: "";
        margin-bottom: 15px;
    }
    .footer {
        font-size: 1.5em;
        color: #666;
        margin-top: 15px;
        padding: 10px;
        background-color: #f0f0f0;
        border-radius: 8px;
        display: inline-block;
    }
    .limit-reached {
        color: #d32f2f;
        font-weight: bold;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
</style>

<body>
    <h1>浅草寺抽签</h1>
    <h2>{{ title }}</h2>
    <div class="content">
        <p>
            {{ message }}
        </p>
    </div>
    {% if footer %}
    <div class="footer">
        {{ footer }}
    </div>
    {% endif %}
</body>
'''