import execjs

with open('js_file/Exerc.js', mode='r', encoding='utf-8') as f:
    jsEx = f.read()

m_value = execjs.compile(jsEx).call('get_en_pwd', '654')
print(m_value)
