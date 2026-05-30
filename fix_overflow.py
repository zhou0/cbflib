with open('examples/adscimg2cbf_sub.c', 'r') as f:
    content = f.read()

content = content.replace('sprintf(temp, "%s=%s;\\n", s, s1);', 'snprintf(temp, sizeof(temp), "%s=%s;\\n", s, s1);')

with open('examples/adscimg2cbf_sub.c', 'w') as f:
    f.write(content)
