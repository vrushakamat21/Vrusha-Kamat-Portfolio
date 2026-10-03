with open('js/main.js', encoding='utf-8') as f:
    js = f.read()

# Fix 1: default theme to dark
js = js.replace("return 'light';", "return 'dark'; // dark-first design")

# Fix 2: guard scrollTopBtn null
old_st = "    if (scrollY > 500) {\n      scrollTopBtn.classList.add('visible');\n    } else {\n      scrollTopBtn.classList.remove('visible');\n    }"
new_st = "    if (scrollTopBtn) {\n      if (scrollY > 500) { scrollTopBtn.classList.add('visible'); }\n      else { scrollTopBtn.classList.remove('visible'); }\n    }"
js = js.replace(old_st, new_st)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Done")
print("dark default:", "return 'dark'" in js)
print("scrollTopBtn guard:", "if (scrollTopBtn)" in js)
