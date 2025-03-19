TMPL = '''
<style>
    body {
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        background-color: #f8f8f8;
        text-align: center;
        padding: 40px;
        margin: 0;
    }
    h1 {
        color: #d32f2f;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    h2 {
        color: #555;
        font-size: 2em;
        margin-top: 10px;
        margin-bottom: 30px;
    }
    .content {
        background-color: #fff;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin: 0 auto;
        max-width: 800px;
    }
    .content p {
        font-size: 1.5em;
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
</style>

<body>
    <h1>浅草寺抽签</h1>
    <h2>{{ title }}</h2>
    <div class="content">
        <p>
            {{ message }}
        </p>
    </div>
</body>
'''